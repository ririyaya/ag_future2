#!D:\vnstudio


import requests
import time
import winsound
import sys
import pyaudio
import wave
list=[0,0,0,0,0, 0,0,0,0,0, 0,0]
var=1
chunk = 1024
def getvol():
 r=requests.get('http://futsse.eastmoney.com/static/118_AGTD_qt')
 a=r.json()['qt']
 vol=a['vol']
 utime=a['utime']
 return vol,utime

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
 
while var==1:
 for i in range(12):
  time.sleep(4.92)
  list[i]=getvol()[0]
  if i<11 and (list[i]-list[i+1])>30000:
   audio()
   print((list[i]-list[i+1]))
  elif (list[11]-list[0])>30000:
   print((list[11]-list[0]))
   audio()

input()
   
