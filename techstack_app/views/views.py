# Create your views here.
from bs4 import BeautifulSoup
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.forms.models import modelform_factory
from techstack_app.models import *
from engineering_blog_parsing import *
from company_info import *

#importing other views

def home_page(request):
    companies = Company.objects.all()
    variables = RequestContext(request, {
        'companies': companies
    })
    return render_to_response('index.html', variables)


def search_controller(request):
    param = request.GET.get('company_name', '')
    company_name = clean_company(param)
    company = Company.objects.filter(company_name=company_name)
    if company:                         #company already exists
        company = company[0]
                                                                            #print get(company) --> glassdoor works
        redirect_url = '/company/%s' % company.id
    else:                                  #create company page
        c_name = create_company_page(company_name)
        if c_name != None:
            company = Company.objects.filter(company_name=c_name)[0]
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
    company = get_object_or_404(Company, id=company_id)
    posts = Post.objects.filter(company = company)
    tech_tags = Technology.objects.filter(company__id__exact=company_id)
    available_tech = Technology.objects.all()

    variables = RequestContext(request, {
        'company': company,
        'posts':posts,
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

def parse_blogs(request):
  return_message = {}
  try:
    square_blogs()
    dropbox_blogs()
  except:
    return_message['status'] = 'Error'
    return_message['message'] = sys.exc_info()[0]
    return HttpResponse(json.dumps(return_message), content_type="application/json")
  else:
    return_message['status'] = 'Success'
    return_message['message'] = 'Parsed Blogs'
    return HttpResponse(json.dumps(return_message), content_type="application/json")


'''AUXILLARY FUNCTIONS '''

#Clean the company search
def clean_company(company_name):
    company_name = company_name.lower()
    company_name = company_name.capitalize()
    return company_name








