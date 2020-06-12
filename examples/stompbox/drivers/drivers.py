import vibrance.driver.uart

serial_ports = vibrance.driver.uart.list_ports()

drivers = []

for port in serial_ports:
    drivers.append(vibrance.driver.uart.SerialDriver(f"Arduino on {port}",
                                                     port))
