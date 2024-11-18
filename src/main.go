//https://tinygo.org/docs/reference/microcontrollers/pico/

package main

import (
        "machine"
//        "time"
//        "fmt"
)

func main() {

    led := machine.LED
    led.Configure(machine.PinConfig{Mode: machine.PinOutput})

    for {
        led.Low()
        led.High()
    }

//    count := 0
//    for {
//        fmt.Println("Hello world!", count)
//        count++
//
//        led.Low()
//        time.Sleep(time.Millisecond * 200)
//
//        led.High()
//        time.Sleep(time.Millisecond * 1000)
//
//        led.Low()
//        time.Sleep(time.Millisecond * 200)
//
//        led.High()
//        time.Sleep(time.Millisecond * 200)
//    }
}
