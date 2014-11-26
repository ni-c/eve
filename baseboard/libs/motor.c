/**
 * eve (https://github.com/ni-c/eve)
 *
 * @file    lib/motor.c
 * @brief   Control unit for the stepper motors
 * @author  Willi Thiel (ni-c@ni-c.de)
 * @date    Jan 25, 2014
 *
 * Connection:
 *
 * AtTiny   Conn.    TB6550  Description
 * =====================================
 * PD4  ->  P1   ->   P1     Enable
 * PD0  ->  P2   ->   P3     Dir X
 * PD5  ->  P3   ->   P4     Step Y
 * PD1  ->  P4   ->   P5     Dir Y
 * PB4  ->  P5   ->   P7     Dir Z
 * PD6  ->  P6   ->   P22    Ground
 * PB3  ->  P7   ->   P6     Step Z
 * PB0  ->  P8   ->
 * PB2  ->  P9   ->   P2     Step X
 * PB1  ->  P10  ->
 *
 */

#include <inttypes.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include "main.h"
#include "motor.h"
#include "i2cslave.h"

#define I2C_MOTOR_BUFFER_OFFSET 2 /*!< I2C offset for the Motor buffer (where the Motor buffer begins in the I2C buffer */

uint16_t speed_cnt[3] = { 0, 0, 0 };

uint16_t speed[3] = { 0, 0, 0 };
uint16_t steps[3] = { 0, 0, 0 };

/**
 * Timer Compare Interrupt
 */
ISR (TIMER0_COMPA_vect) {

    // Allow interruption (from I2C)
    sei();

    // Disable our motors if the where enabled last round
    PORTB &= ~((1 << PB2) | (1 << PB3));
    PORTD &= ~(1 << PD5);

    for (uint8_t i = 0; i < 3; ++i) {

        // Do we have steps left
        if (steps[i] != 0) {
            // Have we reached our target speed
            if (speed_cnt[i]++ > speed[i]) {
                steps[i]--;
            	uint8_t buffer = I2C_MOTOR_BUFFER_OFFSET + i * 2;
                i2c_buffer[buffer + 1] = steps[i] & 0xff;
                i2c_buffer[buffer] = (steps[i] >> 8);
                speed_cnt[i] = 0;
                switch(i) {
                case 0:
                    // X-CLK
                    PORTB |= (1 << PB2);
                    break;
                case 1:
                    // Y-CLK
                    PORTD |= (1 << PD5);
                    break;
                default:
                    // Z-CLK
                    PORTB |= (1 << PB3);
                	break;
                }
            }
        }
    }
}

/**
 * Update the values of the motor control
 */
void motor_update(void) {
    for (uint8_t i = 0; i < 3; ++i) {
    	uint8_t buffer = I2C_MOTOR_BUFFER_OFFSET + i * 2;
        speed[i] = ((uint16_t) i2c_buffer[buffer + 6] << 8) | i2c_buffer[buffer + 7];
        steps[i] = ((uint16_t) i2c_buffer[buffer] << 8) | i2c_buffer[buffer + 1];
    }
}

/**
 * Update the motor directions
 */
void motor_update_register(volatile uint8_t *control_register) {
    // Bit 2 in control register: Direction Motor X;
    if ((control_register[0] >> 2) & 0x01) {
        PORTD &= ~(1 << PD0);
    } else {
        PORTD |= (1 << PD0);
    }
    // Bit 3 in control register: Direction Motor Y;
    if ((control_register[0] >> 3) & 0x01) {
        PORTD &= ~(1 << PD1);
    } else {
        PORTD |= (1 << PD1);
    }
    // Bit 4 in control register: Direction Motor Z;
    if ((control_register[0] >> 4) & 0x01) {
        PORTB &= ~(1 << PB4);
    } else {
        PORTB |= (1 << PB4);
    }
    // Bit 5 in control register: en/disable motorcontrol
    if ((control_register[0] >> 5) & 0x01) {
        PORTD &= ~(1 << PD4);
    } else {
    	PORTD |= (1 << PD4);
    }
    // Bit 6 in control register: relais
    if ((control_register[0] >> 6) & 0x01) {
        PORTB &= ~(1 << PB0);
    } else {
    	PORTB |= (1 << PB0);
    }
}

/**
 * Motor initialization
 */
void motor_init(void) {

    // Set ports to output
    DDRB |= (1 << DDB0) | (1 << DDB2) | (1 << DDB3) | (1 << DDB4);
    DDRD |= (1 << DDD0) | (1 << DDD1) | (1 << DDD4) | (1 << DDD5);

    // Disable TB6560
    PORTD |= (1 << PD4);

    // Disable TB6550 Relais
    PORTB |= (1 << PB0);

    // CTC Modus
    TCCR0A = (1 << WGM01);

    // 64 prescale
    TCCR0B |= (1 << CS01) | (1 << CS00);

    // Output-Compare
    OCR0A = TIMER_COMPARE;

    // Enable interrupt
    TIMSK |= (1 << OCIE0A);
}
