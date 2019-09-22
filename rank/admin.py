from django.contrib import admin
from rank.models import DaumRank
from .models import NaverRank


admin.site.register(NaverRank)
admin.site.register(DaumRank)