import os
import sys
import argparse
import subprocess
import shutil
import re

def abspath(path):
    return os.path.abspath(path)

def run(cmd, check=True):
    print(" ".join(cmd))
    subprocess.run(cmd, check=check)

def get_size_mib(folder):
    total = 0
    for dirpath, _, files in os.walk(folder):
        for f in files:
            total += os.path.getsize(os.path.join(dirpath, f))
    return max(64, (total // (1024**2)) + 50)

def patch_inst_stage2(file_path, old_label, new_label):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    patched = data.replace(f"inst.stage2=hd:LABEL={old_label}", f"inst.stage2=hd:LABEL={new_label} inst.ks=hd:LABEL={new_label}:/ks.cfg")
    # Optionally, handle cases where spaces or quotes are around the label
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(patched)

def ensure_clean_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Create bootable USB image with kickstart file from ISO")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--kickstart", required=True, help="Path to ks.cfg file to copy into root of USB image")
    parser.add_argument("--version", help="Version info for OS (replaces {{version}} in ks.cfg")
    parser.add_argument("--diskpath", help="Disk path to use for installation (replaces {{diskpath}} in ks.cfg)")
    parser.add_argument("--rootsizemib", type=int, help="Size of root partition in MiB (replaces {{rootsizemib}} in ks.cfg)")
    parser.add_argument("--user", help="main user of the installed system (root disabled, replaces {{user}} in ks.cfg)")
    parser.add_argument("--userpwhash", help="Password hash for user (replaces {{userpwhash}} in ks.cfg)")
    args = parser.parse_args()

    label = "OEMDRV"

    worktemp = "/worktemp"
    extract_dir = abspath(os.path.join(worktemp, "iso"))
    fat_path = abspath(os.path.join(worktemp, "fat"))

    # Patch kickstart template with provided parameters
    ks_src = args.kickstart
    with open(ks_src, "r", encoding="utf-8") as f:
        ks_data = f.read()
    if args.version:
        ks_data = ks_data.replace("{{version}}", args.version)
    if args.diskpath:
        ks_data = ks_data.replace("{{diskpath}}", args.diskpath)
    if args.rootsizemib is not None:
        ks_data = ks_data.replace("{{rootsizemib}}", str(args.rootsizemib))
    if args.userpwhash:
        ks_data = ks_data.replace("{{user}}", args.user)
    if args.userpwhash:
        ks_data = ks_data.replace("{{userpwhash}}", args.userpwhash)
    # Write patched kickstart to temp file
    patched_ks_path = os.path.join(worktemp, "patched_ks.cfg")
    os.makedirs(worktemp, exist_ok=True)
    with open(patched_ks_path, "w", encoding="utf-8") as f:
        f.write(ks_data)
    ks_to_copy = patched_ks_path

    ensure_clean_dir(extract_dir)
    ensure_clean_dir(fat_path)

    # Copy extra files
    if os.path.isdir(f"{args.kickstart}.d/"):
        run(["rsync", "-aH", f"{args.kickstart}.d/", f"{extract_dir}/"])

    # Calculate required FAT32 size
    fat_size_mib = get_size_mib(extract_dir)

    img_path = abspath(args.output)

    # Build image
    run(["qemu-img", "create", "-f", "raw", img_path, f"{fat_size_mib}M"])
    run(["parted", "--script", img_path, "mklabel", "gpt",
         "mkpart", "primary", "fat32", "1MiB", "100%"])

    # Mount loop and partition
    loopdev = subprocess.check_output(["losetup", "--show", "-fP", img_path]).decode().strip()
    run(["kpartx", "-av", loopdev])

    part1 = f"/dev/mapper/{os.path.basename(loopdev)}p1"
    run(["mkfs.vfat", "-F", "32", "-n", label, part1])
    run(["mount", part1, fat_path])

    # Copy everything
    run(["rsync", "-aH", f"{extract_dir}/", f"{fat_path}/"])

    # Copy ks.cfg to the root of the FAT32 partition

    shutil.copy2(abspath(ks_to_copy), os.path.join(fat_path, "ks.cfg"))
    print("Copied Kickstart to image root")

    run(["umount", fat_path])
    run(["kpartx", "-d", loopdev])
    run(["losetup", "-d", loopdev])

    print("Bootable USB image created:", img_path)

if __name__ == "__main__":
    main()
