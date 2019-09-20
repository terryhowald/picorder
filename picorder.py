import vlc
import sys
import time

def main():
    print("Launch VLC\n")

    Instance = vlc.Instance(['--video-on-top'])
    player = Instance.media_player_new()
    player.set_fullscreen(True)

    Media = Instance.media_new("/home/terry/Downloads/Creature from the Black Lagoon (1954).m4v")
    player.set_media(Media)

    player.play()

    str = ""
    while str == "":
        str = sys.stdin.read(1)
        pass   

    player.pause()

    time.sleep(5)

    player.next_chapter()

    player.play()

    time.sleep(5)

    player.previous_chapter()

    #player.play()    

    time.sleep(5)

    player.stop() 

if __name__ == '__main__':
    main()