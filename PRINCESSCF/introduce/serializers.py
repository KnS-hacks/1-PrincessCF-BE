from rest_framework import serializers
from .models import *


class MemberSerializer(serializers.ModelSerializer):
    hashtag = serializers.PrimaryKeyRelatedField(
        many=True, queryset=HashTag.objects.all())
    interest = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Interest.objects.all())
    participate = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Participate.objects.all())

    class Meta:
        model = Member
        fields = ('name', 'team', 'school', 'participate', 'introduce',
                  'interest', 'hashtag')
