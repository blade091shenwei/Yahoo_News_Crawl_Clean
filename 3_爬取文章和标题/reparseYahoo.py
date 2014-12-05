#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

from selenium import webdriver

if __name__== "__main__":
    
    foxProfile = webdriver.FirefoxProfile('/home/blade091/ConfigData')
    driver = webdriver.Firefox(foxProfile)
    driver.set_page_load_timeout(20) 
#     allURLs = ['http://news.yahoo.com/sarah-palin-play-jersey-223500001--politics.html', 'http://news.yahoo.com/egypt-el-sissi-wins-election-landslide-032532611.html']
    readfile = open('allURLs', 'r')
    allURLs = []
    for url in readfile.xreadlines():
        newURL = url.replace('\n','')
        allURLs.append(newURL) 
    readfile.close()
    
    for URL in allURLs:
        time.sleep(10) 
        try:
            driver.get(URL)
        except:
            continue
        
        try:
            article = driver.find_element_by_id("mediacontentstory")
            contentID = article.get_attribute("data-uuid")
#             print 'contentID:', contentID
        except:
            continue
        
        try:
            Types = driver.find_element_by_id("mediacontentnavigation").find_elements_by_tag_name("a")
            typeName = 'None'
            for Type in Types:
                if cmp("selected Fw-b", Type.get_attribute("class")) == 0:
                    typeName = Type.text
                    break
                else:
                    continue
#             print 'Type:', typeName
        except:
            Type = 'None'
        
        try:
            title = article.find_element_by_class_name("headline").text
#             print 'title:', title
        except:
            title = 'None'
            
        try:
            author = article.find_element_by_class_name("fn").text
#             print 'author:', author
        except:
            author = 'None'
            
        try:
            date = article.find_element_by_tag_name("abbr").text
#             print 'date:', date
        except:
            date = 'None'
        
        try:
            contentsText = []
            contents = article.find_elements_by_tag_name("p")
            for content in contents:
                contentsText.append(content.text)
#                 print 'content:', content.text
        except:
            contentsText = ['None']
        
        '去除一个叫做View photo的字符串'
        if cmp(contentsText[0], "View photo") == 0:
            del contentsText[0]
           
        '将文章的相关信息写入结构化文档中'
        titleName = title.replace('/','')  
        titleName = titleName.replace('\\','')
        titleName = titleName.replace(':','')
        titleName = titleName.replace('*','')
        titleName = titleName.replace('?','')
        titleName = titleName.replace('>', '')
        titleName = titleName.replace('<', '')
        titleName = titleName.replace('|', '')
        titleName = titleName.replace('\"', '')
        print titleName
        
        writeFile = open('allArticles/' + typeName + '-' + titleName,'a')
        writeFile.write('<title type=\"' + typeName + '\" ')
        writeFile.write('author=\"' + author + '\" ')
        writeFile.write('date=\"' + date + '\" ')
        writeFile.write('contentID=\"' + contentID + '\"' + '>\n')
        writeFile.write(title + '\n' + '</title>' + '\n')
        writeFile.write('<article>\n')
        for contentText in contentsText:
            writeFile.write(contentText + '\n')
        writeFile.write('</article>\n')
        writeFile.close()
        
    driver.close()
        
        
        
    