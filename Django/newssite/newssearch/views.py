from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import TbUserSerializer
from .models import TbUser

def print_page(request):
    return HttpResponse('Here you are!')

class UserView(APIView):
    def get(self, request):
        return Response("N~~~~~ope!", status=200)

class TbUserViewset(viewsets.ModelViewSet):
    queryset = TbUser.objects.all()
    serializer_class = TbUserSerializer