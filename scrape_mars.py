#!/usr/bin/env python
# coding: utf-8

# Dependencies
import pandas as pd
from splinter import Browser
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup 
from selenium import webdriver
from flask import Flask, render_template, redirect


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# ## Step 1 - Scraping: 

# ### NASA Mars News

    ### NASA Mars News ###
    # Visting url througher splinter browser
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(1)

    # Using Beatiful soup to parse the html in the designated url
    html = browser.html
    soup = BeautifulSoup(html, "html5")

    # Get the date, title, and content text in the latest news
    news_date = soup.find('div', class_='list_date').text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    ############################################
    ### JPL Mars Space Images - Featured Image ###

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    browser.is_element_present_by_text("FULL IMAGE", 2)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(1)

    # Using Beatiful soup to parse the html in the designated url
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Get the image url for the JPL Deatures space image
    featured_image_tag = soup.find("img", class_="fancybox-image")["src"]
    featured_image_url = ('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + str(featured_image_tag ))
    
    ############################################
    ### Mars Facts ###

    # Using the read_html function in Pandas to automatically scrape tabular data from designated url
    url = 'http://space-facts.com/mars/'
    mars_facts_table = pd.read_html(url)

    # Slicing dataframes to use normal indexing
    mars_facts_df = mars_facts_table[0]
    mars_facts_df.columns = ['Measurement', 'Unit']

    # Using to_html method to generate HTML tables from mars_facts_df 
    mars_facts_html_table = mars_facts_df.to_html(index=False)

    ############################################
    ### Mars Hemispheres ###

    ## Cerberus Hemisphere Enhanced ##
   
    # Visting url througher splinter browser
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    time.sleep(1)
    # Using Beatiful soup to parse the html in the designated url
    html = browser.html
    soup = BeautifulSoup(html, "html5")
    # Getting image url
    cerberus = soup.find('img', class_='wide-image')['src']
    cerberus_url = ('https://astrogeology.usgs.gov/' + str(cerberus)) 
    # Getting Hemisphere Name 
    cerberus_title = soup.find('h2', class_='title').text

    ## Schiaparelli Hemisphere Enhanced ##
   
    # Visting url througher splinter browser
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    time.sleep(1)
    # Using Beatiful soup to parse the html in the designated url
    html = browser.html
    soup = BeautifulSoup(html, "html5")
    # Getting image url
    schiaparelli = soup.find('img', class_='wide-image')['src']
    schiaparelli_url = ('https://astrogeology.usgs.gov/' + str(schiaparelli)) 
    # Getting Hemisphere Name
    schiaparelli_title = soup.find('h2', class_='title').text

    ## Syrtis Major Hemisphere Enhanced ##
   
    # Visting url througher splinter browser
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    time.sleep(1)
    # Using Beatiful soup to parse the html in the designated url
    html = browser.html
    soup = BeautifulSoup(html, "html5")
    # Getting image url
    syrtis_major = soup.find('img', class_='wide-image')['src']
    syrtis_major_url = ('https://astrogeology.usgs.gov/' + str(syrtis_major)) 
    # Getting Hemisphere Name 
    syrtis_major_title = soup.find('h2', class_='title').text

    ## Valles Marineris Hemisphere Enhanced ##
   
    # Visting url througher splinter browser
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    time.sleep(1)
    # Using Beatiful soup to parse the html in the designated url
    html = browser.html
    soup = BeautifulSoup(html, "html5")
    # Getting image url
    valles_marineris = soup.find('img', class_='wide-image')['src']
    valles_marineris_url = ('https://astrogeology.usgs.gov/' + str(valles_marineris)) 
    # Getting Hemisphere Name 
    valles_marineris_title = soup.find('h2', class_='title').text

    # Creating dictionary for each hemisphere title and image url
    cerberus_dict ={
        'title': cerberus_title,
        'img_url': cerberus_url
    }
    schiaparelli_dict ={
        'title': schiaparelli_title,
        'img_url': schiaparelli_url
    }
    syrtis_major_dict ={
        'title': syrtis_major_title,
        'img_url': syrtis_major_url
    }
    valles_marineris_dict ={
        'title': valles_marineris_title,
        'img_url': valles_marineris_url
    }

    # Creating a list to store all of the hemisphere dictionaries
    hemisphere_image_urls= []
    hemisphere_image_urls.append(cerberus_dict)
    hemisphere_image_urls.append(schiaparelli_dict)
    hemisphere_image_urls.append(syrtis_major_dict)
    hemisphere_image_urls.append(valles_marineris_dict)

    ############################################
    ### Store data in a dictionary ###
    planet_data = {
        ### NASA Mars News ###
        "news_date": news_date,
        "news_title": news_title,
        "news_p": news_p,

        ### Featured Image ###
        "featured_image_url": featured_image_url,

        ### Mars Facts ###
        "mars_facts_html_table": mars_facts_html_table,  

        ## Mars Hemispheres ##
        "hemisphere_image_urls": hemisphere_image_urls
        }


    # Close the browser after scraping
    browser.quit()

    # Return results
    return planet_data
