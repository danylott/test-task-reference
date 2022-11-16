import asyncio
import time

import httpx
from django.conf import settings
from httpx import AsyncClient

from characters.models import Character


GRAPHQL_QUERY = """
query {
  characters(page: {page}) {
    results{
      api_id: id
      name
      status
      gender
      image
    }
  }
}
"""


def parse_characters_response(characters_response: dict) -> list[Character]:
    return [
        Character(
            api_id=character_dict["id"],
            name=character_dict["name"],
            status=character_dict["status"],
            gender=character_dict["gender"],
            image=character_dict["image"],
        )
        for character_dict in characters_response["results"]
    ]


async def scrape_single_page(
    client: AsyncClient, url_to_scrape: str, page: int
) -> list[Character]:
    characters_response = (
        await client.post(
            url_to_scrape, data={"query": GRAPHQL_QUERY.format(page=page)}
        )
    ).json()
    return parse_characters_response(characters_response)


async def scrape_characters() -> list[Character]:
    start = time.perf_counter()

    url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    characters_response = httpx.get(url_to_scrape).json()
    num_pages = characters_response["info"]["pages"]
    characters = parse_characters_response(characters_response)

    async with httpx.AsyncClient() as client:
        characters.extend(
            sum(
                await asyncio.gather(
                    *[
                        scrape_single_page(client, url_to_scrape, page)
                        for page in range(2, num_pages + 1)
                    ]
                ),
                [],
            )
        )

        end = time.perf_counter()
        print("Elapsed for scraping:", end - start)

        return characters


async def save_characters(characters: list[Character]) -> None:
    start = time.perf_counter()

    await Character.objects.abulk_create(characters, ignore_conflicts=True)

    end = time.perf_counter()
    print("Elapsed for saving:", end - start)


async def sync_characters_with_api() -> None:
    characters = await scrape_characters()
    await save_characters(characters)
