# Import Dependencies
import os
import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# Defining scrape & dictionary
def scrape():
    browser = init_browser()
    mars_dict ={}


    ## NASA Mars News
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    ## JPL Mars Space Images - Featured Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + image
    
    ## Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    table = pd.read_html(mars_facts_url)
    df = table[0]
    df = df.rename(columns={0:"Mars", 1: "Facts"})
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    
    ## Mars Hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    hemisphere_image_urls = []
    hemispheres = soup.find_all('div', class_='item')
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        partial_img_url = hemisphere.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    ## Mars
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict
