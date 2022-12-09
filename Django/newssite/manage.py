# cd .\venv\Studying\NEWS_TEAM_4\NEWS_TEAM_4_PersonalTest\django_news\newssite
# models.py 생성 -> 후 Serializers.py -> views.py -> urls.py
# D:\99.Dev\Python\pythonProject\Scripts\python manage.py inspectdb > models.py # db 구조 긁어다가 model.py로 코드 자동생성
# D:\99.Dev\Python\pythonProject\Scripts\python manage.py makemigrations newssearch 
# D:\99.Dev\Python\pythonProject\Scripts\python manage.py migrate

# 기존 존재하는 디비 테이블 불러들어와 model.py 생성
# D:\99.Dev\Python\pythonProject\Scripts\python manage.py inspectdb > model.py

# 관리자 생성 및 페이지 체크
# D:\99.Dev\Python\pythonProject\Scripts\python manage.py createsuperuser

# for test
# http://127.0.0.1:8000/newssearch/first_page/
# http://127.0.0.1:8000/users/
# http://127.0.0.1:8000/posts

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newssite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
