#!D:\vnstudio

import requests
import time
import winsound
import sys
import pyaudio
import wave

list=[0,0]
a=0
b=0
chunk = 1024
def getvol():
 r=requests.get('http://futsse.eastmoney.com/static/118_AGTD_qt')
 a=r.json()['qt']
 vol=a['vol']
 #utime=a['utime']
 p=a['p']
 return vol,p #,utime

def sum(list):
 total = 0
 for ele in range(0, len(list)): 
  total = total + list[ele] 
 return total

def audio():
 wf = wave.open(r'D:/22.wav', 'rb')
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
 StyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
 return StyleTime
 
def fwrite(a):
 f=open('D://log.txt','a')
 f.write(a+'\r')
 f.close()

 


 
while 1==1:
 try:
  for i in range(2):
   time.sleep(4.48)
   list[i]=getvol()[0]
   #b=a
   a=abs(list[1]-list[0])
   
   if a>20000:#or (a+b)>30000:
    audio()
    print(a)
    #fwrite(now())
 except Exception:
  print(e)
  pass
   
'''
while 1==1:
 for i in range(2):
  time.sleep(4.92)
  list[i]=getvol()[0]
  if (list[1]-list[0])>20000 or (list[0]-list[1])>20000:
   audio()
   print(abs(list[1]-list[0]),now())
   fwrite(now())
 '''

