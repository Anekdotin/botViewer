__author__ = 'edwin'

import argparse, os, time
import urlparse, random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

def getPeopleLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if 'profile/view?id=' in url:
                links.append(url)

    return links

def getJbLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/jobs' in url:
                links.append(url)

    return links


def ViewBot(browser):
    visited = {} # make sure u dont go to same person, hashs identifier
    pList = []
    count  = 0

    while True:
        time.sleep(random.uniform(3.5,15.0))
        page = BeautifulSoup(browser.page_source)
        people = getPeopleLinks(page)
        if people:
            for person in people:
                ID = getID(person)
                if ID not in visited:
                    pList.append(person)
                    visited[ID] = 1
        if pList: # if people to look at
            person = pList.pop()
            browser.get(person)
            count += 1

        else:# found people by jb pages
            jobs = getJbLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'http://www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'https://www.linkedin.com' + job
                browser.get(job)
            else:
                print "Bot lost"
                break
        print "[+] "+browser.title+" Visited \n ("+str(count) +str(len(pList))+") Visited/Queue"








def getID(url):

    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query)['id'][0]

def Main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("value", help="username")
        parser.add_argument("password", help="password")
        args = parser.parse_args()
    except Exception as e:
        print str(e)

    browser = webdriver.Firefox()
    browser.get("https://linkedin.com/uas/login")

    emailElement = browser.find_element_by_id("session_key-login")
    emailElement.send_keys(args.value)
    passElement = browser.find_element_by_id("session_password-login")
    passElement.send_keys(args.password)
    passElement.submit()
    os.system('clear')

    print '[+] Success! Logged in, bot starting!'
    ViewBot(browser)
    browser.close()

if __name__ == '__main__':
    Main()







