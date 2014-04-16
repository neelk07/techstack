import json
import urllib2
from glassdoor import get
from techstack_app.models import *


#GLOBAL VARIABLES
CRUNCHBASE_API_KEY = "qh8x7d9kjfkxz6b2ftem46xy"

#Generates Crunchbase Request 
def crunchbase_api(company_name):
    return "http://api.crunchbase.com/v/1/company/" + company_name + ".js?api_key=" + CRUNCHBASE_API_KEY


''' FUNCTION DEF:
    this will automatically create a companies home page if it doesn't exist in the data base

    TESTING:
        - FAILS FOR AMAZON
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
