# TinyGo development enviroment for RP2350

This is a containerized environment for working on porting TinyGo to the RP2350. It sets up the following tools:

* RP2350 boot room source, for boot issue debugging
* RPi fork of OpenOCD
* Go and LLVM as TinyGo prerequisites (from packaged distributions)

The TinyGo source tree, TinyGo binary, and sample application live outside of the container, and are mapped into it for compilation and debugging.

The provided Makefile gives canned routines for building and debugging the sample application.

Quick instructions:

```
git clone https://github.com/Blinkinlabs/rp2350_tinygo_dev.git
cd rp2350_tinygo_dev
sudo cp 99-openocd.rules /etc/udev/rules.d
cd docker
make docker-image
make run
(from inside container) bash provision_tinygo.sh
exit
(from outside container) make build
make flash
```

Then, the TinyGo files can be edited either inside or outside of the container, and the various make targets
allow for flashing and debugging a program using the pico debug probe.
Note that you will need to change the tinygo git origin manually, if you plan to push changes back to Github.
