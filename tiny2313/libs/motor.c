/**
 * eve (https://github.com/ni-c/eve)
 *
 * @file    lib/motor.c
 * @brief   Control unit for the stepper motors
 * @author  Willi Thiel (ni-c@ni-c.de)
 * @date    Jan 25, 2014
 */

#include <inttypes.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include "main.h"
#include "motor.h"
#include "i2cslave.h"

#define I2C_MOTOR_BUFFER_OFFSET 2 /*!< I2C offset for the RX buffer (where the RX buffer begins in the I2C buffer */

uint16_t speed_cnt[3] = { 0, 0, 0 };

uint16_t speed[3] = { 0, 0, 0 };
uint16_t steps[3] = { 0, 0, 0 };

struct s_enabled {
    uint8_t x :1;
    uint8_t y :1;
    uint8_t z :1;
} enabled;

/**
 * Timer Compare Interrupt
 */
ISR (TIMER0_COMPA_vect) {

    // Allow interruption (from I2C)
    sei();

    // Disable our motors if the where enabled last round
    if (enabled.x == 1) {
        PORTB &= ~(1 << PB2);
        enabled.x = 0;
    }
    if (enabled.y == 1) {
        PORTD &= ~(1 << PD5);
        enabled.y = 0;
    }
    if (enabled.z == 1) {
        PORTB &= ~(1 << PB3);
        enabled.z = 0;
    }

    for (int i = 0; i < 3; ++i) {

        // Do we have steps left
        if (steps[i] > 0) {
            speed_cnt[i]++;
            // Have we reached our target speed
            if (speed_cnt[i] > speed[i]) {
                steps[i]--;
                i2c_buffer[I2C_MOTOR_BUFFER_OFFSET + 1 + i * 2] = steps[i] & 0xff;
                i2c_buffer[I2C_MOTOR_BUFFER_OFFSET + i * 2] = (steps[i] >> 8);
                speed_cnt[i] = 0;
                if (i == 0) {
                    // X-CLK
                    enabled.x = 1;
                    PORTB |= (1 << PB2);
                } else if (i == 1) {
                    // Y-CLK
                    enabled.y = 1;
                    PORTD |= (1 << PD5);
                } else {
                    // Z-CLK
                    enabled.z = 1;
                    PORTB |= (1 << PB3);
                }
            }
        }
    }
}

/**
 * Update the values of the motor control
 */
void motor_update(void) {
    for (int i = 0; i < 3; ++i) {
        speed[i] = ((uint16_t) i2c_buffer[I2C_MOTOR_BUFFER_OFFSET + 6 + i * 2] << 8) | i2c_buffer[I2C_MOTOR_BUFFER_OFFSET + 7 + i * 2];
        steps[i] = ((uint16_t) i2c_buffer[I2C_MOTOR_BUFFER_OFFSET + i * 2] << 8) | i2c_buffer[I2C_MOTOR_BUFFER_OFFSET + 1 + i * 2];
    }
}

/**
 * Motor initialization
 */
void motor_init(void) {

    // Set ports B2 (OC0A), B3 (OC1A) and D5 (OC0B) to output
    DDRB |= ((1 << DDB2) | (1 << DDB3));
    DDRD |= (1 << DDD5);

    // CTC Modus
    TCCR0A = (1 << WGM01);

    // 64 prescale
    TCCR0B |= (1 << CS01) | (1 << CS00);

    // Output-Compare
    OCR0A = TIMER_COMPARE;

    // Enable interrupt
    TIMSK |= (1 << OCIE0A);
}
