from bs4 import BeautifulSoup # For HTML parsing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import requests
import re # Regular expressions
import time
from nltk.corpus import stopwords


def load_linkedin(technologies):
    dr = webdriver.Chrome() # open Chrome
    dr.implicitly_wait(10) # wait for Chrome to load

    dr.get(f'https://www.linkedin.com/jobs/search?keywords=software%2Bdeveloper&location=United%2BStates&geoId=103644278')
    time.sleep(5)
    # dr.find_element(By.XPATH, f'//button[@aria-label="Page 1"]').click()
    jobs_lists = dr.find_element(By.CLASS_NAME, 'jobs-search__results-list') #here we create a list with jobs
    jobs = jobs_lists.find_elements(By.CLASS_NAME, 'base-search-card')#here we select each job to count
    ## waiting load
    time.sleep(1)
    ## the loop below is for the algorithm to click exactly on the number of jobs that is showing in list
    ## in order to avoid errors that will stop the automation
    dr.maximize_window() # For maximizing window
    dr.implicitly_wait(10) # gives an implicit wait for 20 seconds
    for job in jobs[0:5]:
        try:
            # Move to the job element to ensure it's visible
            dr.execute_script("arguments[0].scrollIntoView();", job)

            # Click on the job posting
            job.click()
            time.sleep(5)
            dr.implicitly_wait(10)

            # Click on show more
            show_more = dr.find_element(By.CLASS_NAME, 'show-more-less-html__button')
            show_more.click()
            time.sleep(2)

            job_title = dr.find_element(By.CLASS_NAME, 'job-search-card--active').find_element(By.CLASS_NAME, 'base-search-card__title').text
            print('Job title: ' + job_title)
            job_link = dr.find_element(By.CLASS_NAME, 'job-search-card--active').find_element(By.TAG_NAME, "a").get_attribute("href")
            print(job_link)
            job_description = dr.find_element(By.CLASS_NAME, "show-more-less-html__markup").text
            tech_check(job_description, technologies)
        except Exception as e:
            print(f"An error occurred: {e}")

    return

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
    time.sleep(1)
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
    print(found_technologies)
    print('\n')
    return list(found_technologies)



def main():
    # Path to the file containing common technologies
    filepath = "./common_technologies.txt"  # Update this to the actual path

    # Load technologies from the file
    technologies = load_technologies(filepath)
    
    # Check the example text for technology keywords
    load_linkedin(technologies)

if __name__ == '__main__':
    main()