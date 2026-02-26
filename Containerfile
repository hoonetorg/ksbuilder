FROM almalinux:10

RUN dnf -y install \
    qemu-img \
    parted \
    kpartx \
    dosfstools \
    e2fsprogs \
    btrfs-progs \
    util-linux \
    rsync \
    && dnf clean all \
    && rm -rf /var/cache/dnf


RUN mkdir -p /ksbuilder
WORKDIR /ksbuilder

COPY src/ksbuilder /usr/local/bin/
RUN chmod +x /usr/local/bin/ksbuilder

# Default entrypoint (can override)
ENTRYPOINT ["/usr/local/bin/ksbuilder"]
