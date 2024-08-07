from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


@login_required
def article_func(request):
    articles = Article.objects.all().order_by('-id')

    search = request.GET.get('search')
    articles = articles.filter(Q(title__icontains=search) | Q(text__icontains=search)) if search else articles

    context = {
        'articles': articles,
    }
    return render(request, 'home_list.html', context)


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.article = article
            instance.save()
            return redirect('article_detail', slug=slug)
    form = CommentForm()
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'article_detail.html', context)


@login_required
def article_create(request):
    form = ArticleForm(request.POST or None, request.FILES)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect('article_func')
    form = ArticleForm()
    return render(request, 'article_create.html', {'form': form})


def article_edit(request, slug):
    article = Article.objects.get(slug=slug)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        form.save()
        return redirect('article_detail', slug=request.POST.get('slug'))
    context = {
        "form": form, 'article': article
    }
    return render(request, 'article_edit.html', context)


def article_delete(request, slug):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        article.delete()
        return redirect('article_func')
    context = {
        "article": article
    }
    return render(request, 'article_delete.html', context)


def like_article(request, slug):
    article = Article.objects.get(slug=slug)

    if request.user not in article.likes.all():
        article.likes.add(request.user)
        article.dislikes.remove(request.user)
    elif request.user in article.likes.all():
        article.likes.remove(request.user)

    return redirect('article_detail', slug=slug)


def dislike_article(request, slug):
    article = Article.objects.get(slug=slug)
    if request.user not in article.dislikes.all():
        article.dislikes.add(request.user)
        article.likes.remove(request.user)
    elif request.user in article.dislikes.all():
        article.dislikes.remove(request.user)
    return redirect('article_detail', slug=slug)


def comment_delete(request, slug, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == "POST":
        comment.delete()
        return redirect('article_detail', slug=slug)
    context = {
        'comment': comment
    }
    return render(request, 'comment_delete.html', context)


def comment_edit(request, slug, pk):
    comment = Comment.objects.get(pk=pk)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('article_detail', slug=slug)

    context = {
        'form': form,
        'article': comment.article
    }
    return render(request, 'comment_edit.html', context)
