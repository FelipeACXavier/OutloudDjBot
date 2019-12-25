from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions

import csv
import time
import argparse
import signal, os, sys

WINDOW_SIZE = "1920,1080"

webdriverPath = "Add webdriver path"

def parseNames():
    nameslist = []
    with open("namescsv.csv") as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            nameslist.append(row[1])

    return nameslist

def parseSongs():
    songlist = []
    artistlist = []
    with open("songs.csv") as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if row[0] != "x":
                print("Added " + str(row[0]) + " to list")
                songlist.append(row[0])
                artistlist.append(row[1])

    return songlist, artistlist

def startBrowser(website):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    driver = webdriver.Chrome(executable_path=webdriverPath, chrome_options=chrome_options)
    driver.get(website)
    time.sleep(3)
    return driver

def setNames(nameInput, howmany):
    names = []
    for i in range(howmany):
        name = nameInput + str(i);
        names.append(name)
    return names

def createUser(driver, userid):
    form = driver.find_element_by_id("screenname")
    form.send_keys(userid)
    time.sleep(1)
    form.send_keys(Keys.ENTER)
    time.sleep(1)

def search(driver, song, artist):
    toSearch = artist + " " + song
    btn = driver.find_element_by_id("open-search").click()
    time.sleep(2)
    form = driver.find_element_by_id("spotify-search")
    form.send_keys(toSearch)
    time.sleep(1)
    form.send_keys(Keys.ENTER)
    time.sleep(3)
    selectSong(driver, song)

def selectSong(driver, song):
    toSearch = "//div[@id='search-results']/div[@data-title='" + str(song) + "']"
    name = driver.find_element(By.XPATH, toSearch)
    time.sleep(1)
    name.click()
    time.sleep(2)

def findSong(driver, desiredSong):
    # cycle through songs in playlist
    songs = driver.find_elements(By.XPATH, "//div[@id='playlist']/div")
    for song in songs:
        # Get song id
        songId = song.get_attribute('id')
        # Create path to search
        toSearch = "//div[@id='playlist']/div[@id='" + str(songId) + "']/div[@class='song-info']/h2[text()]"
        # Find name
        name = driver.find_element(By.XPATH, toSearch).text
        # print(name + " " + desiredSong)
        if name == desiredSong:
            time.sleep(1)
            print(">>>> " + desiredSong + " found! <<<<")
            return str(songId)

    return None

def upVote(driver, songId):
    time.sleep(1)
    toSearch = "//div[@id='playlist']/div[@id='" + str(songId) + "']/div[@class='vote-up-icon pull-right']/a"
    name = driver.find_element(By.XPATH, toSearch)
    name.click()
    time.sleep(1)

def handler(signum, frame):
    print('\nSignal handler called with signal', signum)
    raise KeyboardInterrupt

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--song', help="song title")
parser.add_argument('-a', '--artist', help="artist name")
parser.add_argument('-w', '--website', help="website", required=True)
parser.add_argument('-n', '--votes', help="how many votes to add", default=1)
parser.add_argument('-c', '--create', help="if is a new song or to upvote", default=0)
args = parser.parse_args()

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGSEGV, handler)
signal.signal(signal.SIGABRT, handler)

# selenium.find_element_by_name("submit").click()
if __name__ == "__main__":
    if args.song is not None:
        songName = args.song
    if args.artist is not None:
        artist = args.artist
    if args.website is not None:
        web = args.website
    if args.votes is not None:
        votes = int(args.votes)

    upvote = False
    automate = False
    if args.create == str(0):
        print ("Add song mode selected")
    elif args.create == str(1):
        print ("Upvote mode selected")
        upvote = True
    else:
        print("Automatic mode selected")
        automate = True

    names = parseNames()
    songs, artists = parseSongs()

    if automate == True:
        print(">>>>>>>> Start <<<<<<<<")

        for i in range(len(songs)):
            # Add song to playlist
            noSong = False
            totalTime = time.time()
            try:
                start = time.time()
                print("Adding " + str(songs[i]) + " by " + artists[i])
                browser = startBrowser(web)
                createUser(browser, "Mark with a K")
                search(browser, songs[i], artists[i])
                browser.quit()
                print("Time to add: " + str(time.time() - start))
            except:
                noSong = True
                pass
            if noSong == False: # Only performs if song was added
                print("Added: " + str(songs[i]) + " by " + artists[i])
                upvotes = 0
                for index in range(0, votes, 2):
                    try:
                        start = time.time()
                        browser1 = startBrowser(web)
                        browser2 = startBrowser(web)
                        createUser(browser1, names[index])
                        createUser(browser2, names[index+1])
                        if index == 0:
                            songid = findSong(browser1, songs[i])
                            songid1 = findSong(browser2, songs[i])
                        upVote(browser1, songid)
                        upVote(browser2, songid1)
                        browser1.quit()
                        browser2.quit()
                        print("Time to upvote twice: " + str(time.time() - start))
                        upvotes = upvotes + 2
                        print("Votes: " + str(upvotes))
                    except Exception as ex:
                        if (type(ex).__name__ == "KeyboardInterrupt"):
                            print("CTRL+C")
                            break
                            sys.exit()
                        else:
                            pass

            else:
                try:
                    print("Could not add song: " + str(songs[i]))
                except Exception as ex:
                    if (type(ex).__name__ == "KeyboardInterrupt"):
                        print("CTRL+C")
                        break
                        sys.exit()
                    else:
                        pass
            print("Total time for " + str(songs[i]) + " : " + str(time.time() - totalTime))
    # Only Upvote
    elif upvote == True:
        # add n votes
        songId = ''
        songId1 = ''
        for index in range(0, votes, 3):
            try:
                print("Start")
                start = time.time()
                browser = startBrowser(web)
                browser1 = startBrowser(web)
                createUser(browser, names[index])
                createUser(browser1, names[index+1])
                if index == 0:
                    songid = findSong(browser, songName)
                    songid1 = findSong(browser1, songName)
                upVote(browser, songid)
                upVote(browser1, songid1)
                browser.quit()
                browser1.quit()
                print("Time to upvote twice: " + str(time.time() - start))
            except Exception as ex:
                print type(ex).__name__
                if (type(ex).__name__ == "KeyboardInterrupt"):
                    print("CTRL+C")
                    sys.exit()
                else:
                    print (str(ex))
    # Only add song
    else:
        start = time.time()
        browser = startBrowser(web)
        createUser(browser, "Mark with a K")
        search(browser, songName, artist)
        browser.quit()
        print("Time to add: " + str(time.time() - start))
