from django.db import models
from base.models import BaseModel
from accounts.models import *
from django.utils.text import slugify
from ckeditor.fields import RichTextField 

# Create your models here.
class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name


class Articles(BaseModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=255)
    slug = models.SlugField(null = True, blank=True)
    content = RichTextField()
    category = models.ManyToManyField(Category, related_name='article_category', blank=True)
    is_approved = models.BooleanField(default=False)
    is_latest = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Articles, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

class ArticleImage(BaseModel):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="article_images")
    image = models.ImageField(upload_to="article_image")
