# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404


from techstack_app.models import *


def home_page(request):
    """docstring for home_page"""
    companies = Company.objects.all()
    variables = RequestContext(request, {
        'companies': companies
    })

    return render_to_response('base.html', variables)


def companies_page(request):
    # companies = Company.objects.order_by('-company_name')[:20]
    companies = Company.objects.all()
    variables = RequestContext(request, {
        'companies': companies
    })

    return render_to_response('companies.html', variables)


def company_page(request, company_id):
    company = get_object_or_404(
            Company, id=company_id)

    technologies = Technology.objects.filter(company__id__exact=company_id)

    variables = RequestContext(request, {
        'company': company,
        'technologies': technologies
    })
    return render_to_response('company_page.html', variables)
