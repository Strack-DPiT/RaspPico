import _thread
import utime
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import json
#from updateDisplay import update_display
from functions import *

userData = {"lat": 46.123, "long": 23.123, "user_id": "David"}
bluetooth_data = {
    "type": "L",
    "user_id": "",
    "lat": 43.123,
    "long": 23.123,
    "heard_devices": {
    }
}
lora_data=""

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()
# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

def get_gps_data():
    userData["lat"] += 1
    userData["long"] += 1
    print("Gps Data Updated", userData)

def lora_send():
    global lora_data
    lora_data = parse_data(userData)
    print("Lora Data Sent", lora_data)
    
def lora_receive():
    # remove all the previously heard devices
    bluetooth_data["heard_devices"] = []
    
    # mock received data
    received_data = "LDavid***43.11123000"
    received_data = reverse_parse_data(received_data)
    
    bluetooth_data["heard_devices"].append(received_data)

    print("Receive Lora Messages")
    print(bluetooth_data)
    
def send_bluetooth_data():
    global bluetooth_data  
    bluetooth_data["lat"] = userData["lat"]
    bluetooth_data["long"] = userData["long"]
    bluetooth_data["user_id"] = userData["user_id"]
    debounce_time = 0
    if (time.ticks_ms()-debounce_time) > 300:
        if sp.is_connected():
            bluetooth_data_json = json.dumps(userData)
            sp.send(bluetooth_data_json)
            print("BluetoothSent")
        debounce_time = time.ticks_ms()
    print("Bluetooth Data Sent", bluetooth_data)

while(True):
    
    get_gps_data()
    lora_send()
    lora_receive()
    utime.sleep(30)
    #update_display()