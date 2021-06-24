import sys
import os
import re
from datetime import datetime, timedelta
from pytz import timezone
from pprint import pprint

# This is so that below import works.  Sets the pwd to home directory
sys.path.append(os.path.realpath("."))

import fawkes.utils.utils as utils
import fawkes.constants.constants as constants

url_regex = re.compile(constants.URL_REGEX)

class DerivedInsight:
    """ The Derived Insights from a user review.

    Derived insights include attributes like sentiment, category etc. which are obtained by running algorithms on top of the existing user review.

    Attributes:
        sentiment: The sentiment attached to the user review.
        category: The category in which the user review false.
        review_message_encoding: The sentence encoding into a vector.
        extra_properties: Any other extra derived insights. Free flowing dict.
    """

    def __init__(self, derived_insight = None):
        """ Initialiser of the derived insight """

        if derived_insight is None:
            self.sentiment = None
            self.category = constants.CATEGORY_NOT_FOUND
            self.review_message_encoding = None
            self.extra_properties = {}
        else:
            self.sentiment = derived_insight["sentiment"]
            self.category = derived_insight["category"]
            self.review_message_encoding = derived_insight["review_message_encoding"]
            self.extra_properties = derived_insight["extra_properties"]

    def to_dict(self):
        """ Converts the DerivedInsight class object to a dict """

        return {
            "sentiment": self.sentiment,
            "category": self.category,
            "review_message_encoding": self.review_message_encoding,
            "extra_properties": self.extra_properties,
        }

class Review:
    """ Definition of a user review.

    When initialising a user review, we also standardise the timestamp and cleanup the message.

    Attributes:
        message: The message in the review.
        timestamp: The timestamp when the review was submitted.
        rating: The rating attached to the review. Ideally a numeric value..
        user_id: Any identifier which uniquely indetifies a user.
        app_name: The name of the app from where the review originated.
        channel_name: The source/channel name from which the review originated.
        channel_type: The source/type from which the review originated.
        hash_id: A unique id for the review. Determined by sha1 of (message + timestamp).
        derived_insight: The derived insights like category, sentiment etc. associated with review.
        raw_review: The raw review without any modifications.
    """

    def __init__(
        self,
        message: str,
        timestamp:  = "",
        channel_name: str = "",
        rating = None,
        user_id = None
    ):
        """ Initialiser of a user review """
        self.message = self._clean_message(message)
        self.timestamp = self._convert_timezone(timestamp)
        self.channel_name = channel_name
        self.user_id = user_id

        rating = self._normalize_rating(rating)

        # Now that we have all info that we wanted for a review.
        # We do some post processing.
        if timestamp_format == constants.UNIX_TIMESTAMP:
            self.timestamp = datetime.fromtimestamp(timestamp)
        else:
            self.timestamp = datetime.strptime(
                timestamp, timestamp_format # Parse it using the given timestamp format
            )

        # Every review hash id which is unique to the message and the timestamp
        self.hash_id = utils.calculate_hash(self.message + self.timestamp.strftime(
            constants.TIMESTAMP_FORMAT # Convert it to a standard datetime format
        ) + str(self.user_id))

    def _clean_message(self, message):
        # Removes links from message using regex
        message = url_regex.sub("", message)
        # Removing the non ascii chars
        message = (message.encode("ascii", "ignore")).decode("utf-8")
        return message

    def _convert_timezone(self, timestamp):
        timestamp = timestamp.replace(
            tzinfo=timezone(review_timezone) # Replace the timezone with the given timezone
        ).astimezone(
            timezone("UTC") # Convert it to UTC timezone
        )
        return timestamp

    def _normalize_rating(self, rating):
        rating = float(rating)
        # Normalising the rating to be a value between 1 - 5
        if rating_max_value != None:
            rating = constants.RATINGS_NORMALIZATION_CONSTANT * (rating / rating_max_value)
            except ValueError:
                rating = None
        return rating

    def to_dict(self):
        """ Converts the Review class object to a dict """

        return {
            "message": self.message,
            "timestamp": self.timestamp.strftime(
                constants.TIMESTAMP_FORMAT # Convert it to a standard datetime format
            ),
            "rating": self.rating,
            "user_id": self.user_id,
            "app_name": self.app_name,
            "channel_name": self.channel_name,
            "hash_id": self.hash_id,
        }

    def __lt__(self, other):
        return len(self.message) < len(other.message)
