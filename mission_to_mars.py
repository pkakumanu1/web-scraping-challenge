from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time



def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return(Browser('chrome', **executable_path, headless=False))


def scrape():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)
    html =browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title =soup.find('ul',class_='item_list').find('li',class_='slide').find('div',class_='content_title').find('a').text
    news_p =soup.find('li',class_='slide').find('div',class_='article_teaser_body').text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    imgtag = soup.find('div',class_='fancybox-inner fancybox-skin fancybox-dark-skin fancybox-dark-skin-open').find('img')['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+ imgtag
    
    

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find('div',class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o').find('div',class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').find('span',class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Description','Values']
    df_html = df.to_html(index=False)
    print(df_html)

    HempList = ['Cerberus Hemisphere Enhanced',
                'Schiaparelli Hemisphere Enhanced',
                'Syrtis Major Hemisphere Enhanced',
                'Valles Marineris Hemisphere Enhanced']
    hemisphere_image_urls = []
    for x in range(0, 4):
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        browser.click_link_by_partial_text(HempList[x])
        time.sleep(5)
        browser.click_link_by_partial_text('Open')
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        imgurl = soup.find('div',class_='wide-image-wrapper').find_all('img')[1]['src']
        hemisphere_image_urls.append({'title': HempList[x], 'img_url' :'https://astrogeology.usgs.gov' +imgurl})

        


    return({'news_title':news_title,
        'news_p':news_p,
        'featured_image_url':featured_image_url,
        'mars_weather':mars_weather,
        'table':df_html,
        'hemisphere_image_urls': hemisphere_image_urls})


#print(scrape())

