#encoding=utf-8
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

if __name__== "__main__":
    
    '''
        整理爬取的url
        整理成不含重复的url的一个文件
    '''
    '读取文件所有文件里的url并存放到列表当中'
    files = os.listdir('/home/blade091/yahooNews数据与程序整理/2_所有链接整合成一个文件/N2_all_urls/')
    '将所有的url写入一个文件当中'
    urls = []
    flag = 1
    writeFile = open('allURLs', 'a')
    for fileName in files:
        filePath = '/home/blade091/yahooNews数据与程序整理/2_所有链接整合成一个文件/N2_all_urls/' + fileName
        file = open(filePath, 'r')
        for line in file.xreadlines():
            for url in urls:
                '如果是重复的url的话，flag就是0，不是的话就是1'
                if cmp(url, line) == 0:
                    flag = 0
                    break
                else:
                    flag = 1
                    continue 
            if flag == 0:
                continue 
            else:
                urls.append(line)
                writeFile.write(line)
    writeFile.close()

