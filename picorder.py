import vlc
import sys
import time

def main():

    # Create instance of VLC and force window to be top level
    Instance = vlc.Instance(['--video-on-top'])

    # Create media player object
    player = Instance.media_player_new()

    # Set media player to fullscreen
    player.set_fullscreen(True)

    # Set path to video to be played
    Media = Instance.media_new("/home/terry/Downloads/Creature from the Black Lagoon (1954).m4v")

    # Give the media player object the video to be played
    player.set_media(Media)

    # Play video
    player.play()

    # Wait for 10 seconds
    time.sleep(10)

    # Set media player to default screen size
    player.set_fullscreen(False)

    # Wait for enter key press
    str = ""
    while str == "":
        str = sys.stdin.read(1)
        pass   

    # Once enter key is pressed, pause video
    player.pause()

    # Wait for 5 seconds
    time.sleep(5)

    # Seek to next chapter in video
    player.next_chapter()

    # Play video
    player.play()

    # Wait for 10 seconds
    time.sleep(10)

    # Seek to previous chapter in video
    player.previous_chapter()

    # Wait for 10 seconds
    time.sleep(10)    

    # Stop video and exit program
    player.stop() 

if __name__ == '__main__':
    main()