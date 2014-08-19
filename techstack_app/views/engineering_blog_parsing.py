from bs4 import BeautifulSoup
import urllib2
import simplejson as json
#from techstack_app.models import *


YELP_ENGINEERING_BLOG_URL = "http://engineeringblog.yelp.com/"
DROPBOX_ENGINEERING_BLOG_URL = "https://tech.dropbox.com/"
SQUARE_ENGINEERING_BLOG_URL = "http://corner.squareup.com/archives.html"
QUORA_ENGINEERING_BLOG_URL = "http://engineering.quora.com/"
HACKER_NEWS_API_URL = "http://hnify.herokuapp.com/"

def retrieve_page(url):
	serialized_data = urllib2.urlopen(url).read()
	return serialized_data

def hackernews_articles():
        top_articles = retrieve_page(HACKER_NEWS_API_URL + "get/top")
        print type(json.loads(top_articles))

hackernews_articles()

def yelp_blogs():
	page = retrieve_page(YELP_ENGINEERING_BLOG_URL)
	html = BeautifulSoup(page)
	blog_titles = html.find_all("h3", {"class":"entry-header"})
	for title in blog_titles:
		print title.string

def dropbox_blogs():
	company = Company.objects.get(company_name = "Dropbox")
	page = retrieve_page(DROPBOX_ENGINEERING_BLOG_URL)
	html = BeautifulSoup(page)
	posts = html.find_all("div", {"class":"post hentry"})
	for post in posts:
		tag = post.find("a")
		title = tag.string
		link = tag.get("href")
		author = post.find("span", {"class":"fn"})
		author = author.string
		date = post.find("span", {"class":"published posted_date"})
		date = date.string
		content = post.find("div", {"class": "entry-content"})
                if not Post.objects.filter(title = title):
                  Post.objects.create(title = title, url = link, author= author, description = content, date = date, company = company)

def square_blogs():
	company = Company.objects.get(company_name = "Square")
	SQUARE_BLOG_URL = "http://corner.squareup.com"
	page = retrieve_page(SQUARE_ENGINEERING_BLOG_URL)
	html = BeautifulSoup(page)
	posts = html.find_all("li", {"class":"post"})
	for post in posts:
		title = post.find("h5",{"class":"post-title"})
		title = title.string
		description = post.find("div", {"class":"post-summary"})
		description = description.find("p")
		description = description.string
		if description == None:
			description = " "
		link = post.find("a")
		link = link.get("href")
		link = SQUARE_BLOG_URL + link
		author = "Square Engineering"
		date = post.find("div", {"class":"date short-date"})
		date = date.string
                if not Post.objects.filter(title = title):
		  Post.objects.create(title = title, url = link, author= author, description = description, date = date, company = company)


def quora_blog():
	company = Company.objects.get(company_name = "Quora")
	page = retrieve_page(QUORA_ENGINEERING_BLOG_URL)
	html = BeautifulSoup(page)
	posts = html.find_all("div", {"class":"blog_post"})
	for post in posts:
		title = post.find("strong")
		print title
		'''
		title = post.find("h5",{"class":"post-title"})
		title = title.string
		description = post.find("div", {"class":"post-summary"})
		description = description.find("p")
		description = description.string
		if description == None:
			description = " "
		link = post.find("a")
		link = link.get("href")
		link = SQUARE_BLOG_URL + link
		author = "Square Engineering"
		date = post.find("div", {"class":"date short-date"})
		date = date.string
		Post.objects.create(title = title, url = link, author= author, description = description, date = date, company = company)
		'''







