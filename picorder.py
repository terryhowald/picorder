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
import os

GPIO_BOARD_PIN_12 = 12
GPIO_BOARD_PIN_16 = 16
GPIO_BOARD_PIN_18 = 18
VIDEOS_DIRECTORY = "/home/pi/Desktop/videos"

class VideoPlayer:
    
    # Constructor
    def __init__(self):
        
        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_BOARD_PIN_12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_BOARD_PIN_16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(GPIO_BOARD_PIN_18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)        
        
        # Add event for button push
        GPIO.add_event_detect(GPIO_BOARD_PIN_12, GPIO.RISING, callback=self.NextChapter_Callback) 
        GPIO.add_event_detect(GPIO_BOARD_PIN_16, GPIO.RISING, callback=self.PrevChapter_Callback)   
        GPIO.add_event_detect(GPIO_BOARD_PIN_18, GPIO.RISING, callback=self.NextEpisode_Callback) 
        
        # Create instance of VLC and force window to be top level
        self.instance = vlc.Instance(['--video-on-top'])
        #Instance = vlc.Instance()        

        # Create media player object
        self.player = self.instance.media_player_new()

        # Set media player to fullscreen
        self.player.set_fullscreen(True)
        
        # Get list of video files
        self.file_list = os.listdir(VIDEOS_DIRECTORY)

        # Set path to first video to be played
        self.video_played = 0
        full_path = VIDEOS_DIRECTORY + "/" + self.file_list[self.video_played]
        media = self.instance.media_new(full_path)

        # Give the media player object the video to be played
        self.player.set_media(media)
        

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
        
    def NextEpisode_Callback(self, channel):
        GPIO.remove_event_detect(GPIO_BOARD_PIN_18)
        print("Button was pushed!")
        
        # Stop video being played
        #self.player.pause()
        
        # Get next video to be played
        self.video_played = self.video_played + 1
        if self.video_played >= len(self.file_list):
            self.video_played = 0
        full_path = VIDEOS_DIRECTORY + "/" + self.file_list[self.video_played]
        media = self.instance.media_new(full_path)

        # Give the media player object the video to be played
        self.player.set_media(media)
        
        #time.sleep(0.25)
        GPIO.add_event_detect(GPIO_BOARD_PIN_18, GPIO.RISING, callback=self.NextEpisode_Callback) 
        
        self.Play()
    
    # Destructor    
    def __del__(self):
        GPIO.cleanup()

def main():
    videoplayer = VideoPlayer()
    
    videoplayer.Play()
     
    # Wait for Enter press
    message = input("Press enter to quit\n\n")
    
    # Stop video and exit program
    videoplayer.Stop() 

if __name__ == '__main__':
    main()
