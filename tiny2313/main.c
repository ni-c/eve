/**
 * eve (https://github.com/ni-c/eve)
 *
 * @file    main.c
 * @brief   Main program
 * @author  Willi Thiel (ni-c@ni-c.de)
 * @date    Jan 23, 2014
 *
 * I2C addresses:
 * 0x00-0x01: Control register (on/off)
 * 0x02-0x03: Remaining steps stepper 1
 * 0x04-0x05: Remaining steps stepper 2
 * 0x06-0x07: Remaining steps stepper 3
 * 0x08-0x09: Speed stepper 1
 * 0x0a-0x0b: Speed stepper 2
 * 0x0c-0x0d: Speed stepper 3
 * 0x0e-0x0f: Add steps to stepper 1
 * 0x10-0x11: Add steps to stepper 2
 * 0x12-0x13: Add steps to stepper 3
 * 0x14: RX Channel 1
 * 0x15: RX Channel 2
 * 0x16: RX Channel 3
 * 0x17: RX Channel 4
 * 0x18: RX Channel 5
 * 0x19: RX Channel 6
 * 0x1a: RX Channel 7
 * 0x1b: RX Channel 8
 *
 */

#include 	<stdlib.h>
#include 	<avr/io.h>
#include 	<avr/interrupt.h>
#include 	<avr/pgmspace.h>

#include    "main.h"
#include    "i2cslave.h"
#include    "rx.h"
#define 	I2CADDRESS 0x34

volatile uint8_t control_register[2] = {0, 0};

void init(void) {
    // Disable interrupts
    cli();

    // TWI slave init
    i2c_init(I2CADDRESS);

    // RX init
    rx_init();

    // Re-enable interrupts
    sei();

    for (int i = 0; i < I2C_BUFFER_SIZE; i++)
        i2c_buffer[i] = 0;
}

int main(void) {

    // Set LED (port 1) to output
    DDRD |= (1 << DDD0);
    PORTD |= (1 << PD0);

    init();

    while (1) {

        if (control_register[0] != i2c_buffer[0]) {
            control_register[0] = i2c_buffer[0];
            // Bit 1 in control register 0 = RX-Receiver;
            if ((control_register[0] >> 1)  & 0x01) {
                rx_enable();
            } else {
                rx_disable();
            }
        }


/*
        uint16_t val = ((uint16_t)i2c_buffer[1] << 8) | i2c_buffer[0];
        if (val == 1337) {
            // port d0 high
            PORTD |= (1 << PD0);
        } else {
            // port d0 low
            PORTD &= ~(1 << PD0);
        }
        */
    }
}
