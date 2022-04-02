from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog,QApplication,QStackedWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

import sys

import serial
import wave
import numpy as np
import winsound
import convert
import bpm
import pyaudio
import porteur

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("untitled.ui",self)

        self.Button_onoff.setCheckable(True)
        self.Button_flash.setCheckable(True)
        self.Button_audio.setCheckable(True)        
        self.Button_fade.setCheckable(True)
        self.Button_smooth.setCheckable(True)
        self.Button_music.setCheckable(True)

        self.R.setText("R = "+str(self.Slider_R.value()))
        self.G.setText("G = "+str(self.Slider_G.value()))
        self.B.setText("B = "+str(self.Slider_B.value()))

        self.testonoff=True
        self.timer = QTimer(self)

        self.Slider_R.valueChanged.connect(self.do_action)
        self.Slider_G.valueChanged.connect(self.do_action)
        self.Slider_B.valueChanged.connect(self.do_action)

        self.Button_onoff.clicked.connect(self.do_onoff) 
        self.Button_flash.clicked.connect(self.do_flash)
        self.Button_audio.clicked.connect(self.do_audio)
        self.Button_fade.clicked.connect(self.do_fade)
        self.Button_smooth.clicked.connect(self.do_smooth)
        self.Button_music.clicked.connect(self.do_music)

    porteur.fn()
    port = porteur.inp
    print ("port : ",port)

    light=serial.Serial(port, baudrate=9600, timeout=.1)
    light.write(('255,w'+'\r\n').encode())

    def do_action(self):
        self.R.setGeometry(QtCore.QRect(60, 350, 101, 41))
        self.R.setWordWrap(True)
        self.R.setStyleSheet("color: rgb("+(str)(self.Slider_R.value())+",0,0)")
        self.R.setText("R = "+str(self.Slider_R.value()))

        self.G.setGeometry(QtCore.QRect(140, 360, 101, 21))
        self.G.setWordWrap(True)
        self.G.setStyleSheet("color: rgb(0,"+(str)(self.Slider_G.value())+",0)")
        self.G.setText("G = "+str(self.Slider_G.value()))

        self.B.setGeometry(QtCore.QRect(220, 360, 111, 21))
        self.B.setWordWrap(True)
        self.B.setStyleSheet("color: rgb(0,0,"+(str)(self.Slider_B.value())+")")
        self.B.setText("B = "+str(self.Slider_B.value()))
        
        self.Aerobotix.setStyleSheet("color: rgb("+(str)(self.Slider_R.value())+","+(str)(self.Slider_G.value())+","+(str)(self.Slider_B.value())+")")

        self.light.write((str(self.Slider_R.value())+'\r\n').encode()+(str(self.Slider_G.value())+'\r\n').encode()+(str(self.Slider_B.value())+'\r\n').encode())

    def do_onoff(self):
        if (self.testonoff==False):
            self.testonoff=True
            self.Button_flash.setEnabled(True)       
            self.Button_fade.setEnabled(True)
            self.Button_smooth.setEnabled(True)
            self.Button_audio.setEnabled(True)
            self.Button_music.setEnabled(True)

            self.Slider_R.setEnabled(True)
            self.Slider_G.setEnabled(True)
            self.Slider_B.setEnabled(True)

        else:
            self.testonoff=False
            self.Slider_R.setSliderPosition(0)
            self.Slider_G.setSliderPosition(0)
            self.Slider_B.setSliderPosition(0)

            try:
                winsound.PlaySound(None, winsound.SND_PURGE)
                self.timer.disconnect()
                convert.closeroot()
            except:
                None

            self.Slider_R.setEnabled(False)
            self.Slider_G.setEnabled(False)
            self.Slider_B.setEnabled(False)

            self.Button_flash.setEnabled(False)
            self.Button_audio.setEnabled(False)        
            self.Button_fade.setEnabled(False)
            self.Button_smooth.setEnabled(False)
            self.Button_music.setEnabled(False)
            
            self.Button_flash.setChecked(False)
            self.Button_audio.setChecked(False)
            self.Button_fade.setChecked(False)
            self.Button_smooth.setChecked(False)
            self.Button_music.setChecked(False)

    def do_flash(self):
        if (self.Button_flash.isChecked()):
            self.timer.timeout.connect(self.flash)
            self.timer.start(1000)

            self.Slider_R.setEnabled(False)
            self.Slider_G.setEnabled(False)
            self.Slider_B.setEnabled(False)
        
            self.Button_fade.setEnabled(False)
            self.Button_audio.setEnabled(False)
            self.Button_smooth.setEnabled(False)
            self.Button_music.setEnabled(False)

        else:
            self.timer.disconnect()
            self.Slider_R.setEnabled(True)
            self.Slider_G.setEnabled(True)
            self.Slider_B.setEnabled(True)

            self.Button_fade.setEnabled(True)
            self.Button_audio.setEnabled(True)
            self.Button_smooth.setEnabled(True)
            self.Button_music.setEnabled(True)

    def flash(self):
        if (self.Button_flash.isChecked()):
            if (self.Slider_R.value()==255):
                self.Slider_R.setSliderPosition(0)
                self.Slider_G.setSliderPosition(255)
                self.Slider_B.setSliderPosition(0)
                
            elif (self.Slider_G.value()==255):
                self.Slider_R.setSliderPosition(0)
                self.Slider_G.setSliderPosition(0)
                self.Slider_B.setSliderPosition(255)
                
            else:
                self.Slider_R.setSliderPosition(255)
                self.Slider_G.setSliderPosition(0)
                self.Slider_B.setSliderPosition(0)

            self.light.write((str(self.Slider_R.value())+'\r\n').encode()+(str(self.Slider_G.value())+'\r\n').encode()+(str(self.Slider_B.value())+'\r\n').encode())


    def do_smooth(self):
        if (self.Button_smooth.isChecked()):
            self.timer.timeout.connect(self.smooth)
            self.timer.start(1000)
            self.i=0
            self.Slider_R.setEnabled(False)
            self.Slider_G.setEnabled(False)
            self.Slider_B.setEnabled(False)

            self.Button_fade.setEnabled(False)
            self.Button_audio.setEnabled(False)
            self.Button_music.setEnabled(False)
            self.Button_flash.setEnabled(False)
            
        else:
            self.timer.disconnect()
            self.Slider_R.setEnabled(True)
            self.Slider_G.setEnabled(True)
            self.Slider_B.setEnabled(True)

            self.Button_fade.setEnabled(True)
            self.Button_audio.setEnabled(True)
            self.Button_music.setEnabled(True)
            self.Button_flash.setEnabled(True)
    #smooth cycle : red green blue yellow purple ice white
    colors_R=[255,0,0,255,100,0,255]
    colors_G=[0,255,0,255,0,255,255]
    colors_B=[0,0,255,0,255,255,255]
    def smooth(self):
        if (self.Button_smooth.isChecked()):
            self.i = (self.i+1) % 7
            self.Slider_R.setSliderPosition(self.colors_R[self.i])
            self.Slider_G.setSliderPosition(self.colors_G[self.i])
            self.Slider_B.setSliderPosition(self.colors_B[self.i])

            self.light.write((str(self.Slider_R.value())+'\r\n').encode()+(str(self.Slider_G.value())+'\r\n').encode()+(str(self.Slider_B.value())+'\r\n').encode())


    def do_fade(self):
        if (self.Button_fade.isChecked()):
            self.red=True
            self.green=False
            self.blue=False
            self.test=False
            self.Slider_R.setSliderPosition(0)
            self.Slider_G.setSliderPosition(0)
            self.Slider_B.setSliderPosition(0)
            self.timer.timeout.connect(self.fade)
            self.timer.start(100)

            self.Slider_R.setEnabled(False)
            self.Slider_G.setEnabled(False)
            self.Slider_B.setEnabled(False)

            self.Button_flash.setEnabled(False)
            self.Button_audio.setEnabled(False)
            self.Button_smooth.setEnabled(False)
            self.Button_music.setEnabled(False)
        else:
            self.timer.disconnect()
            self.Slider_R.setEnabled(True)
            self.Slider_G.setEnabled(True)
            self.Slider_B.setEnabled(True)

            self.Button_flash.setEnabled(True)
            self.Button_audio.setEnabled(True)
            self.Button_smooth.setEnabled(True)
            self.Button_music.setEnabled(True)

    def fade(self):
        if (self.Button_fade.isChecked()):
            #-------RED
            if self.red==True:
                if(self.Slider_R.value()>=255):
                    self.Slider_R.setSliderPosition(255)
                    self.test=True
                elif(self.Slider_R.value()<=0):
                    self.Slider_R.setSliderPosition(0)
                    self.test=False
                    #init
                    self.red=False
                    self.green=True
                    self.blue=False

                if (self.test==False):
                    self.Slider_R.setSliderPosition(self.Slider_R.value()+15)
                else:
                    self.Slider_R.setSliderPosition(self.Slider_R.value()-15)
            #--------GREEN
            elif self.green==True:
                if(self.Slider_G.value()>=255):
                    self.Slider_G.setSliderPosition(255)
                    self.test=True
                elif(self.Slider_G.value()<=0):
                    self.Slider_G.setSliderPosition(0)
                    self.test=False

                    #init
                    self.red=False
                    self.green=False
                    self.blue=True

                if (self.test==False):
                    self.Slider_G.setSliderPosition(self.Slider_G.value()+15)
                else:
                    self.Slider_G.setSliderPosition(self.Slider_G.value()-15)
            #--------BLUE
            elif self.blue==True:
                if(self.Slider_B.value()>=255):
                    self.Slider_B.setSliderPosition(255)
                    self.test=True

                elif(self.Slider_B.value()<=0):
                    self.Slider_B.setSliderPosition(0)
                    self.test=False

                    #init
                    self.red=True
                    self.green=False
                    self.blue=False

                if (self.test==False):
                    self.Slider_B.setSliderPosition(self.Slider_B.value()+15)
                else:
                    self.Slider_B.setSliderPosition(self.Slider_B.value()-15)

            self.light.write((str(self.Slider_R.value())+'\r\n').encode()+(str(self.Slider_G.value())+'\r\n').encode()+(str(self.Slider_B.value())+'\r\n').encode())


    CHUNK = 2**11
    RATE = 44100
    #old=0
    file='presets/samples/sample.wav'
    wf = wave.open(file, 'rb')
    #idk=[]
    test_yakra=True
    test_forsa=50

    def do_music(self):
        if (self.Button_music.isChecked()):
            print('Music_Reactive')
            self.i=0
            self.timer.timeout.connect(self.music)
            self.Slider_R.setSliderPosition(128)
            self.Slider_G.setSliderPosition(128)
            self.Slider_B.setSliderPosition(128)
            self.ps=True
            self.cmpl=False
            self.cmpl=convert.mp3()
            if (self.cmpl==True):
                # print(self.wf.getnchannels())
                # def callback(in_data, frame_count, time_info, status):
                #     data = self.wf.readframes(frame_count)
                #     return (data, pyaudio.paContinue)
                # self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                #             # channels=self.wf.getnchannels(),
                #             channels=1,
                #             rate=self.wf.getframerate(),
                #             input=True)
                #             #stream_callback=callback)
                self.beats=bpm.bpm_detect(self.file)
                self.tmp=60000/self.beats
                self.timer.start(self.tmp)
                self.Slider_R.setEnabled(False)
                self.Slider_G.setEnabled(False)
                self.Slider_B.setEnabled(False)

                self.Button_fade.setEnabled(False)
                self.Button_smooth.setEnabled(False)
                self.Button_audio.setEnabled(False)
                self.Button_flash.setEnabled(False)
            else:
                None

        else:
            try:
                self.timer.disconnect()
                self.stream.stop_stream()
                convert.closeroot()
            except:
                None
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.old=0
            self.cmpl=False
            #print(self.idk)
            self.Slider_R.setEnabled(True)
            self.Slider_G.setEnabled(True)
            self.Slider_B.setEnabled(True)

            self.Button_fade.setEnabled(True)
            self.Button_smooth.setEnabled(True)
            self.Button_audio.setEnabled(True)
            self.Button_flash.setEnabled(True)

    def music(self):
        if (self.Button_music.isChecked()):
            if (self.ps==True and self.cmpl==True):
                winsound.PlaySound(self.file, winsound.SND_ASYNC)
                self.ps=False

            if (self.cmpl==True):
                self.i = (self.i+1) % 7
                self.Slider_R.setSliderPosition(self.colors_R[self.i])
                self.Slider_G.setSliderPosition(self.colors_G[self.i])
                self.Slider_B.setSliderPosition(self.colors_B[self.i])

                #####################VARIATION TEMPO###########################
                data=np.frombuffer(self.wf.readframes(self.CHUNK),dtype=np.int16)
                peak = (np.average(np.abs(data))*2)
                print(peak)
                #khamem fel comparaison de peak avec le max d'une liste de peak, au lieu de 5000
                # if(peak>10000):
                #     self.tmp=30000/self.beats
                #     self.timer.disconnect()
                #     self.timer.timeout.connect(self.music)
                #     self.timer.start(self.tmp)
                # else:
                #     self.tmp=60000/self.beats
                #     self.timer.disconnect()
                #     self.timer.timeout.connect(self.music)
                #     self.timer.start(self.tmp)
                # if (data == b''):
                #     self.test_forsa-=1
                # if (self.test_forsa<=0):
                #     self.test_yakra=False(zid if self.test_yakra==True lfouk fel parametre mtaa if buttonisChecked())
            else:
                try:
                    self.stream.stop_stream()
                except:
                    None

            self.light.write((str(self.Slider_R.value())+'\r\n').encode()+(str(self.Slider_G.value())+'\r\n').encode()+(str(self.Slider_B.value())+'\r\n').encode())


    CHUNK = 2**11
    RATE = 44100
    old=0
    val=0
    p=pyaudio.PyAudio()

    def do_audio(self):
        if (self.Button_audio.isChecked()):
            print('Audio_Reactive')
            self.stream=self.p.open(format=pyaudio.paInt16,channels=1,rate=self.RATE,input=True,
                                    frames_per_buffer=self.CHUNK)
            self.old=0
            self.timer.timeout.connect(self.audio)
            self.timer.start(30)
            self.Slider_R.setEnabled(False)
            self.Slider_G.setEnabled(False)
            self.Slider_B.setEnabled(False)

            self.Button_fade.setEnabled(False)
            self.Button_music.setEnabled(False)
            self.Button_smooth.setEnabled(False)
            self.Button_flash.setEnabled(False)
            
        else:
            try:
                self.timer.disconnect()
            except:
                None
            try:
                self.stream.stop_stream()
            except:
                None
            self.Slider_R.setEnabled(True)
            self.Slider_G.setEnabled(True)
            self.Slider_B.setEnabled(True)

            self.Button_fade.setEnabled(True)
            self.Button_music.setEnabled(True)
            self.Button_smooth.setEnabled(True)
            self.Button_flash.setEnabled(True)

    def audio(self):
        if (self.Button_audio.isChecked()):
            data=np.frombuffer(self.stream.read(self.CHUNK),dtype=np.int16)
            avg=np.average(np.abs(data)*2)
            diff=avg-self.old
            print('diff :'+str(diff))

            def Gmap( x,  in_min,  in_max, out_min, out_max):
                return int((x - in_min) * (out_max - out_min) / (in_max - in_min ) + out_min)
            val=Gmap(diff,0,20000,0,255)

            print('val :'+str(val))
            print('---')

            if(val<50):
                self.Slider_R.setSliderPosition(self.Slider_R.value())
                self.Slider_G.setSliderPosition(self.Slider_G.value())
                self.Slider_B.setSliderPosition(self.Slider_B.value())

            elif(val<100):
                #red_tnakes
                if self.Slider_R.value()-val/4>=0:
                    self.Slider_R.setSliderPosition(self.Slider_R.value()-val/4)
                #green_tzid
                if self.Slider_G.value()+val>=255:
                    self.Slider_G.setSliderPosition(self.Slider_G.value()-val)
                else:
                    self.Slider_G.setSliderPosition(self.Slider_G.value()+val)
                #blue_tzid
                if self.Slider_B.value()+val/2<=255:
                    self.Slider_B.setSliderPosition(self.Slider_B.value()+val/2)
                else:
                    self.Slider_B.setSliderPosition(self.Slider_B.value()-val/2)

            elif(val>100):
                if self.Slider_R.value()+val<=255:
                    self.Slider_R.setSliderPosition(self.Slider_R.value()+val)
                #green_tzid
                if self.Slider_G.value()+val>=255:
                    self.Slider_G.setSliderPosition(self.Slider_G.value()-val)
                else:
                    self.Slider_G.setSliderPosition(self.Slider_G.value()+val)
                #blue_tzid
                if self.Slider_B.value()-val>=0:
                    self.Slider_B.setSliderPosition(self.Slider_B.value()-val)
            

            self.light.write((str(self.Slider_R.value())+'\r\n').encode()+(str(self.Slider_G.value())+'\r\n').encode()+(str(self.Slider_B.value())+'\r\n').encode())
            self.old=avg

        else:
            try:
                self.stream.stop_stream()
            except:
                None

#main
app = QApplication(sys.argv)
mainframe = MainScreen()

widget = QStackedWidget()
widget.addWidget(mainframe)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()

try:
    sys.exit(app.exec())
except:
    print("Exiting")