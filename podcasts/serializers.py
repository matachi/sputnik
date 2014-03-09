from rest_framework import serializers


class SubscribeSerializer(serializers.Serializer):
    podcast = serializers.CharField()
    subscribe = serializers.BooleanField()


class ListenedSerializer(serializers.Serializer):
    episode = serializers.IntegerField()
    listened = serializers.BooleanField()
