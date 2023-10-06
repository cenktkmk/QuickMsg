
from django.contrib import admin
from .models import *
from .views import *
# Register your models here.



admin.site.register(SiteUser)
admin.site.register(Tweet)
admin.site.register(Comment)
admin.site.register(ReportedTweet)
admin.site.register(ReportedComment)
admin.site.register(BannedUser)