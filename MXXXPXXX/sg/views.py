from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import auth
import json

from .models import Writing, ScrapList
from .forms import UserForm, ArticleForm
from .sw_gpt_function import *
from .google_crawling_20026 import collect_links


# 단순히 HTML만 띄우는 코드
def index(request):
    headline = Writing.objects.all()[:10]
    poli = Writing.objects.filter(category='정치')[:5]
    it = Writing.objects.filter(category='IT/과학')[:5]
    culture = Writing.objects.filter(category='문화/예술')[:5]
    social = Writing.objects.filter(category='사회')[:5]
    context = {
        'headline': headline,
        'poli': poli,
        'it': it,
        'culture': culture,
        'social': social,
    }
    return render(request, 'sg/index.html', context)


# POST인경우 받아온 데이터를 처리하고 HTML에 넘겨줌
def writing(request):
    category = ['정치', '사회', 'IT/과학', '문화/예술']
    if request.method == "POST":
        # HTML에서 값 받아오는 법
        title = request.POST['title']
        content = request.POST['content']
        text = request.POST['text']
        checked = request.POST['category']
        links = request.POST['links']
        # 문장 생성 함수
        if request.GET.get('type') == 'text':
            gen = serveral_sentence_generate(content)
            for i in range(len(gen)):
                text = text + gen[i]
        if request.GET.get('type') == 'image':
            if title == '':
                return redirect('sg:writing')
            collect = collect_links.CollectLinks()
            links = collect.google_full(title)

        ctx = {
            'title': title,
            'content': '',
            'text': text,
            'links': links,
            'checked': checked,
            'category': category,
        }

    else:
        ctx = {
            'title': '',
            'content': '',
            'text': '',
            'links': '',
            'checked': '',
            'category': category,
        }

    return render(request, 'sg/writing.html', ctx)


# DB에 저장하고 index페이지로 이동
def save(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sg:index')
        else:
            return HttpResponse(form.errors)
    return redirect('sg:writing')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('sg:index')
        else:
            return HttpResponse(form.errors)

    else:
        form = UserForm()
        return render(request, 'sg/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        user = auth.authenticate(request, username=userid, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('sg:index')
        else:
            return render(request, 'sg/login.html',
                          {'error': 'userid or password is incorrect'})

    else:
        return render(request, 'sg/login.html')


def logout(request):
    auth.logout(request)
    return redirect('sg:index')


def recommend_words(request):
    if request.method == "POST":
        content = request.POST["content"]
        words_list = context_words_list2(content)
        recommend = []
        for i in range(5):
            recommend.append(words_list[i][0][0])
        ctx = {
            'recommend': recommend,
        }
        return HttpResponse(json.dumps(ctx), content_type="application/json")


def detail(request, pk):
    article = Writing.objects.get(id=pk)
    headline = Writing.objects.all()[:10]
    context = {
        'article': article,
        'headline': headline,
    }
    return render(request, 'sg/news_detail.html', context)


def scrap(request):
    if request.method == "POST":
        user_info = request.POST["user_id"]
        articleid = request.POST["article_id"]
        article = Writing.objects.get(id=articleid)
        title = article.title
        writer = article.writer
        category = article.category
        article.scrap_update
        scrap_cnt = article.scrap
        scrap_info = ScrapList(user_info=user_info,
                               title=title,
                               article_id=articleid,
                               category=category,
                               writer=writer,
                               scrap=scrap_cnt)
        scrap_info.save()
        #return HttpResponse(user_info)
        #return render(request, 'sg/scrap.html')
        return redirect('sg:scraplist')


def scraplist(request):
    scraps = ScrapList.objects.all()
    context = {'scraps': scraps}
    return render(request, 'sg/scrap.html', context)


def list(request):
    # 해당 카테고리인 최신글 10개 디비에서 가져오기
    headline = Writing.objects.all()[:10]
    cat = request.GET.get('cat')
    page = int(request.GET.get('page'))
    hot_article = ''
    if page == 1:
        hot_article = Writing.objects.filter(category=cat)[0]
    last_page = (Writing.objects.filter(category=cat).count() - 2) // 10 + 1
    article_range = range(1, last_page + 1)
    articles = Writing.objects.filter(category=cat)[1 + 10 * (page - 1):1 +
                                                    10 * page]
    context = {
        'cat': cat,
        'articles': articles,
        'range': article_range,
        'page': page,
        'hot_article': hot_article,
        'headline': headline,
        'last_page': last_page,
    }
    return render(request, 'sg/list.html', context)
