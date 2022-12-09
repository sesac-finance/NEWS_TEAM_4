from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import TbUserTeam4Serializer, TbDomainSerializer, TbNewsTeam4Serializer, TbCommentSerializer
from .models import TbUserTeam4, TbComment, TbNewsTeam4, TbDomain
from rest_framework.decorators import api_view
from rest_framework import status
import datetime
from django.core import serializers
from django.forms.models import model_to_dict


class RecentNewsList(viewsets.ModelViewSet):
    """
    recent 접속시 default 로 설정된 카테고리별 최신 뉴스
    input:
    output: list(TbNewsTeam4)
    """

    def retrieve(self, request):
        json_dumps_params = {'ensure_ascii': False}
        print('default page ', datetime.date(2022, 11, 30))

        sql = "select * from tb_news_team_4 where DATE_FORMAT(WritedAt ,'%%Y-%%m-%%d')='2022-11-30' group by SubCategory order by id desc"
        obj = TbNewsTeam4.objects.raw(sql)
        result_list = []
        # news_list = serializers.serialize("json", obj)
        data_list = serializers.serialize("python", obj)
        for data in data_list:
            result_list.append(data.get('fields'))
        # serializer_class = TbNewsTeam4Serializer(result_list, many=True)
        # list_of_dicts = [model_to_dict(l) for l in obj]
        # return HttpResponse(news_list, content_type='application/json')
        # return Response(result_list, status=status.HTTP_200_OK)
        # return HttpResponse(result_list, status=status.HTTP_200_OK)

        if len(data_list) == 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return JsonResponse(result_list, json_dumps_params=json_dumps_params, safe=False)


class ContentsBasedSearch(viewsets.ModelViewSet):
    """
    컨텐츠 기반필터링 조회
    input: news_id
    output: list(TbNewsTeam4)
    """

    def retrieve(self, request, news_id):
        json_dumps_params = {'ensure_ascii': False}
        queryset = TbNewsTeam4.objects.get(id=news_id)
        print("ContentsBasedSearch cossimilarity : ", news_id, " : ", queryset.cossimilarity)
        try:
            if queryset.cossimilarity != None:
                sql = f'select * from tb_news_team_4 where id in ({queryset.cossimilarity})'
                obj = TbNewsTeam4.objects.raw(sql)
                result_list = []
                data_list = serializers.serialize("python", obj)
                for data in data_list:
                    # print(data)
                    result_list.append(data.get('fields'))

                return JsonResponse(result_list, json_dumps_params=json_dumps_params, safe=False)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


class CollaborativeBasedSearch(viewsets.ModelViewSet):
    """
    협업 기반필터링 조회
    input: user_id
    output: list(TbNewsTeam4)
    """

    def retrieve(self, request, user_id):
        print(f'CollaborativeBasedSearch : {user_id}')
        # obj = get_object_or_404(TbUserTeam4, id=user_id)
        # serializer_class = TbUserTeam4Serializer(obj)
        # return Response(serializer_class.data)

        json_dumps_params = {'ensure_ascii': False}
        queryset = TbUserTeam4.objects.get(id=user_id)
        print("CollaborativeBasedSearch cossimilarity : ", user_id, " : ", queryset.cossimilarity)
        try:
            if queryset.cossimilarity != None:
                sql = f'select * from tb_user_team_4 where id in ({queryset.cossimilarity})'
                obj = TbNewsTeam4.objects.raw(sql)
                result_list = []
                data_list = serializers.serialize("python", obj)
                for data in data_list:
                    # print(data)
                    result_list.append(data.get('fields'))

                return JsonResponse(result_list, json_dumps_params=json_dumps_params, safe=False)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def create_user(request):
    print(f'create_user ')
    return Response('create_user', status=status.HTTP_200_OK)


class search_article_by_num(viewsets.ModelViewSet):
    """
    상세 뉴스 기사 조회
    input: article_id
    output: TbNewsTeam4
    """

    def retrieve(self, request, article_id):
        print(f'search_article_by_num : {article_id}')
        obj = get_object_or_404(TbNewsTeam4, id=article_id)
        serializer_class = TbNewsTeam4Serializer(obj)

        return Response(serializer_class.data)


class TbUserTeam4Viewset(viewsets.ModelViewSet):
    """
    특정 사용자 조회
    input: user_id
    output: TbUserTeam4
    """

    def retrieve(self, request, user_id):
        print(f'TbUserTeam4Viewset : {user_id}')
        obj = get_object_or_404(TbUserTeam4, id=user_id)
        serializer_class = TbUserTeam4Serializer(obj)

        return Response(serializer_class.data)


"""

class TbUserTeam4Viewset(viewsets.ModelViewSet):
    ueryset = TbUserTeam4.objects.all()[:10]
    serializer_class = TbUserTeam4Serializer
    def get(self, request, *args, **kwargs):
        try:
            queryset = TbUserTeam4.objects.get(userid=request.user_id)
            queryset = TbUserTeam4.objects[0:30]
            serializer_class = TbUserTeam4Serializer
        except Exception as e:
            print(e)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        return Response('POST Test OK', status=status.HTTP_200_OK)

    def put(self, request):
        return Response('Put Test OK', status=status.HTTP_200_OK)

    def delete(self, request):
        return Response('delete Test OK', status=status.HTTP_200_OK)
"""


class TbDomainViewset(viewsets.ModelViewSet):
    queryset = TbDomain.objects.all()
    serializer_class = TbDomainSerializer


@api_view(['GET'])
def print_page(request):
    return Response('Here you are!', status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
def details(request, user_id):
    print('user id : ', user_id)
    return Response('aaaa you are!', status=status.HTTP_200_OK)


class UserView(APIView):
    def get(self, request):
        return Response("N~~~~~ope!", status=status.HTTP_200_OK)
