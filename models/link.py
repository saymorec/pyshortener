"""Link model."""
import string 
from google.appengine.ext import db

import random 


class Link(db.Model):
    """Create an link model."""

    created_at = db.DateTimeProperty(auto_now_add=True)

    original_url = db.StringProperty()  # e.g. www.google.com/search/today/en?q=N

    # shortened form of the original url string with length = 5. 
    # length can be changed depending on traffic
    short_url = db.StringProperty() 

    # track number of visits 
    visits = db.IntegerProperty(default=0)

    @staticmethod
    def shorten_url(original_url):

        def get_shorter_url():
            base62 = string.uppercase + string.lowercase + string.digits
            return ''.join(random.sample(list(base62), k=5))

        if Link.original_url_exists(original_url):
            return Link.original_url_exists(original_url)

        while True:
            short_url = get_shorter_url()
            # check if shorturl exists
            if not Link.shorturl_exists(short_url):
                break

        new_link = Link(
            original_url=original_url,
            short_url=short_url)
        new_link.put()

        return short_url

    @staticmethod
    def get_stats():
        query = Link.all()
        query.order("-created_at")

        return query.fetch(10000)

    @staticmethod
    def shorturl_exists(short_url):
        query = Link.all()
        query.filter('short_url =', short_url)
        return query.get() 

    @staticmethod
    def original_url_exists(original_url):
        query = Link.all()
        query.filter('original_url =', original_url)
        result = query.get()
        return result.short_url if result else None  

    @staticmethod
    def get_original_url(short_url):
        result = Link.shorturl_exists(short_url)
        if result:
            result.visits += 1  # increment visits
            result.put()
            return '{}'.format(result.original_url)
        return False
