# Copyright 2025 Amazon Inc

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Find some apartments and calculate distance to Caltrain station.

Usage:
python -m nova_act.samples.apartments_caltrain \
    [--caltrain_city <city_with_a_caltrain_station>] \
    [--bedrooms <number_of_bedrooms>] \
    [--baths <number_of_baths>] \
    [--headless]
"""

import fire  # type: ignore
from pydantic import BaseModel

from nova_act import NovaAct


class Apartment(BaseModel):
    address: str
    price: str
    beds: str
    baths: str


class ApartmentList(BaseModel):
    apartments: list[Apartment]


class CaltrainBiking(BaseModel):
    biking_time_hours: int
    biking_time_minutes: int
    biking_distance_miles: float


def aggregate(results: list[dict]) -> list[dict]:
    # For demonstration, simply sort the results by the distance.
    # Assumes that 'distance' is convertible to a float.
    def sort_key(item):
        try:
            return float(item.get("distance", "0"))
        except Exception:
            return 0.0
    return sorted(results, key=sort_key)


def main(
    caltrain_city: str = "Redwood City",
    bedrooms: int = 2,
    baths: int = 1,
    headless: bool = False,
    min_apartments_to_find: int = 5,
):
    # Initialize main Nova Act session for apartment listings
    main_nova = NovaAct(
        starting_page="https://www.realestate-website.com/",
        headless=headless,
        chrome_channel="chromium"
    )
    main_nova.start()
    main_nova.act(f"search for apartments in {caltrain_city}")

    # Extract listing elements (each representing z₀²)
    listings = main_nova.act(f"extract {min_apartments_to_find} apartment listings")

    # For each listing, start parallel Nova Act sessions (recursive iterations)
    results = []
    for listing in listings:
        # Each parallel session represents an iteration extracting detail (c input)
        detail_nova = NovaAct(
            starting_page=listing.url,
            headless=headless,
            chrome_channel="chromium"
        )
        detail_nova.start()
        # Act on finding distance information (e.g., via clicking or reading a field)
        detail_nova.act("extract distance from train station")
        distance = detail_nova.act("get the distance value from span.distance")
        results.append({
            "apartment": listing.identifier,
            "distance": distance
        })
        detail_nova.stop()

    # Synthesize the results (z₂ iteration)
    integrated_result = aggregate(results)
    print("Final Result Set:", integrated_result)
    main_nova.stop()


if __name__ == "__main__":
    fire.Fire(main)
