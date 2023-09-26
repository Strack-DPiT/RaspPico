'''
_________________________   _______________._______  ___.______________
\_   _____/\______   \   \ /   /\_   _____/|   \   \/  /|   \__    ___/
 |    __)   |     ___/\   Y   /  |    __)  |   |\     / |   | |    |   
 |     \    |    |     \     /   |     \   |   |/     \ |   | |    |   
 \___  /    |____|      \___/    \___  /   |___/___/\  \|___| |____|   
     \/                              \/              \_/               

'''
import machine
import utime
# Initialize the SPI bus
# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(13, machine.Pin.OUT)
switch_receive = machine.Pin(15, machine.Pin.OUT)
switch_transmit = machine.Pin(14, machine.Pin.OUT)
# Initialize SPI
spi = machine.SPI(1,
                  baudrate=1000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(12))
def send_data(addr, data):
    # Start the SPI transaction by pulling NSEL low
    cs.value(0)

    # Send the bytes through SPI
    mask = 0x80
    tmp = addr | mask
    spi.write(bytes([tmp , data]))
    # End the SPI transaction by pulling NSEL high
    cs.value(1)

def read_data(addr):
    # Start the SPI transaction by pulling NSEL low
    cs.value(0)

    # Send the address byte for read access (bit 7: 1, bits 6-1: 000000)
    mask = 0x00
    spi.write(bytes([addr | mask]))

    # Read the data from the slave (MISO line)
    response = spi.read(1)

    # End the SPI transaction by pulling NSEL high
    cs.value(1)

    return response[0]
def main():
     # Sleep
    #while True:
    addr = 0b0000001
    data = 0b00000000
    send_data(addr,data)
        
        # LoRa enable

    addr = 0b0000001
    data = 0b10000000
    send_data(addr,data)
        
    addr = 0b0000001
    response_data = read_data(addr)   
    print(f"Current operation mode: {response_data:08b}")
        
        #Set FifoAddrPtr to FifoRxBaseAddr
    addr = 0b0001101
    data = 0b00000000
    send_data(addr,data)
        #Implicit header mode on 
        #RegModemConfig1
    addr = 0b0011101
    data = 0b00001101
    send_data(addr,data)
        #set RegModemconfig2
    addr = 0b0011110
    data = 0b11000100
    send_data(addr,data)
        #Set RegPayloadLength (0x22) 
    addr = 0b0100010
    data = 0b00001000 #8 bytes payload
    send_data(addr,data)
        
    addr = 0b0000001
    data = 0b10000001
    send_data(addr,data)
        #Set RegDioMapping1 to 0x10
    addr = 0b1000000
    data = 0b10101010
    send_data(addr,data)
        #Set RegDioMapping2 to 0x10
    addr = 0b1000001
    data = 0b10100000
    send_data(addr,data)
        #channel activity mode detector enable
    addr = 0b0000001
    data = 0b10000111
    send_data(addr,data)
        #check if cad detected gpio20 == 3v3
    #clear irq
    addr = 0b0010010
    data = 0b11111111
    send_data(addr,data)
    # Add some delay to avoid continuous looping
    utime.sleep_ms(100)  # Sleep for 100 milliseconds
        #remap Dio 0,1,2,3,4,5 to default 
        #Set RegDioMapping1 to default
    addr = 0b1000000
    data = 0b00000000
    send_data(addr,data)
        #Set RegDioMapping2 to default
    addr = 0b1000001
    data = 0b00000000
    send_data(addr,data)
        #mode request RXsingle
    addr = 0b0000001
    data = 0b10000110
    send_data(addr,data)
    switch_receive.value(1)
    utime.sleep_ms(1000)
        
        #maximum timeout
    addr = 0b0011111
    data = 0b11001000
    send_data(addr,data)


    addr = 0b0010011
    response_data = read_data(addr)
    
    while (response_data == 0b00000000):
        addr = 0b0010011
        response_data = read_data(addr)
        print(f"Waiting for packet")
        
        
    print(f"Received packet number of bytes: {response_data:08b}")  # Print the response in binary format
    switch_receive.value(0)
        #clear irq
    addr = 0b0010010
    data = 0b11111111
    send_data(addr,data)
       #read bytes received in the FIFO MEMORY
    data_values = [
        0b00000000,
        0b00000001,
        0b00000010,
        0b00000011,
        0b00000100,
        0b00000101,
        0b00000110,
        0b00000111,
    ]

    for counter, data_value in enumerate(data_values, start=1):
        addr = 0b0001101
        data = data_value
        send_data(addr, data)
            
            # Read memory
        addr = 0b0000000
        response_data = read_data(addr)
            
        print(f"Received data from the FIFO#{counter}: {response_data:08b}")
        
if __name__ == "__main__":
    main()
