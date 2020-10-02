
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import dht
esp.osdebug(None)
import gc
gc.collect()

ssid = 'AXTEL XTREMO-EF67'
password = '036AEF67'
mqtt_server = '192.168.15.119'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'/casa/temp_hum'
temp=0
hum=0

last_message = 0
message_interval = 10
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

sensor = dht.DHT22(machine.Pin(32))

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
  
def temp_hum():
  sensor.measure()
  time.sleep(1)
  return
  
  
  

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    #sensor.measure()
    #temp= sensor.temperature()
    #hum=sensor.humidity()
    #print(temp)
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      temp_hum()
      temp = sensor.temperature()
      hum = sensor.humidity()
      #print(temp)
      if isinstance(temp, float) and isinstance(hum, float):
        msg =(b'{0:3.1f},{1:3.1f}'.format(temp, hum))
        #msg = temp
        #print(topic_pub)
        client.publish(topic_pub, msg)
        last_message = time.time()
        counter += 1
        
      
  except OSError as e:
    restart_and_reconnect()

