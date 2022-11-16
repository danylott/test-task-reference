from django.urls import path

from characters.views import get_random_character, CharacterListView

app_name = "characters"

urlpatterns = [
    path("characters/random/", get_random_character, name="character-random"),
    path("characters/", CharacterListView.as_view(), name="character-list"),
]
