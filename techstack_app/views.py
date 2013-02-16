# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404

from django.forms import ModelForm
from django.forms.models import modelform_factory


from techstack_app.models import *


def home_page(request):
    """docstring for home_page"""
    companies = Company.objects.all()
    variables = RequestContext(request, {
        'companies': companies
    })

    return render_to_response('index.html', variables)


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

