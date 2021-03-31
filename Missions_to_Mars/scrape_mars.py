# dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def news():
    '''Scrapes Nasa Mars News'''
    # open browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # mars news url
    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)
    # making beautiful soup
    html = browser.html
    soup = bs(html, 'html.parser')
    # pulling first title and teaser
    title = soup.find('div', class_='content_title').text
    teaser = soup.find('div', class_='article_teaser_body').text
    return (title, teaser)

def space():
    '''Scrapes Mars Space Images'''
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # sends browser to url
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    # creates soup of browser
    html = browser.html
    soup = bs(html, 'html.parser')
    # anchor
    anchor = soup.find('a', class_='showimg fancybox-thumbs')
    # half the featured_image_url
    image_url = anchor['href']

    browser.quit()

    # joining urls
    featured_image_url = url + image_url

    return featured_image_url

def facts():
    '''Scrape Mars Facts'''
    # url
    url = 'https://galaxyfacts-mars.com/'
    # read all tables on page into df's
    tables = pd.read_html(url)
    # pick out table i want 
    mars_table = tables[1]
    # convert to html format
    mars_html = mars_table.to_html(header=False, index=False)

    return mars_html

def sphere():
    '''Scrape the Spheres'''
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # sends browser to url
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # creates soup of browser
    html = browser.html
    soup = bs(html, 'html.parser')

    # gather list of links
    links_list = soup.find_all('a', 'itemLink product-item')

    # shrink list of text
    texts = []
    for i in range(8):
        if (i % 2) == 1:
            texts.append(links_list[i].text.strip())

    images = []

    for text in texts:
        browser.links.find_by_partial_text(text).click()
        
        html_temp = browser.html
        soup_temp = bs(html_temp, 'html.parser')
        
        image_url = soup_temp.find('a', text='Sample')['href']
        full_url = url + image_url
        browser.visit(full_url)
        
        html_temp = browser.html
        soup_temp = bs(html_temp, 'html.parser')
        
        images.append(soup_temp.find('img')['src'])
        
        # sends browser to url
        url = 'https://marshemispheres.com/'
        browser.visit(url)

        # creates soup of browser
        html = browser.html
        soup = bs(html, 'html.parser')
        
    browser.quit()

    mars = []
    for i in range(4):
        mars.append({'title':texts[i], 'img_url':images[i]})

    return mars


def scrape():
    '''My scraping tool'''

    title, teaser = news()
    
    url = space()

    html = facts()

    hemi = sphere()

    mars = {
        'title': title, 'teaser': teaser, 'feature_url': url,
        'table': html, 'hemispheres': hemi
    }

    return mars


print(scrape())