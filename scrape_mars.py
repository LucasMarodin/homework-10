# coding: utf-8
# In[1]:
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time

# In[2]:

### NASA Mars News

# In[3]:

def init_browser():
    executable_path = {"executable_path": "\SeleniumDrivers\chromedriver"}
    return Browser("chrome", **executable_path, headless=True)


# In[4]:

def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}

    #visiting the page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # In[5]:
    # Scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # In[6]:
    news_title = soup.find("div",class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    news_date = soup.find("div", class_="list_date").text
    print(f"Title: {news_title}")
    print(f"Paragraph: {news_paragraph}")

    # Add the news date, title and summary to the dictionary
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_paragraph

    # In[7]:

    ### JPL Mars Space Images - Featured Image

    # In[8]:

    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
    browser.visit(url_image)

    # In[9]:

    # Scrape the browser into soup and use soup to find the image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url
    # Use the requests library to download and save the image from the `img_url` above
    import requests
    import shutil
    response = requests.get(img_url, stream=True)
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    # Display the image with IPython.display
    from IPython.display import Image
    Image(url='img.jpg')

    # Add the featured image url to the dictionary
    mars_data["featured_image_url"] = featured_image_url

    # In[10]:

    ### Mars Weather

    # In[11]:

    #get mars weather's latest tweet from the website
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    # In[12]:

    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    #temp = soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)
    #temp

    # Add the weather to the dictionary
    mars_data["mars_weather"] = mars_weather

    # In[13]:

    ### Mars Facts

    # In[14]:

    url_facts = "https://space-facts.com/mars/"

    # In[15]:

    table = pd.read_html(url_facts)
    table[0]

    # In[16]:

    df_mars_facts = table[0]
    df_mars_facts.columns = ["Parameter", "Values"]
    df_mars_facts.set_index(["Parameter"])

    # In[17]:

    mars_html_table = df_mars_facts.to_html()
    mars_html_table = mars_html_table.replace("\n", "")
    mars_html_table

    # Add the Mars facts table to the dictionary
    mars_data["mars_table"] = mars_html_table

    # In[18]:

    ### Mars Hemispheres

    # In[19]:

    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    # In[20]:

    # Use splinter to loop through the 4 images and load them into a dictionary
    import time
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_hemis=[]

    # In[21]:


    # loop through the four tags and load the data to the dictionary

    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = bs(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = mars_hemis
    # Return the dictionary
    return mars_data
