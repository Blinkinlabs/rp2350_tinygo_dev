# Build a docker image for developing with TinyGo on RPI2040
#
# Included in the image is:
# * Go in /usr/local/go/
# * openocd (rpi pico version) in /usr/local
# * RP2350 bootloader and symbols in /pico/pico-bootrom-rp2350
# * development version of TinyGo in /usr/local/tinygo/

FROM docker.io/library/debian:12 AS base

ARG TARGETOS
ARG TARGETARCH

RUN apt-get -qq update -y

# Nice to have
RUN DEBIAN_FRONTEND=noninteractive \
      apt-get install -y --no-install-recommends \
            vim \
            tmux \
            wget \
            ca-certificates \
            make \
            usbutils \
            gdb-multiarch \
            git \
            gnupg2 \
            build-essential \
            cmake \
            ninja-build \
            automake \
            autoconf \
            texinfo \
            libtool \
            libftdi-dev \
            libusb-1.0-0-dev \
            pkg-config


# https://github.com/tinygo-org/docker/blob/main/Dockerfile
ENV GO_RELEASE=1.23.2
RUN wget https://dl.google.com/go/go${GO_RELEASE}.${TARGETOS}-${TARGETARCH}.tar.gz && \
    tar xfv go${GO_RELEASE}.${TARGETOS}-${TARGETARCH}.tar.gz -C /usr/local && \
    find /usr/local/go -mindepth 1 -maxdepth 1 ! -name 'src' ! -name 'VERSION' ! -name 'bin' ! -name 'pkg' ! -name 'go.env' -exec rm -rf {} +

ENV PATH=${PATH}:/usr/local/go/bin

# Use premade (bring your own) LLVM for TinyGo
WORKDIR /llvm
RUN echo 'deb http://apt.llvm.org/bookworm/ llvm-toolchain-bookworm-18 main' | tee /etc/apt/sources.list.d/llvm.list
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-get -qq update -y
RUN apt-get install -y --no-install-recommends \
    clang-18 llvm-18-dev lld-18 libclang-18-dev

# OpenOCD
WORKDIR /pico
RUN git clone https://github.com/raspberrypi/openocd.git --depth=1
WORKDIR /pico/openocd
RUN ./bootstrap && \
    ./configure --prefix=/usr/local && \
    make -j12 && \
    make install

# Pico bootloader (for debugging image boot)
WORKDIR /pico
RUN wget https://github.com/raspberrypi/pico-bootrom-rp2350/releases/download/A2/arm-bootrom.elf
RUN git clone https://github.com/raspberrypi/pico-bootrom-rp2350.git
WORKDIR /pico/pico-bootrom-rp2350
RUN git submodule update --init --recursive

ENV GOBIN=/build/tinygo-bin
ENV PATH=${PATH}:/build/tinygo-bin

RUN useradd -ms /bin/bash go
USER go

#WORKDIR /
#RUN git clone https://github.com/tinygo-org/tinygo.git
#WORKDIR /tinygo
#RUN git checkout rp2350-add 

#RUN git submodule update --init --recursive
#RUN go install
##RUN make llvm-source
#RUN make gen-device
#


