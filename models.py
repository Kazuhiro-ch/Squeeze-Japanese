from django.db import models
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from streams import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings

class ArticleIndexPage(RoutablePageMixin, Page):
    """Article Index page class."""

    template = "articles/article_index.html"

    content = StreamField(
        [
            ("article_index_block", blocks.ArticleIndexBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = ArticleIndexPage.objects.live().public()
        return context

    @route(r'^latest/$')
    def latest_article_index(self,request, *args,**kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request,"articles/latest_index.html",context)

    class Meta:
        verbose_name = "Article index Page"
        verbose_name_plural = "Article index Pages"

class Like(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    title = models.CharField(max_length=100, default="")
    post = models.ForeignKey(ArticleIndexPage, on_delete=models.CASCADE)
    body = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True, blank=True)



    @login_required
    def like(self, request,*args, **kwargs):
        post = ArticleIndexPage.objects.get(id=kwargs['post_id'])
        is_like = Like.objects.filter(user=request.user).filter(post=post).count()
        # unlike
        if is_like > 0:
            liking = Like.objects.get(post__id=kwargs['post_id'], user=request.user)
            liking.delete()
            ArticleIndexPage.like_num -= 1
            ArticleIndexPage.save()
            messages.warning(request, 'いいねを取り消しました')
            return HttpResponseredirect(reverse_lazy('posts:post_detail', kwargs={'post_id': kwargs['post_id']}))

        # like
        ArticleIndexPage.like_num += 1
        ArticleIndexPage.save()
        like = Like()
        like.user = request.user
        like.post = post
        like.save()
        messages.success(request, 'いいね！しました')
        return HttpResponseRedirect(reverse_lazy('posts:post_detail', kwargs={'post_id': kwargs['post_id']}))

