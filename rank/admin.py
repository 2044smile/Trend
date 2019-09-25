from django.contrib import admin
from rank.models import DaumRank, NaverRank, GoogleRank


admin.site.register(NaverRank)
admin.site.register(DaumRank)
admin.site.register(GoogleRank)