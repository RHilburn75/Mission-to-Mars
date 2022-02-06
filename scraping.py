from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Initiate headless driver for deployment
def scrape_all():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    omg_urls_titles = mars_hemis(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
       
    # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    #url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    url = 'https://spaceimages=mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None
    
        

    # Use the base url to create an absolute url
    #img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the fact's table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    #return df.to_html(classes="table table-striped")
    return df.to_html()

    #def hemisphere(browser):
def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    hemisphere_image_urls = []
    
    #imgs_links = browser.find_by_css("a.product-item h3")
    #for x in range(len(imgs_links)):
        #hemisphere = {}
        ## Find the elements to click link
        #browser.find_by_css("a.product-item h3")[x].click()
    ## Find sample image link
        #sample_img = browser.find_link_by_text("Sample").first
        #hemisphere['img_url'] = sample_img['href']
    ## get hemisphere title
        #hemisphere[title] = browser.find_by_css("h2.title").text
    ## Add objects to hemisphere_img_urls list
        #hemisphere_image_urls.append(hemisphere)
    ## Go back
        #browser.back
    for hemis in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hemis].click()
        html = browser.html
        hemi_soup = soup(html,'html.parser')
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('l1').a.get('href')
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
              
    return hemisphere_image_Urls
if __name__ == "__main__":

    # If running as a script, print scraped data
    print(scrape_all())
