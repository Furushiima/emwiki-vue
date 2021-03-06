import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Article, Comment
from rest_framework import viewsets
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('name')
    serializer_class = ArticleSerializer


class TestView(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return JsonResponse({'username': request.user.username})

    def post(self, request):
        print(request.user.username)
        return JsonResponse({'status': 'OK'})


class ArticleView(View):
    def get(self, request, filename, *args, **kwargs):
        name = os.path.splitext(filename)[0]
        article = Article.objects.get(name=name)
        context = dict()
        context['name'] = article.name
        context['template_path'] = f"article/htmlized_mml/{article.name}.html"
        bib_file_path = os.path.join(settings.MML_FMBIBS_DIR, f'{article.name}.bib')
        if os.path.exists(bib_file_path):
            with open(bib_file_path, "r") as f:
                context['bib_text'] = f.read()
        else:
            context['bib_text'] = f"{bib_file_path.basename()} not found"
        context["context_for_js"] = {
            'is_authenticated': self.request.user.is_authenticated,
            'name': article.name,
            'comments': list(Comment.objects.filter(article=article).values()),
            'comment_url': reverse('article:comment'),
            'names_url': reverse('article:names')
        }
        return render(request, "article/index.html", context)


class ProofView(View):
    def get(self, request, article_name, proof_name):
        return HttpResponse(
            open(os.path.join(settings.MML_HTML_DIR, 'proofs',
                 article_name, proof_name)).read(),
            content_type='application/xml'
        )


class RefView(View):
    def get(self, request, article_name, ref_name):
        return HttpResponse(
            open(os.path.join(settings.MML_HTML_DIR,
                 'refs', article_name, ref_name)).read(),
            content_type='application/xml'
        )


class CommentView(View):

    def get(self, request, *args, **kwargs):
        query = Comment.objects
        if 'article_name' in request.GET:
            query = query.filter(
                article=Article.objects.get(
                    name=request.GET.get("article_name"))
            )
        if 'block' in request.GET:
            query = query.filter(
                block=request.GET.get('block')
            )
        if 'block_order' in request.GET:
            query = query.filter(
                block_order=int(request.GET.get("block_order"))
            )
        return HttpResponse(
            serializers.serialize('json', query.all()), content_type='application/json'
        )

    @method_decorator(login_required)
    def post(self, request):
        article_name = request.POST.get('article_name', None)
        block = request.POST.get('block', None)
        block_order = request.POST.get("block_order", None)
        text = request.POST.get('comment', None)
        article = Article.objects.get(name=article_name)
        if Comment.objects.filter(article=article, block=block, block_order=block_order).exists():
            comment = Comment.objects.get(
                article=article, block=block, block_order=block_order)
        else:
            comment = Comment(article=article, block=block,
                              block_order=block_order, text='')
        comment.text = text
        comment.save()
        article.save_db2mizfile()
        article.commit_mizfile(request.user.username)
        return HttpResponse(status=201)


@cache_page(60 * 60 * 24)
def get_names(request):
    return HttpResponse(
        serializers.serialize(
            'json', Article.objects.order_by("name").all()
        ),
        content_type='application/json'
    )
