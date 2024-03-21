import requests
import bs4
import time
import smtplib

url='https://www.smithsonianmag.com/category/smart-news/'
request=requests.get(url)
content=request.text
soup1=bs4.BeautifulSoup(content,"lxml")

raws=[]
article_names=[]
article_links=[]
article_dates=[]
#c
months={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
date=time.localtime()
raws=soup1.select('.article-list-text')

for i in raws:
    
    tag= i.select('a')[0]['href']
    
    if tag[:4]=='/tag':
        tag= i.select('a')[1]['href']

    name=i.select('h3')[0].getText()
    time=i.select('time')[0].getText()
    
    time=time.split(',')
    month=time[0].split()[0]
    day=time[0].split()[1]
    
    if months[month]==date.tm_mon and int(day)>=date.tm_mday-2:
        
        article_names.append(name.strip())
        article_links.append(tag)
        article_dates.append(' - '+month+' '+day)
    

msg='Subject: newsmail \n'
for i in range(0,len(article_names)):
    msg+= article_names[i]+' '+article_dates[i]+'\nhttps://www.smithsonianmag.com/'+article_links[i]+'\n\n'

email=input("enter your email: ")
key=input("enter your app password: ")
smtp_object=smtplib.SMTP('smtp.gmail.com',587)
smtp_object.ehlo()
smtp_object.starttls()
smtp_object.login(email,key)
from_email=email
c='y'
while c!='n':
    to_email=input("enter email to send to: ")
    smtp_object.sendmail(from_email,to_email,msg)
    c=input("enter 'n' to stop or any other key to continue: ")