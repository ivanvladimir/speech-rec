#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Live sphinx 
# ----------------------------------------------------------------------
# Ivan V. Meza
# 2014/IIMAS, México
# ----------------------------------------------------------------------
# live_sphinx.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------

# Audio libraries
import pyaudio
import wave
import audioop

# Turning on audio
audio = pyaudio.PyAudio()

# Status of audio
status = {
    'recording': False,
    'activity': False,
    'buffer': [],
    'prevScores': [30 for i in range(30)],
    'T': 0.0,
    'on': False,
    'warmed': 0,
    'nwarming': 15,
    'detected': 0,
    'file': False
}


def getScore(data):
    rms = audioop.rms(data, 2)
    return rms / 3

def callback(in_data, frame_count, time_info, status_):
    global status
    if status['warmed'] < status['nwarming']:
        status['prevScores'].pop(0)
        status['prevScores'].append(getScore(in_data))
        status['T'] = sum(status['prevScores'])*1.0/30*3
        status['warmed']+=1 
        return (in_data,pyaudio.paContinue)
   
    if status['on']:
        score = getScore(in_data)
        if score > status['T']:
            status['buffer'].append(in_data)
            status['detected']=1
        else:
            if status['detected']>0:
                if status['detected']<status['nlistening']:
                    status['buffer'].append(in_data)
                    status['detected']+=1
                else:
                    # GRABAR INF
                     wf = wave.open('voz.wav', 'w')
                     wf.setnchannels(1)
                     wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                     wf.setframerate(16000)
                     wf.writeframes(''.join(status['buffer']))
                     wf.close
                     status['detected']=0
                     status['warmed']=0
                     status['buffer']=[]
                     status['file']=True
             
    return (in_data,pyaudio.paContinue)
     
def getInDevices():
    devices=[]
    for i in range(audio.get_device_count()):
        info=audio.get_device_info_by_index(i)
        try:
            if info['maxInputChannels']>0:
                devices.append((i,info['name']))
        except KeyError:
            pass
    return devices



def getDeviceInfo(device=None):
    if not device:
        info=audio.get_default_input_device_info()
    else:
        info=audio.get_device_info_by_index(device)
    return info


def connect(info,samplerate=16000,warmingtime=1,
                            size_buffer=1024,listeningtime=.1):
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=samplerate,
        input_device_index=info['index'],
        input=True,
        stream_callback=callback,
        frames_per_buffer=size_buffer
    )
    status['nwarming']=samplerate/size_buffer*warmingtime
    status['nlistening']=samplerate/size_buffer*listeningtime
    status['on']=True
    return stream


    
