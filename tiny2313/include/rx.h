/**
 * eve (https://github.com/ni-c/eve)
 *
 * @file    include/rx.h
 * @brief   Unit to read the signal from the RX receiver
 * @author  Willi Thiel (ni-c@ni-c.de)
 * @date    Jan 24, 2014
 */

#ifndef RX_H_
#define RX_H_

/**
* Initialization of the RX part
*/
void rx_init(void);

/*
 * Enable the RX module
 */
void rx_enable(void);

/*
 * Disable the RX module
 */
void rx_disable(void);

#endif /* RX_H_ */
