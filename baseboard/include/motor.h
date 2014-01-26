/**
 * eve (https://github.com/ni-c/eve)
 *
 * @file    include/motor.h
 * @brief   Control unit for the stepper motors
 * @author  Willi Thiel (ni-c@ni-c.de)
 * @date    Jan 25, 2014
 */

#ifndef MOTOR_H_
#define MOTOR_H_

#define TIMER_COMPARE 16 /*!< Timer compare */

/**
 * Motor initialization
 */
void motor_init(void);

/**
 * Update the values of the motor control
 */
void motor_update(void);

#endif /* MOTOR_H_ */
