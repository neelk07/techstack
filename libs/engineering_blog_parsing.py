from bs4 import BeautifulSoup
import urllib2

YELP_ENGINEERING_BLOG_URL = "http://engineeringblog.yelp.com/"
DROPBOX_ENGINEERING_BLOG_URL = "https://tech.dropbox.com/"


def retrieve_page(url):
	serialized_data = urllib2.urlopen(url).read()
	return serialized_data

def yelp_blogs():
	page = retrieve_page(YELP_ENGINEERING_BLOG_URL)
	html = BeautifulSoup(page)
	blog_titles = html.find_all("h3", {"class":"entry-header"})
	for title in blog_titles:
		print title.string

'''TESTED: SUCCESS - retrieves engineering blogs from dropbox's engineering site'''
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
        Post.objects.create(title = title, author = author, description = content, date = date, company = company, url = link)



