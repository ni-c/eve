#!/usr/bin/python

import threading, inspect, datetime


def debug(message):
    dt = datetime.datetime.now()
    func = inspect.currentframe().f_back.f_code
    print "\033[33m%s \033[37;1m> \033[32;1mDEBUG \033[37;1m> \033[37m%s:%i \033[37;1m> \033[34;1m%s \x1b[0m" %(dt, func.co_filename, func.co_firstlineno, message)
    return True

def info(message):
    dt = datetime.datetime.now()
    func = inspect.currentframe().f_back.f_code
    print "\033[33m%s \033[37;1m> \033[37;1mINFO  \033[37;1m> \033[37m%s:%i \033[37;1m> \033[34;1m%s \x1b[0m" %(dt, func.co_filename, func.co_firstlineno, message)
    return True

def warn(message):
    dt = datetime.datetime.now()
    func = inspect.currentframe().f_back.f_code
    print "\033[33m%s \033[37;1m> \033[33;1mWARN  \033[37;1m> \033[37m%s:%i \033[37;1m> \033[34;1m%s \x1b[0m" %(dt, func.co_filename, func.co_firstlineno, message)
    return True    

def error(message):
    dt = datetime.datetime.now()
    func = inspect.currentframe().f_back.f_code
    print "\033[33m%s \033[37;1m> \033[31;1mERR   \033[37;1m> \033[37m%s:%i \033[37;1m> \033[34;1m%s \x1b[0m" %(dt, func.co_filename, func.co_firstlineno, message)
    return True    