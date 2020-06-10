import vibrance.driver.uart

drivers = []
drivers.append(vibrance.driver.uart.SerialDriver("Arduino Serial",
                                                 "/dev/ttyUSB0"))
