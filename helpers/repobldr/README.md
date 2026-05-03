 repobldr - Build and run the repobldr container
#
# Creates a Fedora Workstation offline-install repo tarball (f<VERSION>ws.tgz)
# suitable for use with a kickstart %repo line pointing at a local partition.
#
# Typical workflow
# ----------------
#   # 1. Build the container once (needs internet + podman)
#   ./repobldr --build
#
#   # 2. Build the repo tarball for Fedora 44
#   ./repobldr --version 44 --outputdir /srv/repo
#   #  → /srv/repo/f44ws.tgz
#
#   # 3. On an air-gapped machine: export / import the container image
#   ./repobldr --export-image /media/usb/repobldr.oci
#   ./repobldr --import-image /media/usb/repobldr.oci
#   ./repobldr --version 44 --outputdir /srv/repo
#
#   # 4. Interactive debug session inside the container
#   ./repobldr --version 44 --outputdir /srv/repo --interactive

# Packages added on top of the base set inside repobldr.
# Passed as positional arguments to the container entrypoint after the version.
# Use --packages on the command line to extend this list.

