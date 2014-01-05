from rest_framework import serializers


class SubscribeSerializer(serializers.Serializer):
    podcast = serializers.IntegerField()
    subscribe = serializers.BooleanField()
