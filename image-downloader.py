import os
import json 
import requests 
from bs4 import BeautifulSoup 

GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}


i=0
SAVE_FOLDER = 'test' # ganti jdi nama foldernya
filename_tosave = "box" # ganti jdi nama file
dir = "C:/Users/Darren/OneDrive/Pictures/"+SAVE_FOLDER+'/' # ganti directorynya


def main():
    if not os.path.exists(dir):
        print("Making Directory")
        os.makedirs(dir)
    print("Directory exists")
    download_images()

def download_images():
    data = input('What are you looking for? ')
    while True:
        try:
            limit = int(input('How many images do you want to download? '))
            if limit > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
    
    print('Start searching...')
   
    searchurl = GOOGLE_IMAGE + 'q=' + data
    print(searchurl)
    
    response = requests.get(searchurl, headers=usr_agent)
    html = response.text
   
    soup = BeautifulSoup(html, 'html.parser')
   
    i = len(os.listdir(dir))
    print(f"Starting from image number: {i}")
   
    downloaded = 0
    for link in soup.find_all('img'):
        if downloaded >= limit:
            break
        
        src = link.get('src')
        if not src or not src.startswith('http'):
            continue
        
        try:
            response = requests.get(src)
            response.raise_for_status()
            
            imagename = os.path.join(dir, f"{filename_tosave}{i+1}.jpg")
            with open(imagename, 'wb') as file:
                file.write(response.content)
            
            print(f"Downloaded: {imagename}")
            i += 1
            downloaded += 1
        except requests.RequestException as e:
            print(f"Error downloading {src}: {e}")
    
    print(f'Done Downloading. {downloaded} images downloaded.')

if __name__ == '__main__':
    main()