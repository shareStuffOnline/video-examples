from machine import ADC, Pin
import time

# Initialize ADC for GP28 (Pin 28) which corresponds to ADC2
adc = ADC(Pin(28))

# Function to map the value from one range to another
def map_value(value, in_min, in_max, out_min, out_max):
    return max(out_min, min(out_max, (value - in_min) * (out_max - out_min + 1) // (in_max - in_min) + out_min))

# List to store the readings for moving average
window_size = 3
readings = [0] * window_size

# Time interval for printing the reading
print_interval = 0.1  # 100 milliseconds
next_print_time = time.ticks_ms() + print_interval * 1000

# Variable to store the last printed value
last_printed_value = None

while True:
    # Read the analog value
    reading = adc.read_u16()

    # Update the readings list
    readings.pop(0)
    readings.append(reading)

    # Check if it's time to print
    if time.ticks_ms() >= next_print_time:
        # Calculate the average of the readings
        average_reading = sum(readings) // window_size

        # Map the average reading from 0-65535 to 0-255
        mapped_reading = map_value(average_reading, 100, 65535, 0, 255)

        # Check if the mapped reading has changed
        #if mapped_reading != last_printed_value:
        if last_printed_value is None or abs(mapped_reading - last_printed_value) > 2:
            # Print the denoised reading
            print(mapped_reading)

            # Update the last printed value
            last_printed_value = mapped_reading

        # Update the next print time
        next_print_time += print_interval * 1000

    time.sleep(0.001)  # 1 millisecond

