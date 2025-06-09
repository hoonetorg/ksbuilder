
# Example running command
assuming u have the 

`Fedora-Silverblue-ostree-x86_64-42-1.1.iso`

with `sha256sum`

`099d6b580b557d5d86c2485b0404119d8e68f90de69ec02c1a2b25c4d4ad7dbc`

run

```
python3 cksbuilder.py --workdir /home/johndoe/ksbuilder/ksfiles --output ad_fa-inst_sb_42_1disk.img --kickstart ks_fa_1disk.cfg --version "fedora/42/x86_64/silverblue" --diskpath "/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi0-0-0-0" --rootsizemib 20480 --user hoo --userpwhash '$y$j...'
```

or for the Kinoite ISO

```
python3 cksbuilder.py --workdir /home/johndoe/ksbuilder/ksfiles --output ad_fa-inst_kinoite_42_1disk.img --kickstart ks_fa_1disk.cfg --version "fedora/42/x86_64/kinoite" --diskpath "/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi0-0-0-0" --rootsizemib 20480 --user hoo --userpwhash '$y$j...'
```

or for the Cosmic ISO

```
python3 cksbuilder.py --workdir /home/johndoe/ksbuilder/ksfiles --output ad_fa-inst_cosmic_42_1disk.img --kickstart ks_fa_1disk.cfg --version "fedora/42/x86_64/cosmic-atomic" --diskpath "/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_drive-scsi0-0-0-0" --rootsizemib 20480 --user hoo --userpwhash '$y$j...'
```

some notes on arguments

`--workdir`

- is the dir where all the files referenced are or will be created, like
    - `--output` file
    - `--kickstart` file

`--kickstart`

- name of input kickstart template file (`<workdir>/<kickstart>`)

`--output`

- name of the disk image file containing a `FAT32` partition named `OEMDRV` (so that RH/Fedora ISO automatically detects it as ks.cfg source), containing
    - the rendered `ks.cfg`

`--version`

- an arbitrary string that will replace {{version}} in the `kickstart` template

`--diskpath`

- an arbitrary string that will replace {{diskpath}} in the `kickstart` template
    - it's important for the existing templates in `./ksfiles` that the `diskpath` is in form `/dev/disk/by-id/<link-to-a-disk-not-a-partition`, the whole template `%pre` script logic depends on it
    - `--diskpath "/dev/sda"` will most probably fail and is dangerous if more than 1 disk is used

`--rootsizemib`

- an arbitrary integer that will replace {{rootsizemib}} in the `kickstart` template
    - in the existing templates the var `rootsizemib` is used to define the size of the `luks v2` partition containing the root fs

`--user`

- an arbitrary string that will replace {{user}} in the `kickstart` template
    - in the existing templates the var `user` is used to define the user name for the main user of the system (root disabled)

`--userpwhash`

- an arbitrary string that will replace {{userpwhash}} in the `kickstart` template
    - in the existing templates the var `userpwhash` is used to define the user password hash
