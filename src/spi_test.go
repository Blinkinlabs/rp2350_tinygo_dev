package main

import (
        "machine"
        "time"
        "fmt"
)

var (
)

func main() {
    fmt.Println("starting...")
    time.Sleep(500*time.Millisecond)

    led := machine.LED
    led.Configure(machine.PinConfig{Mode: machine.PinOutput})

    // Output SPI on pins 
    spi := machine.SPI0
    err := spi.Configure(machine.SPIConfig{Frequency: 4000000})
    if err != nil {
        fmt.Println("could not configure SPI:", err)
        return
    }

    for {
        led.High()
        fmt.Println("doing tx")

        w := []byte{0x75,0x56}
        r := make([]byte, 2)
        err = spi.Tx(w, r)
        if err != nil {
            fmt.Println("could not interact with SPI device:", err)
            //return
        }

        led.Low()

        time.Sleep(500*time.Millisecond)
    }
}
