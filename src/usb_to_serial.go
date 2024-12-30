package main

import (
        "machine"
//        "time"
        "fmt"
)

var (
    uart = machine.UART1
    usbcdc = machine.USBCDC
)

func main() {
    fmt.Println("USB to Serial converter demo\r\n")

    pin := machine.GPIO7
    pin.Configure(machine.PinConfig{Mode: machine.PinOutput})
    pin.High()


    c := machine.UARTConfig{
        BaudRate: 62500,
        TX : machine.UART1_TX_PIN,
        RX : machine.UART1_RX_PIN,
    }
    uart.Configure(c)


    led := machine.LED
    led.Configure(machine.PinConfig{Mode: machine.PinOutput})

    led.High()

    for {
        // Transmit data from USB to UART
        if usbcdc.Buffered() > 0 {
            led.Low()

            data, err := usbcdc.ReadByte()

            if err == nil {
                uart.WriteByte(data)
            }

            led.High()
        }

        // Transmit data from UART to USB
        if uart.Buffered() > 0 {
            led.Low()

            data, err := uart.ReadByte()

            if err == nil {
                usbcdc.WriteByte(data)
            }

            led.High()
        }
    }
}
