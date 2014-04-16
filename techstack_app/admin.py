from techstack_app.models import *
from django.contrib import admin


class CompanyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Company, CompanyAdmin)

class TechnologyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Technology, TechnologyAdmin)

class PeopleAdmin(admin.ModelAdmin):
	pass

admin.site.register(People, PeopleAdmin)
