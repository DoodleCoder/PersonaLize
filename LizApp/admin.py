from django.contrib import admin
# -*- coding: utf-8 -*-
from LizApp.models import *

admin.site.register(Diary)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Entry)