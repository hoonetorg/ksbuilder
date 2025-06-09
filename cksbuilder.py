import sys
import subprocess
import shlex
import os
import argparse

IMAGE_NAME = "ksbuilder"
CONTAINERFILE = "Containerfile"


def runwrapper(cmdlist):
    """Prints the command (ready to copy/paste), then runs it."""
    if isinstance(cmdlist, str):
        print(f"\n[RUN]: {cmdlist}")
        subprocess.check_call(cmdlist, shell=True)
    else:
        cmd_str = " ".join(shlex.quote(str(a)) for a in cmdlist)
        print(f"\n[RUN]: {cmd_str}")
        subprocess.check_call(cmdlist)

def build_image():
    cmd = f"podman build -t {IMAGE_NAME} -f {CONTAINERFILE} ."
    print("Building image:", cmd)
    runwrapper(shlex.split(cmd))

def run_container(workdir, args):
    abs_workdir = os.path.abspath(workdir)
    print(f"abs_workdir: {abs_workdir}")
    cmd = [
        "podman", 
        "run", 
        "--name", IMAGE_NAME, 
        "--rm", 
        "--privileged",
        "-v", f"{abs_workdir}:/workspace:z",
        "-w", "/workspace",
        IMAGE_NAME
    ] + args
    #print("Running container:", " ".join(shlex.quote(a) for a in cmd))
    runwrapper(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build and run Container building a bootable USB image with kickstart file")
    parser.add_argument("--workdir", type=str, default=".", help="Host workdir to mount into container (/workspace)")
    args, passthrough = parser.parse_known_args()

    build_image()
    run_container(args.workdir, passthrough)

