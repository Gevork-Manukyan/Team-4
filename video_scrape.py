# Ridge Tejuco
# CSUN 
# Team 4
# January 30, 2021

import vlc  # to display video source in vlc media player
import requests # to download html page of sign savvy
import time
from bs4 import BeautifulSoup # to parse html page into video source

tb_text = ["Hello","Night","Plane","Dance","LOL"] # test bench data

# Setup play back of videos for later use
vlc_instance = vlc.Instance()
vlc_media_list = vlc_instance.media_list_new()
position = 0

# Find the URL of each token and add to playlists
for ii in tb_text:
   
    # Web scraping algorithm
    url = "https://www.signingsavvy.com/search/"
    url += ii
    # e.g. https://www.signingsavvy.com/search/Hello

    # download page and parse the html using BS4
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')

    # Look for the video element or search result
    video = soup.video
    if video is not None:
        # Check if a video was found
        video_src = video.source['src']
        # Add video source to Media Playlists
        source_url = "https://www.signingsavvy.com/" + video_src
        vlc_media_list.insert_media(vlc_instance.media_new_location(source_url),position)
        print(video_src)
    else:
        # Check if there is search results
        result = soup.find('div', class_ = 'search_results')
        if result is None:
            print('Could not find any video on token: ' + ii)
            #TODO: Display the Finger spelling
        else:
            print(result.li.a['href'])
            search_url = "https://www.signingsavvy.com/" + result.li.a['href']
            search_page = requests.get(search_url)
            search_soup = BeautifulSoup(search_page.content,'html.parser')
            search_video = search_soup.video
            if search_video is not None:
                # Look for video from search results
                sv_src = search_video.source['src']
                # Add video to Media Playlists
                sv_url = "https://www.signingsavvy.com/" + sv_src
                vlc_media_list.insert_media(vlc_instance.media_new_location(sv_url),position)
                print(sv_src)
            else:
                print('Could not find any video on token: ' + ii)
                #TODO: Display the Finger spelling
    position += 1



# Create the VLAN player    
player = vlc_instance.media_list_player_new()

# Set the playlists
player.set_media_list(vlc_media_list)

# Start the video playback
player.play()

print(player.get_state())
# Check if the media player is finished every second
# 6 is finished state of the media player
Ended = 6
while player.get_state() != Ended:
    time.sleep(1)
print(player.get_state())


