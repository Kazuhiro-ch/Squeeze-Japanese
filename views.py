from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from streams.blocks import ArticleIndexBlock


# Create your views here.
class LikeButton(APIView):

    authentication_classes = (authentication.SessionAuthentication,) #ユーザーが認証されているか確認
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        obj = get_object_or_404(ArticleIndexBlock, user = self.request.user) #ユーザー情報の取得
        if user in obj.like.all(): #ユーザーがいいねをしていた場合
            if not(status):
                liked = True
            else:
                obj.like.remove(user) #likeからユーザーを外す
                liked = False
        else: #ユーザーがいいねをしていない場合
            if not(status):
                liked = False
            else:
                obj.like.add(user) #likeにユーザーを加える
                liked = True

        data = {
            "liked": liked,
        }
        return Response(data)