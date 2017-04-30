import time, serial, random
import paho.mqtt.client as mqtt

#subprocess.call("sudo rfcomm connect hci0 98:D3:32:10:BA:4D",shell=False)

bt_serial = serial.Serial("/dev/rfcomm0", baudrate=9600)

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe("water/#")

def on_message(client, userdata, msg):
	print msg.topic, " ", str(msg.payload)
	to_serial = "3" + str(msg.payload).split(":")[2] +"\r\n";
	bt_serial.write(to_serial)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("termin8", "jeghaterbarnmedraraksent")
client.connect("termin8.tech", 8883, 60)

client.loop_start()

def read_data():
	data = ''
	char = ''
	while char != '\n':
		char = str(bt_serial.read())
		data += char
	return data[:-1]

def create_message():
	full_data = ["0","0","0"]
	for i in range(0, len(full_data)):
		data = read_data()
		full_data[int(data[0])] = data[1:]
	return str(int(time.time())) + ":" + full_data[0] + ":" + full_data[2] 
		
plant_ids = [5,6,7,8,19]

while True:
	message = create_message()	

	target = "data/" + str(random.choice(plant_ids))
	print target + "\t" + message
	client.publish(target, message)

	time.sleep(60)

# call client.loop_stop(force=False) at some point 