from rest_framework import serializers
from .models import *

# class HashTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HashTag
#         fields = ('name')

# class ParticipateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Participate
#         fields = ('name')

# class InterestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Interest
#         fields = ('name')


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
