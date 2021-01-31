import vlc  # to display video source in vlc media player
import requests # to download html page of sign savvy
import time
from bs4 import BeautifulSoup # to parse html page into video source

class AslRenderer:

    def __init__(self):
        # Setup play back of videos for later use
        self.vlc_instance = vlc.Instance("--video-title-show --video-title-timeout 1 --sub-source marq --verbose -1")

        # Create the VLAN player    
        self.player = self.vlc_instance.media_player_new()

        # Set caption position
        self.player.video_set_marquee_int(4, 4) 

    def renderASL(self, tb_text):
        
        def play_media(vlc_player,media,video_text):
            time_left = True
            Ended = 6
            while time_left:
                if vlc_player.get_state() == Ended or vlc_player.get_state() == 0:
                    time_left = False
                else:
                    time.sleep(0.01)
            # NOTE: vlc_player is passed argument as seen above ^
            vlc_player.set_media(media)
            vlc_player.play()
            vlc_player.video_set_marquee_string(vlc.VideoMarqueeOption.Text,video_text)

        def getElement(this_url):
            # download page and parse the html using BS4
            page = requests.get(this_url)
            # html parse
            soup = BeautifulSoup(page.content,'html.parser')
            # find and return a video tag
            return soup

        def getWebMedia(this_url,this_video,vInstance):
            # Check if a video was found
            src = this_video.source['src']
            # Concat relative path to domain
            new_url = this_url + src
            print("Found Web Video: " +new_url)
            # Pull media from URL for vlc instance
            new_media = vInstance.media_new_location(new_url)
            return new_media

        SigningSavvy = "https://www.signingsavvy.com/"
        # Find the URL of each token and add to playlists
        for ii in tb_text:
        
            # Web scraping algorithm
            url = "https://www.signingsavvy.com/search/"
            url += ii
            # e.g. https://www.signingsavvy.com/search/Hello

            new_soup = getElement(url)
            video = new_soup.video
            if video is not None:
                # If video is found, pass to vlc media locator, then play media
                vlc_media = getWebMedia(SigningSavvy,video,self.vlc_instance)
                play_media(self.player,vlc_media,ii)
            else:
                # Check if there is search results
                result = new_soup.find('div', class_ = 'search_results')
                if result is None:
                    print('Could not find any video on token: ' + ii)
                    #TODO: Display the Finger spelling
                else:
                    # Find the URL redirection of the first search result in list
                    search_url = "https://www.signingsavvy.com/" + result.li.a['href']
                    print("Found Search Result: " + search_url)
                    search_video = getElement(search_url).video
                    if search_video is not None:
                        # Look for video from search results
                        vlc_media = getWebMedia(SigningSavvy,search_video,self.vlc_instance)
                        play_media(self.player,vlc_media,ii)
                    else:
                        print('Could not find any video on token: ' + ii)
                        #TODO: Display the Finger spelling

        print(self.player.get_state())
        # Check if the media player is finished every second
        # 6 is finished state of the media player
        Ended = 6
        while self.player.get_state() != Ended:
            time.sleep(1)
        print(self.player.get_state())

