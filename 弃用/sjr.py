import socket
import requests
import winsound
import sys
import time
import pyaudio
import wave
import traceback
req=b"\x30\x30\x30\x30\x30\x30\x36\x34\x23\x61\x67\x61\x69\x6e\x5f\x66\x6c\x61\x67\x3d\x30\x23\x75\x73\x65\x72\x5f\x69\x64\x3d\x31\x31\x30\x31\x38\x31\x35\x34\x34\x35\x23\x75\x73\x65\x72\x5f\x6b\x65\x79\x3d\x33\x34\x39\x38\x38\x35\x32\x30\x32\x23\x75\x73\x65\x72\x5f\x74\x79\x70\x65\x3d\x32\x23"
#00000064#again_flag=0#user_id=1101815445#user_key=349885202#user_type=2#
list=[0,0]
tail=''
key="instID=Ag(T+D)#last" #19
key2="#weig"
chunk = 1024
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '58.250.197.67'
port = 17003
vvol,hold,count,nowvol,pastvol=0,0,0,0,0
#client.bind(('192.168.1.4', 11560)) #本地端口
client.connect((host, port))
client.send(req)
posi="Posi" #持仓

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
 time_array = time.localtime(now)
 style_time = time.strftime("%H:%M:%S", time_array)#%Y-%m-%d
 return style_time

def fwrite(a,b,c):
 f=open('D://log.txt','a')
 f.write(a+'\t'+b+'\t'+c+'\r')
 f.close()



f=open('D://log.txt','a')
while True:
 try:
  bt=client.recv(400)
  recve=str(bytes(bt)).replace("'",'').replace('\\','').replace('b','')
  rec=tail+recve
  #length=len(rec)
  #print(bt)
  if key in rec and key2 in rec:
   #print(rec)
   pastvol,nowvol=nowvol,getvol(rec)
   #samevol=vvol
   vvol=nowvol-pastvol
   hhold,hold=hold,gethold(tail+recve)
   if vvol>1000:
    print(vvol,hold-hhold)
    #f.write(str(vvol)+'\r')
#   if vvol>80 and vvol!=samevol and vvol<6000:
    if vvol>3000:
     audio('D:/PositiveBling.wav')
    #count+=1
    #if   vvol>30 :#or count==2:
     
#audio('D:/PositiveBling.wav')
#     print(int(vvol/2),now())
#     count=0
   #elif abs(nowvol-pastvol)>2500:
    #audio('D:/232.wav')
    #fwrite(str(vvol),str(hold-hhold),now())
  else:
   #tail1=tail
   tail=recve
   #print(rec)
 except: # BaseException as e:
  #print(e)
  traceback.print_exc()  #print(traceback.format_exc())
  print(bt)
  #print(tail)
  #input()
  client.close()
  pass

