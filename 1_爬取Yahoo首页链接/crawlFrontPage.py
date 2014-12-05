#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":
    
    foxProfile = webdriver.FirefoxProfile('/home/blade091/ConfigData')
    driver = webdriver.Firefox(foxProfile)
#     driver.set_page_load_timeout(20)
        
    driver.get('http://news.yahoo.com/')
    webpage = driver.find_element_by_xpath('/html')
    for i in range(1000):
        webpage.send_keys(Keys.PAGE_DOWN)
    
    file = open('FrontPageURL - 20141008.txt', 'a')
    picUrls = driver.find_elements_by_xpath('//a[@class = "yom-lead-featured-image"]')
    for picUrl in picUrls:
        pic_url = picUrl.get_attribute('href')
        file.write(pic_url + '\n')  
    
    Urls = driver.find_elements_by_xpath('//div[@class = "body-wrap"]//h3/a')
    for Url in Urls:
        url = Url.get_attribute('href')
        if url.find('http://news.yahoo.com/'):
            pass
        else:
            file.write(url + '\n') 
    file.close()         
    driver.close()