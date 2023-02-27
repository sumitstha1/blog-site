from django.shortcuts import render
from articles.models import *

# Create your views here.
def index(request):
    article = Articles.objects.filter(is_approved = True)
    context = {
        'articles': article
    }

    return render(request, 'home/articles.html', context)