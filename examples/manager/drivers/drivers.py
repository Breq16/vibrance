import vibrance.driver.midi
import vibrance.driver.uart
import vibrance.driver.pygame_if
import vibrance.driver.keypad

drivers = []
drivers.append(vibrance.driver.midi.MidiDriver("Ableton MIDI", "vibrance"))
drivers.append(vibrance.driver.uart.SerialDriver("Arduino Serial", "/dev/ttyUSB0"))
drivers.append(vibrance.driver.pygame_if.PyGameDriver("PyGame Demo"))
drivers.append(vibrance.driver.keypad.KeypadDriver("Terminal Keys"))
