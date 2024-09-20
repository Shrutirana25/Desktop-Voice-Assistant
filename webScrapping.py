import webbrowser
import smtplib
import threading
from bs4 import BeautifulSoup
import requests


def openWebsite(url='https://www.google.com/'):
	webbrowser.open(url)

def latestNews(news=5):
	URL = 'https://indianexpress.com/latest-news/'
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')

	headlineLinks = []
	headlines = []

	divs = soup.find_all('div', {'class':'title'})

	count=0
	for div in divs:
		count += 1
		if count>news:
			break
		a_tag = div.find('a')
		headlineLinks.append(a_tag.attrs['href'])
		headlines.append(a_tag.text)

	return headlines,headlineLinks


import webbrowser
from youtubesearchpython import VideosSearch

def youtube(query):
    query = query.replace('play', ' ')
    query = query.replace('on youtube', ' ')
    query = query.replace('youtube', ' ')
    print("Searching...")
    results = VideosSearch(query, limit=1).result()
    print("Found a video")
    video_id = results['result'][0]['id']
    webbrowser.open(f'https://www.youtube.com/watch?v={video_id}')
    return "Enjoy, Sir..."

import smtplib
import os

def email(rec_email=None, text="Hello, It's TARRA here...", sub='TARRA'):
    if not rec_email or '@gmail.com' not in rec_email:
        print("Invalid recipient email.")
        return

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("311taara@gmail.com","xcznqjrcmukvwtig")  # Use an environment variable for the password
        message = 'Subject: {}\n\n{}'.format(sub, text)
        s.sendmail("311taara@gmail.com", rec_email, message)
        print("Sent")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        s.quit()
