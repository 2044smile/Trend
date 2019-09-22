from django.db import models


class NaverRank(models.Model):
    rank_num = models.IntegerField(default=0)
    rank_title = models.CharField(max_length=144)

    def __str__(self):
        return str(self.rank_num) + ' ||| '+ self.rank_title