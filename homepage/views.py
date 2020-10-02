from django.shortcuts import render, redirect
from .models import Article
from django.contrib.auth.decorators import login_required
from . import forms
import base64
import pickle



# Create your views here.

def indexHome(request):
    articles = Article.objects.all().order_by('date')
    context = {
        'articles': articles
    }
    return render(request, 'homepage/index.html', context)

def article_details(request, slug):
    article = Article.objects.get(slug=slug)
    context = {
        'article': article
    }
    return render(request, 'homepage/post.html', context)

@login_required(login_url="accounts/login")
def share_article(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            #save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:home')
    else:
        form = forms.CreateArticle()
    context = {
        'form':form,
    }
    return render(request, 'homepage/share.html', context)

def search_articles(request):
    if request.method == 'POST':
        # cookie = request.cookies.get("searched")
        # cookie = pickle.loads(base64.b64decode(cookie))
        try:
            cookie = request.COOKIES.get('search_cookie')
            cookie = pickle.loads(base64.b64decode(cookie))  
        except:
            pass  
        try:
            query = request.POST.get('query')
        except:
            pass
    context = {
        'query':query,
    }
    html = render(request, 'homepage/search.html', context)
    html.set_cookie('search_cookie', query)
    return html

    
    