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
#include "i2cslave.h"

// Global Vars
volatile uint16_t pulse = 0; /*!< Number of timer pulses */
volatile uint8_t channelIndex = 0; /*!< Current channel index */
volatile uint8_t channelPos[] = { 0, 0, 0, 0, 0, 0, 0, 0 }; /*!< Positions of the channel */

ISR( TIMER1_COMPA_vect ) {
    /* 1 tick = 200µs */
    pulse++;
    TCNT1 = 0;
}

ISR( INT0_vect ) {
    /* Read pulseTime in µs */
    uint16_t pulseTime = pulse * 200 + 4 * TCNT1 / 5;
    /* Reset Timer */
    TCNT1 = 0;
    pulse = 0;

    /* pulse > 3000 µs => Sync */
    if (pulseTime > 3000) {
        /* Write channelvalues to I2C buffer */
        for (int i = 0; i < 8; ++i) {
            i2c_buffer[i] = channelPos[i];
        }
        /* Start from the beginning */
        channelIndex = 0;
    } else if (channelIndex < 8) {
        /* Save channel position and increase servo index */
        channelPos[channelIndex++] = (pulseTime - 1000) / 5;
    }
}

/**
 * Initialization of the RX part
 */
void rx_init(void) {

    /* Timer 1 */
    TCCR1B |= (1 << CS11); /* Prescaler 8 - 400ns */
    TIMSK |= (1 << OCIE1A); /* Timer/Counter1, Output Compare A Match Interrupt Enable */
    OCR1A = 500; /* 200µs */

    /* Enable Pin Change Interrupt on falling edge */
    DDRD &= ~(1 << PD2);
    PORTD |= (1 << PD2);
    MCUCR |= (1 << ISC01);
    GIMSK |= (1 << INT0);
}
