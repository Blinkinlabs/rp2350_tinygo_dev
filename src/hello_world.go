package main

import (
        "machine"
        "time"
        "fmt"
)

var (
    usbcdc = machine.USBCDC
)

func main() {
    led := machine.LED
    led.Configure(machine.PinConfig{Mode: machine.PinOutput})

    count := 0
    for {
        led.Low()
        fmt.Println("Hello world!", count)
//        usbcdc.WriteByte('a')
        
        time.Sleep(500*time.Millisecond)

        led.High()
        fmt.Println("xxx")
//        usbcdc.WriteByte('b')
        time.Sleep(500*time.Millisecond)

        count++
    }
}
