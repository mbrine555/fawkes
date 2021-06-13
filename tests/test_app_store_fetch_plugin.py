import pytest
import responses

from fawkes.fetch.plugins.appstore import AppStore

@pytest.fixture
def app_store_plugin():
    return AppStore(country="us", app_id=1)

@responses.activate
def test_app_store_fetch_success(app_store_plugin):
    response_data = {
        "feed": {
            "entry": [
                {
                    "review": "text"
                },
                {
                    "review_2": "text_2"
                }
            ]
        },
        "field_2": "value"
    }

    for i in range(1,11):
        responses.add(
            responses.GET,
            f"https://itunes.apple.com/us/rss/customerreviews/id=1/page={i}/sortBy=mostRecent/json",
            json=response_data
        )

    reviews = app_store_plugin.fetch()
    assert reviews == [{"review": "text"}, {"review_2": "text_2"}]*10

@responses.activate
def test_app_store_less_than_ten_pages(app_store_plugin):
    response_data = {
        "feed": {
            "entry": [
                {
                    "review": "text"
                },
                {
                    "review_2": "text_2"
                }
            ]
        },
        "field_2": "value"
    }

    for i in range(1,3):
        responses.add(
            responses.GET,
            f"https://itunes.apple.com/us/rss/customerreviews/id=1/page={i}/sortBy=mostRecent/json",
            json=response_data
        )

    responses.add(
        responses.GET,
        f"https://itunes.apple.com/us/rss/customerreviews/id=1/page=3/sortBy=mostRecent/json",
        json={"feed":{"field_2": "value"}}
    )

    reviews = app_store_plugin.fetch()
    assert reviews == [{"review": "text"}, {"review_2": "text_2"}]*2

@responses.activate
def test_app_store_http_error(app_store_plugin):

    responses.add(
        responses.GET,
        f"https://itunes.apple.com/us/rss/customerreviews/id=1/page=1/sortBy=mostRecent/json",
        json={"error": "not found"},
        status=404
    )

    reviews = app_store_plugin.fetch()
    assert reviews == []