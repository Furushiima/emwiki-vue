from django.db import models
from django.urls import reverse_lazy


class Content(models.Model):
    # 抽象基底クラス
    name = models.CharField(primary_key=True, max_length=50)
    category = models.CharField(max_length=20)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.category}:{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('contents:index', kwargs={'category': self.category, 'name': self.name})

    def get_static_url(self):
        pass

    def get_static_path(self):
        pass
