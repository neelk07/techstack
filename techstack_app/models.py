from django.db import models


class Company(models.Model):
    """docstring"""

    company_name = models.CharField(max_length='50')
    location = models.CharField(max_length='20')
    link_to_main = models.URLField(verify_exists=True, max_length=100, blank=False)
    link_to_github = models.URLField(verify_exists=False, max_length=100, blank=True)
    description = models.TextField(blank=False)



    def __unicode__(self):
        return self.company_name



class Technology(models.Model):
    language = models.CharField(max_length='30', blank=False)
    technology_name = models.CharField(max_length='30', blank=False)
    company = models.ManyToManyField(Company)


    def __unicode__(self):
        return self.technology_name

