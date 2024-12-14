from django.contrib import admin
from .models import Otp , TradingCodes , PrivatePerson , UserProfile , Accounts , Addresses , JobInfo 

admin.site.register(Otp)
admin.site.register(TradingCodes)
admin.site.register(PrivatePerson)
admin.site.register(UserProfile)
admin.site.register(Accounts)
admin.site.register(Addresses)
admin.site.register(JobInfo)

