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
    # quits browser
    browser.quit()

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
    #quits browser
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
    mars_html = mars_table.to_html(header=False, index=False, classes=['table-striped', 'table-bordered'])

    return mars_html

def sphere():
    '''Scrape Mars Hemispheres'''
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

    # shrink list of text to only image links
    texts = []
    for i in range(8):
        if (i % 2) == 1:
            texts.append(links_list[i].text.strip())

    images = []

    # loop over the text list
    for text in texts:
        # clicks on the button that has that text (the image)
        browser.links.find_by_partial_text(text).click()
        
        # makes soup out of that new page
        html_temp = browser.html
        soup_temp = bs(html_temp, 'html.parser')
        
        # get href link of the sample button that leads to full image
        image_url = soup_temp.find('a', text='Sample')['href']
        # i had to paste url together this way because when i would click
        # on the button it would open a tab and the browser would stay on 
        # the same page, this way i can tell the browser to go to this new page.
        full_url = url + image_url
        browser.visit(full_url)
        
        # make soup out of new page
        html_temp = browser.html
        soup_temp = bs(html_temp, 'html.parser')
        
        # append full image url to list
        images.append(soup_temp.find('img')['src'])
        
        # sends back to original browser url
        url = 'https://marshemispheres.com/'
        browser.visit(url)

        # creates soup of that browser
        html = browser.html
        soup = bs(html, 'html.parser')
        
    # quits browser
    browser.quit()

    # making dict out of text list and images list
    mars = []
    for i in range(4):
        mars.append({'title':texts[i], 'img_url':images[i]})

    return mars


def scrape():
    '''My scraping tool'''

    # scraping Nasa Mars News
    title, teaser = news()
    
    # Scraping Mars Space Images
    url = space()

    # Scrape Mars Facts
    html = facts()

    # Scraping Mars Hemispheres
    hemi = sphere()

    # stuffing everything into a dictionary for easy storage later on
    mars = {
        'article_title': title, 'article_teaser': teaser, 'feature_url': url,
        'table': html, 'hemispheres': hemi
    }

    return mars
