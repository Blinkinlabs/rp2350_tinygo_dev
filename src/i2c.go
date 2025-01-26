package main

import (
        "machine"
        "time"
        "fmt"
)

var (
)

func main() {
    led := machine.LED
    led.Configure(machine.PinConfig{Mode: machine.PinOutput})

    i2c := machine.I2C0
    err := i2c.Configure(machine.I2CConfig{Frequency: 100000})
    if err != nil {
        fmt.Println("could not configure I2C:", err)
        return
    }

    for {
        led.High()

        w := []byte{0x75}
        r := make([]byte, 1)
        err = i2c.Tx(0x68, w, r)
        if err != nil {
            fmt.Println("could not interact with I2C device:", err)
            //return
        }

        led.Low()

        time.Sleep(500*time.Millisecond)
    }
}
