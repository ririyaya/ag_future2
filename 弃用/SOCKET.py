#  ip.addr eq 119.145.36.53
import socket
import requests
import time
import winsound
import sys
import pyaudio
import wave
import traceback
req=b"\x30\x30\x30\x30\x30\x30\x36\x34\x23\x61\x67\x61\x69\x6e\x5f\x66\x6c\x61\x67\x3d\x30\x23\x75\x73\x65\x72\x5f\x69\x64\x3d\x31\x31\x30\x31\x38\x31\x35\x34\x34\x35\x23\x75\x73\x65\x72\x5f\x6b\x65\x79\x3d\x39\x34\x31\x35\x35\x37\x31\x30\x33\x23\x75\x73\x65\x72\x5f\x74\x79\x70\x65\x3d\x32\x23"
list=[0,0]
tail=''
key="instID=Ag(T+D)#last" #19
key2="#weig"
chunk = 1024
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '119.145.36.53'
port = 17003
vvol,hold,count,nowvol,pastvol=0,0,0,0,0
client.bind(('192.168.1.12', 11560)) #本地端口
client.connect((host, port))
client.send(req)
posi="Posi"

#print(client.recv(1024))
#client.close()

def gethold(a):
 id1=a.find("Posi=")
 id2=a.find("#RspCode")
 return int(a[id1+5:id2])
 
def getvol(a):
 id1=a.find('volume=')
 id2=a.find("#weig")
 if 'volume' in a:
  return int(a[id1+7:id2])
 else:
  return 0
 
def audio(a):
 wf = wave.open(a, 'rb')
 p = pyaudio.PyAudio()
 stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
  channels=wf.getnchannels(),
  rate=wf.getframerate(),
  output=True)
 data = wf.readframes(chunk)
 while len(data) > 0:
  stream.write(data)
  data = wf.readframes(chunk)
  
def now():
 now = int(time.time())
 timeArray = time.localtime(now)
 StyleTime = time.strftime("%H:%M:%S", timeArray)#%Y-%m-%d 
 return StyleTime
 
def fwrite(a,b,c):
 f=open('D://log.txt','a')
 f.write(a+'\t'+b+'\t'+c+'\r')
 f.close()

while 0==0:
 try:
  recve=str(bytes(client.recv(400))).replace("'",'').replace('\\','').replace('b','')
  rec=tail+recve
  #length=len(rec)
  if key in rec and key2 in rec:
   #print(recve)
   pastvol=nowvol
   nowvol=getvol(rec)
   samevol=vvol
   vvol=nowvol-pastvol
   #print(rec)
   if vvol>5000 and vvol!=samevol:
    #audio('D:/PositiveBling.wav')
    count+=1
    if vvol>9000 or count==2:
     #hhold,hold=hold,gethold(tail1+tail+recve)
     audio('D:/PositiveBling.wav')
     print(vvol,now())
     #count=0
   #elif abs(nowvol-pastvol)>2500:
    #audio('D:/232.wav')
    #fwrite(str(vvol),str(hold-hhold),now())
  else:
   #tail1=tail
   tail=recve
   #print(rec)
 except Exception as e:
  print(e)
  traceback.print_exc()
  #print(rec)
  #print(tail)
  #input()
  client.close()
  pass
 
 


 

'''

f=open('D://sjr.txt','a')
f.write(client.recv(4000).decode())
f.close()
 
#    00000064#again_flag=0#user_id=1101815445#user_key=941557103#user_type=2#


for i in range(2):
    list[i]=vol(rec)
    a=abs(list[1]-list[0])
    if a>20000:
     print(list,a)#audio()








def __init__(self,host,port):
    self.port = port
    self.host = host
    self.status = 0
    self.BUF_SIZE = 1024
def connect(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    self.client.connect((self.host, self.port))
def send(self,mes):
    client.startResv()
    while True:
        self.client.send(mes.encode())
        time.sleep(1)
def resv(self):
    while True:
        data = self.client.recv(self.BUF_SIZE)
        text = data.decode()
        print(text)
def startResv(self):
    t = threading.Thread(target=self.resv)
    t.start()
'''