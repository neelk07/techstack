from bs4 import BeautifulSoup
import urllib2


YELP_ENGINEERING_BLOG_URL = "http://engineeringblog.yelp.com/"
DROPBOX_ENGINEERING_BLOG_URL = "https://tech.dropbox.com/"
SQUARE_ENGINEERING_BLOG_URL = "http://corner.squareup.com/archives.html"
TWITTER_ENGINEERING_BLOG_URL = "https://blog.twitter.com/engineering"


def retrieve_page(url):
	serialized_data = urllib2.urlopen(url).read()
	return serialized_data

def quora_blog():
	#company = Company.objects.get(company_name = "Quora")
	page = retrieve_page(TWITTER_ENGINEERING_BLOG_URL)
	html = BeautifulSoup(page)
	posts = html.find_all("div", {"class":"node node-blog node-teaser"})
	for post in posts:
		title = post.find("h2")
		title = title.find("a")
		print title
		

quora_blog()