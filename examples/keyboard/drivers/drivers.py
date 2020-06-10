import vibrance.driver.pygame_if
import vibrance.driver.keypad

drivers = []
drivers.append(vibrance.driver.pygame_if.PyGameDriver("PyGame Demo"))
drivers.append(vibrance.driver.keypad.KeypadDriver("Terminal Keys"))
