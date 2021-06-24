import json
import logging
import requests
from typing import List, Mapping

from fawkes.fetch.plugins.fetch_plugin import FetchPlugin

class AppStore(FetchPlugin):
    _platform = 'app_store'

    def __init__(self, country: str, app_id: str):
        self.country = country
        self.app_id = app_id

    def fetch(self):
        reviews = []
        logging.info("Fetching App Store reviews")
        # App store RSS feed limited to 10 pages
        for i in range(1,11):
            url = f"https://itunes.apple.com/{self.country}/rss/customerreviews/id={self.app_id}/page={i}/sortBy=mostRecent/json"
            response = requests.get(url)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logging.error(f"Error requesting App Store reviews: {err}")
                break # Should this break on first error?

            resp_json = json.loads(response.text)
            try:
                new_reviews = resp_json['feed']['entry']
            except KeyError:
                break
            reviews.extend(new_reviews)
        return reviews

    def parse(self, reviews: List[Mapping[str, Any]]):
        return reviews