import random

import time

from datetime import datetime

from azure.iot.device import IoTHubDeviceClient, Message

import adafruit_dht

import board
 
# Azure IoT Hub configuration

IOT_HUB_HOSTNAME = "trumeterHub.azure-devices.net"  

DEVICE_ID = "HERE"  # Replace with your device ID

DEVICE_SYMMETRIC_KEY = "HERE"  # Replace with your symmetric key
 
# Create the connection string for the device

CONNECTION_STRING = f"HostName={IOT_HUB_HOSTNAME};DeviceId={DEVICE_ID};SharedAccessKey={DEVICE_SYMMETRIC_KEY}"
 
# Initialise the DHT11 sensor

dht_device = adafruit_dht.DHT11(board.D4)  # GPIO4 (Pin 7)
 
# Simulate dummy sensor data

def generate_dummy_serial_data():

    temperature = round(random.uniform(20.0, 30.0), 2)

    humidity = round(random.uniform(30.0, 70.0), 2)

    timestamp = time.time()

    return {

        "deviceId": DEVICE_ID,

        "temperature": temperature,

        "timestamp": timestamp,

        "test": True,
 
    }
 
# Generate payload for DHT11 sensor data

def generate_sensor_payload(temperature, timestamp):

    return {

        "deviceId": DEVICE_ID,

        "temperature": temperature,

        "timestamp": timestamp

    }
 
def main():

    try:

        # Initialize the IoT Hub client

        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        print("Connected to Azure IoT Hub")
 
        while True:

            try:

                # Read from the DHT11 sensor

                temperature = dht_device.temperature

                humidity = dht_device.humidity
 
                # Get the current timestamp

                timestamp = time.time()
 
                if humidity is not None and temperature is not None:

                    # Prepare payload for real sensor data

                    payload = generate_sensor_payload(temperature, timestamp)

                    print(f"Sensor data available: {payload}")

                else:

                    raise RuntimeError("Sensor returned None values")
 
            except RuntimeError as error:

                # Handle sensor read errors by using dummy data

                print(f"Sensor read error: {error}. Using dummy data.")

                payload = generate_dummy_serial_data()
 
            # Send the message

            message = Message(str(payload).replace("'", '"'))  # Convert to JSON-compliant string

            client.send_message(message)

            print(f"Message sent: {payload}")
 
            # Wait before sending the next message

            time.sleep(2)
 
    except Exception as e:

        print(f"Error: {e}")

    finally:

        # Disconnect the client

        client.shutdown()
 
if __name__ == "__main__":

    main()

 
