from rest_framework import serializers

from characters.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ("id", "name", "status", "gender", "image")
