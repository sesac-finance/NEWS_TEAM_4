from rest_framework import serializers
from .models import TbUser


class TbUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbUser
        fields = '__all__' 

