from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
from bs4 import BeautifulSoup
from datetime import datetime

# Setup Variables
term = "2247"
classes = ["CSC 123", "CSC 321"]
classid = ["9876", "1234"]

# Function to scrape data from specific <td> tags within <tr> tags that have <tbody> as parent
def scrape_table_data(url):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    chromedriver_path = os.path.join(current_directory, 'chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    
    try:
        # Wait until the element with class "dataTables_empty" is not found
        WebDriverWait(driver, 10).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'dataTables_empty')))
    except TimeoutException:
        driver.quit()
        return
    
    # Parse HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tbody_tags = soup.find_all('tbody')
    
    for tbody in tbody_tags:
        # Find all <tr> tags within the current <tbody> tag
        tr_tags = tbody.find_all('tr')
        
        # Iterate through each <tr> tag
        for tr in tr_tags:
            if tr.find_all('td')[9].string.strip() == "0" and tr.find_all('td')[8].find_all()[1].string.strip() == "0":
                continue
            if not classid or tr.find_all('td')[3].string.strip() in classid:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), end=' ')
                th_tag = tbody.find('th')
                if th_tag:
                    # Extract text from the first element inside <th> tag
                    th_text = th_tag.find_all(string=True)[0].strip()
                    print(th_text, end=' ')
                
                td_tags = tr.find_all('td')
                if len(td_tags) >= 9:
                    # Print the content of the 2nd, 4th, 6th, and 9th <td> tags
                    print(td_tags[1].string.strip(), td_tags[3].string.strip(), end=' ')  # Print the content of the 2nd and 4th <td> tags with a space separator
                    sixth_td_span = td_tags[5].find('span')  # Find the <span> tag within the 6th <td> tag
                    if sixth_td_span:  # If <span> tag exists
                        span_texts = sixth_td_span.find_all(string=True)  # Get all string nodes within <span>
                        if len(span_texts) >= 2:  # Ensure at least two string nodes exist
                            print(span_texts[1].strip(), end=' ')  # Print the second string node within <span> with a space separator
                    sixth_td_div = td_tags[5].find('div')  # Find the <div> tag within the 6th <td> tag
                    if sixth_td_div:  # If <div> tag exists
                        div_texts = sixth_td_div.find_all(string=True)  # Get all string nodes within <div>
                        for i, text in enumerate(div_texts):
                            print(text.strip(), end=' ')  # Print string node with leading/trailing whitespaces stripped
                    
                    ninth_td_content = td_tags[8].find_all()[0].string.strip()
                    if len(ninth_td_content) > 20:
                        ninth_td_content = ninth_td_content[17:]  # Trim first 17 characters
                    print(ninth_td_content)
    driver.quit()

# Construct the URL for each class and scrape data
while True:
    for class_name in classes:
        # Split the class input by space to separate subject and class number
        subject, category_number = class_name.split(' ')
        
        # Example usage
        url_template = 'https://webapps.sfsu.edu/public/classservices/classsearch/results?term={}&classCategory=REG&subject={}&categoryNumber={}'
        url = url_template.format(term, subject, category_number)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        scrape_table_data(url)
    time.sleep(60)  # Sleep for 60 seconds before scraping again