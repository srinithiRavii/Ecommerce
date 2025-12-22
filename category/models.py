from django.db import models


class Category(models.Model):
    category_name=models.CharField(max_length=100,unique=True)
    slug=models.CharField(max_length=200,unique=True)
    description=models.CharField(max_length=1000,blank=True)
    cat_img=models.ImageField(upload_to='photos/categories')
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    def __str__(self):
        return self.category_name
