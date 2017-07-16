from django.views.generic import ListView, DetailView, TemplateView
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article, Tag

per_page = 5
# per_page = 10
tags = Tag.objects.all()


def index(request):
    # archive
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    # tag
    tag_name = request.GET.get('tag')
    # page
    page = request.GET.get('page') or 1

    if tag_name is None:
        articles = Article.objects.all()
    else:
        tag = get_object_or_404(Tag, name=tag_name)
        articles = tag.article_set.all()

    date = {}
    if year is not None:
        date.update({'first_commit__year': year})
    if month is not None:
        date.update({'first_commit__month': month})
    if day is not None:
        date.update({'first_commit__day': day})

    if date:
        articles = articles.filter(**date)

    paginator = Paginator(articles, per_page)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    q = request.GET.urlencode()
    q = QueryDict(q, mutable=True)
    try:
        q.pop('page')
    except KeyError:
        pass
    finally:
        parameters = q.urlencode()
        if parameters:
            parameters += '&'

    context = {
        'articles': articles,
        'tags': tags,
        'parameters': parameters,
    }
    return render(request, 'article/articles.html', context)


class ArticleListView(ListView):
    queryset = Article.objects.order_by('-first_commit')


class ArticleDetailView(DetailView):
    model = Article

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(self, request, *args, **kwargs)
        self.object.increase_views()
        return response


# def search(request):
#     q = request.GET.get('q')
#     # TODO
#     context = {}
#     return render(request, 'article/articles.html', context)


class SearchView(ListView):
    model = Article


class AboutView(TemplateView):
    template_name = 'article/about.html'
