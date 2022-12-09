from rest_framework import serializers
from .models import TbUserTeam4, TbDomain, TbNewsTeam4, TbComment
from rest_framework import viewsets


class TbUserTeam4Serializer(serializers.ModelSerializer):
    class Meta:
        model = TbUserTeam4
        fields = '__all__'


class TbDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbDomain
        fields = '__all__'


class TbNewsTeam4Serializer(serializers.ModelSerializer):
    class Meta:
        model = TbNewsTeam4
        fields = '__all__'

class TbCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TbComment
        fields = '__all__'
