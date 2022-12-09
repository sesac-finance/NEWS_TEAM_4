# C:\Users\19498\AppData\Local\Programs\Python\Python3_8\python manage.py runserver
from django.urls import path
from newssearch.views import print_page
from . import views

app_name = 'newssearch'

urlpatterns = [
    # path('first_page/', views.print_page),
    # path('details/<str:user_id>', views.details),
    # path('users/', views.UserView.as_view()),
    # path('domain/', views.TbDomainViewset.as_view({'get': 'list'})),
    path('recent/', views.RecentNewsList.as_view({'get': 'retrieve'})),  # 디폴트 (핫한 뉴스?)
    path('search/bynews/<int:news_id>', views.ContentsBasedSearch.as_view({'get': 'retrieve'})),  # 컨텐츠 기반
    path('search/byuser/<int:user_id>', views.CollaborativeBasedSearch.as_view({'get': 'retrieve'})),  # 협업 기반
    path('auth/users/<int:user_id>', views.TbUserTeam4Viewset.as_view({'get': 'retrieve'})),  # 특정 사용자 조회
    path('article/<int:article_id>', views.search_article_by_num.as_view({'get': 'retrieve'})),  # 특정 뉴스 기사 조회
]

# http://127.0.0.1:8000/api/team4/recent  # recent 접속시 default 로 설정된 카테고리별 최신 뉴스
# http://127.0.0.1:8000/api/team4/search/bynews/46413 # 컨텐츠 기반필터링 조회
# http://127.0.0.1:8000/api/team4/search/byuser/23 # 협업 기반필터링 조회
# http://127.0.0.1:8000/api/team4/auth/users/21 # 특정 사용자 조회
# http://127.0.0.1:8000/api/team4/article/32 # 특정 뉴스 기사 조회
