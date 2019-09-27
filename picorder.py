#!/usr/bin/env python3

"""Picorder - a Raspberry Pi-based tricorder

Required installs on Ubuntu:

sudo apt install vlc
sudo apt install python3-pip
pip3 install python-vlc
sudo apt install python3-rpi.gpio

Written by Terry Howald
terry.howald@gmail.com
"""

import RPi.GPIO as GPIO
import time
import vlc

GPIO_BOARD_PIN_12 = 12
GPIO_BOARD_PIN_16 = 16

class VideoPlayer:
    
    # Constructor
    def __init__(self):
        
        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_BOARD_PIN_12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_BOARD_PIN_16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        # Add event for button push
        GPIO.add_event_detect(GPIO_BOARD_PIN_12, GPIO.RISING, callback=self.NextChapter_Callback) 
        GPIO.add_event_detect(GPIO_BOARD_PIN_16, GPIO.RISING, callback=self.PrevChapter_Callback)    
        
        # Create instance of VLC and force window to be top level
        Instance = vlc.Instance(['--video-on-top'])
        #Instance = vlc.Instance()        

        # Create media player object
        self.player = Instance.media_player_new()

        # Set media player to fullscreen
        self.player.set_fullscreen(True)

        # Set path to video to be played
        Media = Instance.media_new("/home/pi/Desktop/Phantom of the Opera (1943).m4v")

        # Give the media player object the video to be played
        self.player.set_media(Media)
        

    def SetupGPIO(self):
        pass
        
    def SetupVideoPlayer(self):
        pass
        
    def Play(self):
        self.player.play()
        
    def Stop(self):
        self.player.stop()
        
    def NextChapter(self):
        self.player.next_chapter()
        
    def PrevChapter(self):
        self.player.previous_chapter()
        
    def NextChapter_Callback(self, channel):
        GPIO.remove_event_detect(GPIO_BOARD_PIN_12)
        print("Button was pushed!")
        
        # Seek to next chapter in video
        self.NextChapter()
        
        time.sleep(0.25)
        GPIO.add_event_detect(GPIO_BOARD_PIN_12, GPIO.RISING, callback=self.NextChapter_Callback)  
        
    def PrevChapter_Callback(self, channel):
        GPIO.remove_event_detect(GPIO_BOARD_PIN_16)
        print("Button was pushed!")
        
        # Seek to next chapter in video
        self.PrevChapter()
        
        time.sleep(0.25)
        GPIO.add_event_detect(GPIO_BOARD_PIN_16, GPIO.RISING, callback=self.PrevChapter_Callback) 
    
    # Destructor    
    def __del__(self):
        GPIO.cleanup()

def main():
    videoplayer = VideoPlayer()
    
    videoplayer.Play()
   
    # Wait for 10 seconds
    #time.sleep(10)

    # Set media player to default screen size
    #player.set_fullscreen(False)    
    
    # Wait for Enter press
    message = input("Press enter to quit\n\n")
    
    # Stop video and exit program
    videoplayer.Stop() 

if __name__ == '__main__':
    main()
