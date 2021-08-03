#!/usr/bin/env python
# coding: utf-8

# Dependencies
import pandas as pd
from splinter import Browser
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results_li = soup.find('li', class_='slide')
    title = results_li.find('div', class_='content_title').text
    print(title)

    news_p = results_li.find('div', class_='article_teaser_body').text
    print(news_p)

    #JPL Mars Space Images - Featured Image
    space_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    space_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(space_image_url)

    html=browser.html
    soup=BeautifulSoup(html,"html.parser")
    img_url=soup.find_all('a')[2]
    img_url=soup.find('a', class_='showimg')['href']
    featured_image_url = space_url+img_url


    #Mars Facts
    url = 'http://space-facts.com/mars/'
    mars_facts_table = pd.read_html(url)

    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")
    MarsFacts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(MarsFacts_url)

    html = browser.html

    table = pd.read_html(html)

    facts_df = table[0]
    facts_df.columns =['Mars - Earth Comparison', 'Mars', 'Earth']

    mars_facts_html_table = facts_df.to_html(index=False)

    # Mars Hemispheres
    MarsHemisphereImage_url = 'https://marshemispheres.com/'
    browser.visit(MarsHemisphereImage_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_divs = soup.find_all('div', class_="item")
    hemisphere_image_data = [] #

    for hemisphere in range(len(hemisphere_divs)):
        hem_link = browser.find_by_css("a.itemLink h3")
        hem_link[hemisphere].click()
        time.sleep(1)
        
        img_detail_html = browser.html
        imagesoup = BeautifulSoup(img_detail_html, 'html.parser')

        base_url = 'https://marshemispheres.com/'    
        hem_url = imagesoup.find('img', class_="wide-image")['src'] 
        img_url = base_url + hem_url
        img_title = browser.find_by_css('.title').text
        
        hemisphere_image_data.append({"title": img_title,"img_url": img_url})
        browser.back()
        
    browser.quit()

    scraped_data = {
        "featured_image_url": featured_image_url,
        "mars_facts_html": mars_facts_html_table,
        "hemisphere_image_data": hemisphere_image_data
    }
    print(scraped_data)

    return scraped_data
