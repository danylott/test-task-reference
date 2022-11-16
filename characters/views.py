import random

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics

from characters.models import Character
from characters.serializer import CharacterSerializer


@api_view(["GET"])
def get_random_character(request: Request) -> Response:
    pks = Character.objects.values_list("pk", flat=True)
    random_pk = random.choice(pks)
    random_character = Character.objects.get(pk=random_pk)
    serializer = CharacterSerializer(random_character)

    return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
    serializer_class = CharacterSerializer

    def get_queryset(self) -> QuerySet:
        queryset = Character.objects.all()

        name = self.request.query_params.get("name")

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset
