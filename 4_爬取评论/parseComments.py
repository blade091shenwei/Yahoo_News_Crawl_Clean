#encoding=utf-8
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
from lxml import etree
from selenium import webdriver

def readFile(file, decoding):
    html = ''
    try:
        html = open(file).read().decode(decoding)
    except:
        print 'can not read'
        pass
    return html

def extract(file, decoding, xpath):
    html = readFile(file, decoding)
    tree = etree.HTML(html)
    return tree.xpath(xpath)

if __name__== "__main__":
    
    foxProfile = webdriver.FirefoxProfile('/home/blade091/ConfigData')
    driver = webdriver.Firefox(foxProfile)
#     driver.set_page_load_timeout(20) 
    count = 0
    '对每个文件夹中的文件'
    files = os.listdir('/home/blade091/yahooNews数据与程序整理/4_爬取评论/copy/')
    for fileName in files:
        count = count + 1
	print count
	print fileName
        '数据初始化'
        offset = 0
        pageNumber = 0
        '提取contentID并生成评论的URL'
        filePath = '/home/blade091/yahooNews数据与程序整理/4_爬取评论/copy/' + fileName
        contentID = extract(filePath, 'utf-8', "//title/@contentid")[0]
        
        comments = ''
        while cmp(comments,'{\"status\":200,\"error\":null,\"message\":\"\",\"commentList\":\"    <li class=\\\"list-error\\\"><div class=\\\"err\\\"><p>NO_COMMENTS<\\/p><\\/div><\\/li>\\n\",\"deeplink\":null,\"more\":null}') != 0:
            
            commentURLcontent_id = "http://news.yahoo.com/_xhr/contentcomments/get_comments/?content_id=" + contentID
            commentURLoffset = "&_device=full&count=10&sortBy=highestRated&isNext=true&offset=" + str(offset)
            commentURLpageNumber = "&pageNumber=" + str(pageNumber)
            commentURLrest = "&_media.modules.content_comments.switches._enable_view_others=1&_media.modules.content_comments.switches._enable_mutecommenter=1&enable_collapsed_comment=1"
            commentURL = commentURLcontent_id + commentURLoffset + commentURLpageNumber + commentURLrest
            
            time.sleep(5)
            
            try:
		driver.get(commentURL)
                comments = driver.find_element_by_xpath('//pre').text
                newComments = comments.replace('\\n','\n')
                newComments = newComments.replace('\\','')
#                 print comments
            except:
                print 'Exception - 1'
                continue
            
            writeComments = open('copy/' + fileName,'a')
            writeComments.write('<comments>\n')
            writeComments.write(newComments + '\n')
            writeComments.close()
            
            if comments.find('Expand Replies') < 0:
                #这一页的评论中没有回复
#                 print 'NO REPLIES'
                pass
            else:
#                 print 'HAVE REPLIES'
                commentIDExpress = re.compile(r'data-cmt=\\\".{50}\\')
                commentIDs_Attribute = commentIDExpress.findall(comments)
                commentIDs = []
                for commentID_Attribute in commentIDs_Attribute:
                    commentID = commentID_Attribute[11:61]
#                     print commentID
                    commentIDs.append(commentID)
                
                for commentID in commentIDs:
                    ReplyURL = "http://news.yahoo.com/_xhr/contentcomments/get_replies/?content_id=" + contentID + "&_device=full&comment_id=" + commentID + "&_media.modules.content_comments.switches._enable_view_others=1&_media.modules.content_comments.switches._enable_mutecommenter=1&enable_collapsed_comment=1"
                    time.sleep(5)
                    
                    try:
			driver.get(ReplyURL)
                        replies = driver.find_element_by_xpath('//pre')
                        if cmp(replies.text,'{\"status\":200,\"error\":null,\"message\":\"\",\"commentList\":\"    <li class=\\\"list-error\\\"><div class=\\\"err\\\"><p>NO_COMMENTS<\\/p><\\/div><\\/li>\\n\",\"deeplink\":null,\"more\":null}') == 0:
                            pass
                        else:
                            newReplies = replies.text.replace('\\n','\n')
                            newReplies = newReplies.replace('\\','')
                            writeReplies = open('copy/' + fileName, 'a')
                            writeReplies.write('<Replies comment_id=\"' + commentID + '\"' + '>\n')
                            writeReplies.write(newReplies + '\n')
                            writeReplies.write('</Replies>\n')
                            writeReplies.close() 
                    except:
                        print 'Exception - 2'
                        continue
            
            writeComments = open('copy/' + fileName,'a')
            writeComments.write('</comments>\n')
            writeComments.close()
                            
            offset += 10
            pageNumber += 1
            
    driver.close()
    
