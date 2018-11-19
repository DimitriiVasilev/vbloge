from django.shortcuts import render
from .models import Category, Article, Comment
from django.utils import timezone
from .forms import ProfileForm, UserForm, CategoryForm, ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required


def index(request):
    categories = Category.objects.all()
    context = dict()
    context['categories'] = categories
    return render(request, 'vbloge/index.html', context)


def show_category(request, slug):
    context = dict()
    try:
        category = Category.objects.get(slug=slug)
        context['category'] = category
        now = timezone.now()
        articles = Article.objects.filter(category=category).exclude(publish_date__gt=now)
        context['articles'] = articles
    except Category.DoesNotExist:
        context['category'] = None
        context['articles'] = None
    return render(request, 'vbloge/category.html', context)


def show_article(request, category_slug, article_slug):
    context = dict()
    try:
        category = Category.objects.get(slug=category_slug)
        context['category'] = category
        article = Article.objects.get(slug=article_slug)
        context['article'] = article
        context['comments'] = Comment.objects.filter(article=article)
    except Category.DoesNotExist:
        context['category'] = None
        context['article'] = None
        context['comments'] = None
    return render(request, 'vbloge/article.html', context)


def register(request):
    registered = False
    context = dict(registered=registered, errors=None)
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            context['registered'] = True
        else:
            context['errors'] = profile_form.errors
    else:
        profile_form = ProfileForm()
        user_form = UserForm()
    context['profile_form'] = profile_form
    context['user_form'] = user_form
    return render(request, 'vbloge/register.html', context)


@login_required
def add_category(request):
    context = dict(errors=None, form=None)
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return index(request)
        else:
            context['errors'] = category_form.errors
    else:
        context['form'] = CategoryForm()
    return render(request, 'vbloge/add_category.html', context)


@login_required
def add_article(request, category_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        category = None
    context = dict(errors=None, form=None, category=category)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.category = category
            article.publish_date = timezone.now()
            article.author = request.user
            article.save()
            return show_category(request, category_slug)
        else:
            context['errors'] = article_form.errors
    else:
        context['form'] = ArticleForm()
    return render(request, 'vbloge/add_article.html', context)


@login_required
def show_profile(request):
    articles = Article.objects.filter(author=request.user)
    context = dict(articles=articles)
    return render(request, 'vbloge/profile.html', context)


@login_required
def add_comment(request, category_slug, article_slug):
    article = None
    category = None
    context = dict(errors=None, article=None)
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        pass
    if category:
        try:
            article = Article.objects.get(slug=article_slug, category=category)
            context['article'] = article
        except Article.DoesNotExist:
            pass
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and article:
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return show_article(request, category.slug, article.slug)
        else:
            context['errors'] = comment_form.errors
    else:
        context['form'] = CommentForm()
    return render(request, 'vbloge/add_comment.html', context)
