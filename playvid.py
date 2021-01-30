
# importing vlc module 
import vlc
import time
url = "https://www.handspeak.com/word/a/abate2.mp4"
# creating vlc media player object 
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
media = vlc_instance.media_new_location(url)
player.set_media(media)
# start playing video 
player.play()
time.sleep(4)