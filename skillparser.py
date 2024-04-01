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
    return tech_check(text)
    

def linkedin_single(website, technologies):
    dr = webdriver.Chrome()
    dr.get(website)
    time.sleep(1)
    soup = BeautifulSoup(dr.page_source, 'lxml')
    listing = soup.findAll("div", {"class": "show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden"})
    text = listing[0].get_text()
    return tech_check(text, technologies)

def load_technologies(filepath):
    """
    Load technology keywords from a file into a set.
    """
    with open(filepath, 'r') as file:
        # Assuming each technology is quoted and separated by commas
        technologies = file.read().split(',')
        # Remove quotes and strip whitespace
        technologies = [tech.strip().strip('"') for tech in technologies if tech.strip()]
    return set(technologies)

def tech_check(text, technologies):
    """
    Check for the presence of technology-related keywords in text.
    """
    # Normalize the text
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
    words = text.split()  # Split text into words
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [w for w in words if not w in stop_words]
    # Check each word against the set of technology keywords
    found_technologies = {word for word in words if word in technologies}
    
    return list(found_technologies)

def main():
    # Path to the file containing common technologies
    filepath = "./common_technologies.txt"  # Update this to the actual path

    # Load technologies from the file
    technologies = load_technologies(filepath)
    
    # Check the example text for technology keywords
    text = linkedin_single('https://www.linkedin.com/jobs/view/3865660254', technologies)
    print("Found technologies:", text)

if __name__ == '__main__':
    main()