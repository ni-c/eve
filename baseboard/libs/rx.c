/**
 * eve (https://github.com/ni-c/eve)
 *
 * @file    lib/rx.c
 * @brief   Unit to read the signal from the RX receiver
 * @author  Willi Thiel (ni-c@ni-c.de)
 * @date    Jan 24, 2014
 */

// Includes
#include <avr/io.h>
#include <avr/interrupt.h>
#include "main.h"
#include "i2cslave.h"

// Global Vars
uint16_t pulse = 0; /*!< Number of timer pulses */
uint8_t channelIndex = 0; /*!< Current channel index */
uint8_t channelPos[] = { 0, 0, 0, 0, 0, 0, 0, 0 }; /*!< Positions of the channel */

#define I2C_RX_BUFFER_OFFSET 20 /*!< I2C offset for the RX buffer (where the RX buffer begins in the I2C buffer */

/**
 * Timer compare interrupt
 */
ISR( TIMER1_COMPA_vect ) {
    // 1 tick = 200µs
    pulse++;
    TCNT1 = 0;
}

/*
 * External interrupt INT0
 */
ISR( INT0_vect ) {
    // Read pulseTime in µs
    uint16_t pulseTime = pulse * 200 + 4 * TCNT1 / 5;
    // Reset Timer
    TCNT1 = 0;
    pulse = 0;

    // pulse > 3000 µs => Sync
    if (pulseTime > 3000) {
        // Start from the beginning
        channelIndex = 0;
        // Write channelvalues to I2C buffer
        for (int i = 0; i < 8; ++i) {
            i2c_buffer[i + I2C_RX_BUFFER_OFFSET] = channelPos[i];
        }
    } else if (channelIndex < 8) {
        // Save channel position and increase servo index
        channelPos[channelIndex++] = (pulseTime - 1000) / 5;
    }
}

/*
 * Enable the RX module
 */
void rx_enable(void) {
    // Enable RX12 (PIN D3)
    PORTD |= (1 << PD3);

    // Enable Timer 1 and Interrupt 0
    TIMSK |= (1 << TOIE1);
    GIMSK |= (1 << INT0);
}

/*
 * Disable the RX module
 */
void rx_disable(void) {
    // Disable Timer 1 and Interrupt 0
    TIMSK &= ~(1 << TOIE1);
    GIMSK &= ~(1 << INT0);

    // Disable RX12 (PIN D3)
    PORTD &= ~(1 << PD3);

    // Clear Buffer
    for (int i = 0; i < 8; ++i) {
        channelPos[i] = 0;
        i2c_buffer[i + I2C_RX_BUFFER_OFFSET] = 0;
    }
}

/**
 * Initialization of the RX part
 */
void rx_init(void) {

    // Set PIN D3 to output
    DDRD |= (1 << DDD3);

    // Prescaler 8 - 400ns
    TCCR1B |= (1 << CS11);

    // Timer/Counter1, Output Compare A Match Interrupt Enable
    TIMSK |= (1 << OCIE1A);

    // 200µs
    OCR1A = 500;

    // Enable Pin Change Interrupt on falling edge
    DDRD &= ~(1 << PD2);
    PORTD |= (1 << PD2);
    MCUCR |= (1 << ISC01);

    // Disable RX
    rx_disable();
}
