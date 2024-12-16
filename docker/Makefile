# Mount this host directory at /build in the container
SRC_DIR=`pwd`/../
BUILD_DIR=/build

DOCKER_IMAGE_NAME=rp2350_tinygo_dev

TARGET=../src/main.elf

COMMON= run \
        --rm \
		--mount type=bind,source=${SRC_DIR},target=${BUILD_DIR} \
		-w ${BUILD_DIR}

all:
	@echo "Build targets: "
	@echo "docker-image         Build an image for building tools with Docker"
	@echo "run                  (for debugging) Run a shell using the above image"
	@echo "flash                Build the firmware, then flash using openocd"
	@echo "openocd-server       Start an OpenOCD session, attached to the target"
	@echo "gdb                  Connect to the debug server using gdb-multiarch"

docker-image:
	docker build -t ${DOCKER_IMAGE_NAME} -f Dockerfile .

run:
	docker ${COMMON} \
		--privileged \
		-v /dev/bus/usb:/dev/bus/usb \
		--net=host \
		-it ${DOCKER_IMAGE_NAME} \
		/usr/bin/bash

build:
	docker ${COMMON} \
		--privileged \
		-it ${DOCKER_IMAGE_NAME} \
		/usr/bin/bash -c "cd src; make"

flash:
	docker ${COMMON} \
		--privileged \
		-v /dev/bus/usb:/dev/bus/usb \
		-it ${DOCKER_IMAGE_NAME} \
		/usr/local/bin/openocd \
			-f interface/cmsis-dap.cfg \
			-f target/rp2350.cfg \
			-c "rp2350.dap.core1 cortex_m reset_config sysresetreq" \
			-c "adapter speed 5000" \
			-c "program src/main.elf verify ; reset ; exit"


# This should work without --net=host ?
openocd-server:
	docker ${COMMON} \
		--privileged -v /dev/bus/usb:/dev/bus/usb \
		--net=host \
		-it ${DOCKER_IMAGE_NAME} \
		/usr/local/bin/openocd \
			-f interface/cmsis-dap.cfg \
			-f target/rp2350.cfg \
			-c "adapter speed 5000"

gdb:
	docker ${COMMON} \
		--net=host \
		-it ${DOCKER_IMAGE_NAME} \
		/usr//bin/gdb-multiarch \
		--se=src/main.elf \
		-x /build/gdb-app-setup

