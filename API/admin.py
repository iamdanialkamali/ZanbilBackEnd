from django.contrib import admin
from .models import Users,Business,Categories,Services,TimeTable,Reserves

#admin.site.register(User)
admin.site.register(Users)
admin.site.register(Business)
admin.site.register(Categories)
admin.site.register(Services)
admin.site.register(TimeTable)
admin.site.register(Reserves)
#admin.site.register(Point)

# Register your models here.
