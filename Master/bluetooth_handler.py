import subprocess
import threading
import time

def connect_bluetooth(mac_address):
    while True:
        try:
            command = f"sudo rfcomm connect rfcomm0 {mac_address}"
            subprocess.run(command.split(), check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        print("Bluetooth connection lost. Retrying in 5 seconds...")
        #subprocess.run("sudo rfcomm release rfcomm0".split(), check=True)
        time.sleep(5)

def check_bluetooth_status(mac_address):
    
    cmd = f"bluetoothctl info {mac_address}"
    result = subprocess.run(cmd.split(), capture_output=True, text=True)
    output_lines = result.stdout.splitlines()

    for line in output_lines:
        if "Connected:" in line:
            status = line.split()[1]
            if status == "yes":
                return True

    return False


mac_address = "00:18:E4:34:D9:54"
threadStatus = False

if not check_bluetooth_status(mac_address):
    
    print("Connecting to HC-05...")
    thread = threading.Thread(target=connect_bluetooth, args=(mac_address,))
    threadStatus = True
    thread.start()

while not check_bluetooth_status(mac_address):
    time.sleep(1)
    print("Waiting for the connection")
    
print("Bluetooth Connection established successfully")
time.sleep(1)
print("Transfering Control to Main Thread")
# Your main code here
#while 1:
#    pass


