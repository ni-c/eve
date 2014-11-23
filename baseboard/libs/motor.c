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
 * Update the motor directions
 */
void motor_update_register(volatile uint8_t *control_register) {
    // Bit 2 in control Direction Motor X;
    if ((control_register[0] >> 2) & 0x01) {
        PORTD &= ~(1 << PD0);
    } else {
        PORTD |= (1 << PD0);
    }
    // Bit 3 in control Direction Motor Y;
    if ((control_register[0] >> 3) & 0x01) {
        PORTD &= ~(1 << PD1);
    } else {
        PORTD |= (1 << PD1);
    }
    // Bit 4 in control Direction Motor Z;
    if ((control_register[0] >> 4) & 0x01) {
        PORTB &= ~(1 << PB4);
    } else {
        PORTB |= (1 << PB4);
    }
}

/**
 * Motor initialization
 */
void motor_init(void) {

    // Set ports to output
    DDRB |= (1 << DDB2) | (1 << DDB3) | (1 << DDB4);
    DDRD |= (1 << DDD0) | (1 << DDD1) | (1 << DDD4) | (1 << DDD5);

    // CTC Modus
    TCCR0A = (1 << WGM01);

    // 64 prescale
    //TCCR0B |= (1 << CS01) | (1 << CS00);

    TCCR0B |= (1 << CS02) | (1 << CS00);

    // Output-Compare
    OCR0A = TIMER_COMPARE;

    // Enable interrupt
    TIMSK |= (1 << OCIE0A);

    // Enable TB6560
    PORTD &= ~(1 << PD4);

}
