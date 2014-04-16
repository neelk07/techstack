from django.db import models
from django.forms import ModelForm


class Company(models.Model):
    company_name = models.CharField(max_length = 50)
    homepage_url = models.URLField(max_length = 200)
    blog_url = models.URLField(max_length = 200)
    category = models.CharField(max_length = 50)
    employees = models.IntegerField(null = True)
    founded_year = models.IntegerField()
    location = models.CharField(max_length = 20, blank= True)
    link_to_github = models.URLField(max_length=300, blank=True)
    description = models.TextField(blank=False)
    total_money_raised = models.CharField(max_length= 100)
    
    def __unicode__(self):
        return self.company_name

class CompanyForm(ModelForm):
    class Meta:
        model = Company

class People(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    title = models.CharField(max_length = 50)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return  u'%s %s - %s' %(self.first_name, self.last_name, self.company.company_name)

class Technology(models.Model):
    language = models.CharField(max_length=30, blank=False)
    technology_name = models.CharField(max_length=30, blank=False)
    company = models.ManyToManyField(Company)

    def __unicode__(self):
        return self.technology_name

class Post(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    url = models.URLField(max_length=300)



