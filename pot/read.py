# sudo apt-get install python3-paho-mqtt
# python3 read.py --read_port ttyACM0 --send_location "LED_ness"


import serial
import argparse
import sys
import paho.mqtt.publish as publish
import time

# Setup argument parser
parser = argparse.ArgumentParser(description='Read data from a specified serial port.')
parser.add_argument('--send_location', type=str, help='Location of the device')
parser.add_argument('--read_port', type=str, required=True, help='Symlink name of the TTY port (e.g., toggler1)')
args = parser.parse_args()

# Function to connect to the serial port
def connect_to_serial(port_name):
    try:
        return serial.Serial(f'/dev/{port_name}', 115200, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port /dev/{port_name}: {e}")
        return None

# Attempt to connect to the serial port
ser = connect_to_serial(args.read_port)

# Continuously try to read from the serial port
while True:
    if ser:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)  # Print the raw line for debug purposes
                publish.single(args.send_location, line, hostname="arpa.net.ai")
        except (serial.SerialException, OSError) as e:
            print(f"Serial error: {e}")
            ser.close()
            ser = None
    else:
        print(f"Waiting for device /dev/{args.read_port} at {args.send_location}...")
        ser = connect_to_serial(args.read_port)
        time.sleep(5)  # Wait before trying to reconnect

    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program terminated by user")
        if ser:
            ser.close()
        sys.exit(0)

