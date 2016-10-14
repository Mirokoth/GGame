import json

from pytube import YouTube
import config
from bs4 import BeautifulSoup
import urllib
import requests


gApi = config.gAPI
YouURL = config.uChannel
downloadLocation = config.dllocal
ftype = config.ftype
fquality = config.fquality

parsed = json.load(open('searched.JSON'))

with urllib.request.urlopen(YouURL) as url:
    channel = url.read()

soup = BeautifulSoup(channel, "html.parser")
soup = soup.find_all('a', {'href': lambda L: L and L.startswith('/watch')})

count = 0
for vidID in soup:
    vidID = str(vidID).split('/watch?v=')
    vidID = str(vidID[1]).split('">')
    if vidID[0] in str(parsed):
        pass
    else:
        if 'title' in vidID[0]:
            pass
        else:
            vidID = vidID[0]
            count += 1
            SearchURL = str('https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part=contentDetails'.format(vidID, gApi))
            response =  requests.get(SearchURL)
            response = response.text
            data = json.loads(response)
            data = data['items'][0]
            vidLeng = str(data['contentDetails']['duration']).split('PT')
            vidLeng = str(vidLeng[1]).split('M')
            if 'H' in str(vidLeng[0]):
                vidLeng = '60'
            if 'S' in str(vidLeng[0]):
                vidLeng = '1'
            vidLeng = int(vidLeng[0])
            if vidLeng >= 20:
                print('{} Minutes - Must be a full episode, downloading... this will take a while'.format(vidLeng))
                getVid = YouTube('http://www.youtube.com/watch?v={}'.format(vidID))
                video = getVid.get(ftype, fquality)
                video.download(downloadLocation)
                print('Fin')
            else:
                print('Epsiode only {} minutes long. Not a full episode'.format(vidLeng))
            parsed.append(vidID)
with open('searched.json', 'w') as database:
    json.dump(parsed, database)
    database.close()
