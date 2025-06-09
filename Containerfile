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

COPY src/ksbuilder.py /usr/local/bin/

WORKDIR /workspace

# Default entrypoint (can override)
ENTRYPOINT ["python3", "/usr/local/bin/ksbuilder.py"]
