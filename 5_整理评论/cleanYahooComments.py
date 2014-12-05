#encoding=utf-8
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

from lxml import html

if __name__== "__main__":
    
    files = os.listdir('/media/blade091/新加卷/Data/politics/')
    for fileName in files:
	print fileName
        filePath = '/media/blade091/新加卷/Data/politics/' + fileName
        HTML = open(filePath).read()
        HTML = HTML.replace('comment_id','id')
        HTML = HTML.replace('data-cmt','id')
        root = html.fromstring(HTML)
        
        '写入标题、正文'
        newFilePath = '/media/blade091/新加卷/Data/newPolitics/' + fileName
        readFile = open(filePath)
        writeFile = open(newFilePath,'a')
        for line in readFile.xreadlines():
            if cmp(line, '</article>\n') == 0:
                writeFile.write(line)
                break
            else:
                writeFile.write(line)
        
        comments = root.xpath('//comments')
        for comment in comments:
            commentText = html.tostring(comment, pretty_print=True, encoding='utf-8')
            commentRoot = html.fromstring(commentText)
            
            '评论相关'
            commentIDs = commentRoot.xpath('//li[@class="js-item comment  "]')#.get('id')
            userIDs = commentRoot.xpath('//li[@class="js-item comment  "]//span[@class="int profile-link"]')#text
            timestamps = commentRoot.xpath('//li[@class="js-item comment  "]//span[@class="comment-timestamp"]')#text
            upcounts = commentRoot.xpath('//li[@class="js-item comment  "]//div[@id="up-vote-box"]//span')#text
            downcounts = commentRoot.xpath('//li[@class="js-item comment  "]//div[@id="down-vote-box"]//span')#text
            contents = commentRoot.xpath('//li[@class="js-item comment  "]//p[@class="comment-content"]')#text  
            '回复相关'
            replies = commentRoot.xpath('//replies')
#             reply_commentIDs = commentRoot.xpath('//li[@class="js-item reply"]')#.get('id')
#             reply_userIDs = commentRoot.xpath('//li[@class="js-item reply"]//span[@class="int profile-link"]')#text
#             reply_timestamps = commentRoot.xpath('//li[@class="js-item reply"]//span[@class="comment-timestamp"]')#text
#             reply_upcounts = commentRoot.xpath('//li[@class="js-item reply"]//div[@id="up-vote-box"]//span')#text
#             reply_downcounts = commentRoot.xpath('//li[@class="js-item reply"]//div[@id="down-vote-box"]//span')#text
#             reply_contents = commentRoot.xpath('//li[@class="js-item reply"]//p[@class="comment-content"]')#text  
#             print replies
#            print '\n'
            for commentID,userID,timestamp,upcount,downcount,content in zip(commentIDs,userIDs,timestamps,upcounts,downcounts,contents):
#                 print commentID.get('id'),userID.text,timestamp.text,upcount.text,downcount.text,content.text
#                 for reply_commentID,reply_userID,reply_timestamp,reply_upcount,reply_downcount,reply_content in zip(reply_commentIDs,reply_userIDs,reply_timestamps,reply_upcounts,reply_downcounts,reply_contents):
#                     print reply_commentID.get('class'),reply_userID.text,reply_timestamp.text,reply_upcount.text,reply_downcount.text,reply_content.text
                writeFile.write('<comment commentID=\"' + commentID.get('id') + '\"' + ' userID=\"' + userID.text + '\"' + \
                                ' timestamp=\"' + timestamp.text + \
                    '\"' + ' upcount=\"' + upcount.text + '\"' + ' downcount=\"' + downcount.text + '\"' + '>' \
                    + '\n' + content.text + '\n')
                for reply in replies:
                    if cmp(commentID.get('id'),reply.get('id')) == 0:
                        replyText = html.tostring(reply, pretty_print=True, encoding='utf-8')
                        replyRoot = html.fromstring(replyText)
#                         reply_commentIDs = replyRoot.xpath('//li[@class="js-item reply"]')#.get('id')
                        reply_userIDs = replyRoot.xpath\
                        ('//li[@class="js-item reply"]//span[@class="int profile-link"]')#text
                        reply_timestamps = replyRoot.xpath\
                        ('//li[@class="js-item reply"]//span[@class="comment-timestamp"]')#text
                        reply_upcounts = replyRoot.xpath\
                        ('//li[@class="js-item reply"]//div[@id="up-vote-box"]//span')#text
                        reply_downcounts = replyRoot.xpath\
                        ('//li[@class="js-item reply"]//div[@id="down-vote-box"]//span')#text
                        reply_contents = replyRoot.xpath\
                        ('//li[@class="js-item reply"]//p[@class="comment-content"]')#text  
                        for reply_userID,reply_timestamp,reply_upcount,reply_downcount,reply_content in zip(reply_userIDs,reply_timestamps,reply_upcounts,reply_downcounts,reply_contents):
#                             print reply_userID.text,reply_timestamp.text,reply_upcount.text,reply_downcount.text,reply_content.text
                            writeFile.write('<reply userID =\"' + reply_userID.text + '\"' + ' timestamp=\"' + \
                                timestamp.text + '\"' + ' upcount=\"' + reply_upcount.text + '\"' + ' downcount=\"' + \
                                downcount.text + '\"' + '>' + '\n' + reply_content.text + '\n' + '</reply>' + '\n')
                    else:
                        pass
                writeFile.write('</comment>' + '\n')
        readFile.close()
        writeFile.close()       
                
                
