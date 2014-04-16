# Create your views here.
from bs4 import BeautifulSoup
import json
import urllib2
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import ModelForm
from django.forms.models import modelform_factory
from techstack_app.models import *
from glassdoor import get

#GLOBAL VARIABLES
CRUNCHBASE_API_KEY = "qh8x7d9kjfkxz6b2ftem46xy"

DROPBOX_ENGINEERING_BLOG_API_URL = "http://apify.heroku.com/api/dbeb.json"
YELP_ENGINEERING_BLOG_URL = "http://engineeringblog.yelp.com/"
DROPBOX_ENGINEERING_BLOG_URL = "https://tech.dropbox.com/"

#Generates Crunchbase Request 
def crunchbase_api(company_name):
    return "http://api.crunchbase.com/v/1/company/" + company_name + ".js?api_key=" + CRUNCHBASE_API_KEY

#Clean the company search
def clean_company(company_name):
    company_name = company_name.lower()
    company_name = company_name.capitalize()
    return company_name

def home_page(request):
    companies = Company.objects.all()
    variables = RequestContext(request, {
        'companies': companies
    })
    return render_to_response('index.html', variables)

def search_controller(request):
    dropbox_blogs()
    param = request.GET.get('company_name', '')
    company_name = clean_company(param)
    company = Company.objects.filter(company_name=company_name)
    print company
    if company:     #company already exists
        company = company[0]
        #print get(company) --> glassdoor works
        redirect_url = '/company/%s' % company.id
    else:           #create company page
        success = create_company_page(param)
        if success:
            company = Company.objects.filter(company_name=company_name)[0]
            redirect_url = '/company/%s' % company.id
        else:
            redirect_url = '/'

    return HttpResponseRedirect(redirect_url)


def suggestion_controller(request):
    companies = Company.objects.filter(company_name__icontains=param)
    print companies

def companies_page(request):
    companies = Company.objects.all()
    variables = RequestContext(request, {
        'companies': companies
    })
    return render_to_response('companies.html', variables)

def company_page(request, company_id):
    company = get_object_or_404(
            Company, id=company_id)

    tech_tags = Technology.objects.filter(company__id__exact=company_id)
    available_tech = Technology.objects.all()

    variables = RequestContext(request, {
        'company': company,
        'tech_tags': tech_tags,
        'available_tech': available_tech,
    })
    return render_to_response('company_page.html', variables)


def add_company_page(request):
    CompanyForm = modelform_factory(Company)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/companies')
    else:
        form = CompanyForm()

    return render_to_response('add_company.html', {
        "formset": form,
        },
        context_instance=RequestContext(request),
    )


def tagcloud_page(request):
    technologies = Technology.objects.order_by('?')

    MAX_WEIGHT = 5
    min_count = 0
    max_count = 0

    for tech in technologies:
        tech_count = tech.company.count()
        if tech_count < min_count:
            min_count = tech_count
        if max_count < tech_count:
            max_count = tech_count

    range = float(max_count - min_count)
    if range == 0:
        range = 1.0

    for tech in technologies:
        tech.weight = int(
                MAX_WEIGHT * (tech.company.count() - min_count) /range
        )

    return render_to_response('tagcloud.html', {
        'technologies' : technologies,
        },
    )

''' FUNCTION DEF:
    this will automatically create a companies home page if it doesn't exist in the data base
'''
def create_company_page(company_name):
    cb_url = crunchbase_api(company_name)
    serialized_data = urllib2.urlopen(cb_url).read()
    json_data = json.loads(serialized_data)
    
    #retrieve all important properties from crunchbase
    c_name = json_data['name']
    hp_url = json_data['homepage_url']
    blog_url = json_data['blog_url']
    category = json_data['category_code']
    employees = json_data['number_of_employees']
    
    #null check
    if employees == None:
        employees = 0
    
    founded_yr = json_data['founded_year']
    description = json_data['overview']
    total_money_raised = json_data['total_money_raised']

    #save the company
    Company.objects.create(company_name = c_name, homepage_url = hp_url, blog_url = blog_url, category = category, employees = employees, founded_year = founded_yr, description = description, total_money_raised = total_money_raised)

    #retrieve saved company
    company = Company.objects.get(company_name = c_name)
    #get five most important people and save them for the company
    people = json_data['relationships'][:5]
    for p in people:
        title = p['title']
        person = p['person']
        first = person['first_name']
        last = person['last_name']
        People.objects.create(first_name = first, last_name = last, title = title, company = company)

    return True


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


def retrieve_page(url):
    serialized_data = urllib2.urlopen(url).read()
    return serialized_data







