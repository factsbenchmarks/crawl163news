import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json

def get_comment_vote(news):
    key = re.search('/(\w+).html',news).group(1)
    comment_url = 'http://sdk.comment.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}'.format(key)
    comment_res = requests.get(comment_url)
    jd = json.loads(comment_res.text)
    comment = jd['tcount']
    vote = jd['cmtAgainst'] + jd['cmtVote'] + jd['rcount']
    return (comment,vote)

def crawl(news):
    try:
        result = {}
        res = requests.get(news)
        res.encoding = 'gbk'
        soup = BeautifulSoup(res.text,'html.parser')
        title = soup.select('.post_content_main h1')[0].text
        date1 = soup.select('.post_time_source')[0].contents[0].lstrip().rstrip('\u3000来源: ')
        date = datetime.strptime(date1,'%Y-%m-%d %H:%M:%S')
        source = soup.select('.cDGray span')[0].contents[1].lstrip(' 本文来源：')
        author = soup.select('.cDGray span')[1].text.lstrip('责任编辑：')
        comment,vote = get_comment_vote(news)
        result['title'] = title
        result['date'] = date
        result['source'] = source
        result['author'] = author
        result['comment'] = comment
        result['vote'] = vote
        return result
    except:
        pass


NEWS = 'http://news.163.com/'
res = requests.get(NEWS)
res.encoding= 'gbk'
soup = BeautifulSoup(res.text,'html.parser')
for item in soup.select('a'):
    if item.get('href') and item['href'].startswith('http://news.163.com/18/'):
        print(item['href'])
        result = crawl(item['href'])
        print(result)