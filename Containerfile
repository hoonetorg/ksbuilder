FROM almalinux:10

RUN dnf -y install \
    qemu-img \
    parted \
    kpartx \
    dosfstools \
    util-linux \
    rsync \
    bsdtar \
    python3 \
    findutils \
    && dnf clean all

RUN mkdir -p /ksbuilder
WORKDIR /ksbuilder

COPY src/ksbuilder /usr/local/bin/
RUN chmod +x /usr/local/bin/ksbuilder

# Default entrypoint (can override)
ENTRYPOINT ["/usr/local/bin/ksbuilder"]
