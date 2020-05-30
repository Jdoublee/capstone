from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .forms import UserForm
from .my_function import *


# 단순히 HTML만 띄우는 코드
def index(request):
    return render(request, 'sg/index.html')


# POST인경우 받아온 데이터를 처리하고 HTML에 넘겨줌
def writing(request):
    if request.method == "POST":
        # HTML에서 값 받아오는 법
        title = request.POST['title']
        content = request.POST['content']
        # 문장 생성 함수
        fin_content = generate_3rd(content)
        ctx = {
            'title': title,
            'content': content,
            'fin_content': fin_content,
        }
    else:
        ctx = {
            'title': '',
            'content': '',
            'fin_content': '',
        }
    return render(request, 'sg/writing.html', ctx)


# DB에 저장하고 index페이지로 이동
# ----------------DB불러오는거 아직 안함
def save(request):
    if request.method == "POST":
        title = request.POST['title']
        fin_content = request.POST['fin_content']

        # ------------------모델 불러와서 저장
    return redirect('sg:index')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'sg/index.html', {})
        else:
            return HttpResponse(form.errors)

    else:
        form = UserForm()
        return render(request, 'sg/signup.html', {'form': form})