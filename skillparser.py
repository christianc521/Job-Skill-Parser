from bs4 import BeautifulSoup # For HTML parsing
from selenium import webdriver #
import requests
import re # Regular expressions
import time
from nltk.corpus import stopwords

def indeed_single(website):
    dr = webdriver.Chrome()
    website = "https://www.indeed.com/viewjob?cmp=Gravity-Tech-Inc&t=Java+Developer&jk=4df18ab5154953fa&q=software+developer&xpse=SoAU67I3CIxXXiQ37J0LbzkdCdPP&xkcb=SoDU67M3CIxYwDyRR50IbzkdCdPP&vjs=3"
    dr.get(website)
    soup = BeautifulSoup(dr.page_source, 'lxml')
    listing = soup.find(type="application/ld+json")
    text = listing.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out 
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') 

    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    except:
        print("An exception occurred")
    text = text.decode('utf-8')
    text = re.sub("[^a-zA-Z.+3]"," ", text)
    text = text.lower().split()
    stop_words = set(stopwords.words("english"))
    text = [w for w in text if not w in stop_words]
    text = list(set(text))

    hasPython = hasJava = hasCPlus = False

    for word in text:
        if word == 'python':
            hasPython = True
        if word == 'java':
            hasJava = True
        if word == 'c++':
            hasCPlus = True

    return("requires C++: ", hasCPlus, " requires Java: ", hasJava, " requires Python: ", hasPython)

def linkedin_single(website):
    dr = webdriver.Chrome()
    dr.get(website)
    time.sleep(1)
    soup = BeautifulSoup(dr.page_source, 'lxml')
    # print(soup)
    # f = open("parse.txt", "a")
    # f.write(str(soup))
    # f.close()
    listing = soup.findAll("div", {"class": "show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden"})
    text = listing[0].get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out 
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') 

    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    except:
        print("An exception occurred")
    text = text.decode('utf-8')
    text = re.sub("[^a-zA-Z.+3]"," ", text)
    text = text.lower().split()
    stop_words = set(stopwords.words("english"))
    text = [w for w in text if not w in stop_words]
    text = list(set(text))

    hasPython = hasJava = hasCPlus = False

    for word in text:
        if word == 'python':
            hasPython = True
        if word == 'java':
            hasJava = True
        if word == 'c++':
            hasCPlus = True
    print("requires C++: ", hasCPlus, " requires Java: ", hasJava, " requires Python: ", hasPython)
    return("requires C++: ", hasCPlus, " requires Java: ", hasJava, " requires Python: ", hasPython)


linkedin_single("https://www.linkedin.com/jobs/view/3860332134")