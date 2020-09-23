"""Handlers for adding links and check for stats."""
from handlers import Handler

from models.link import Link


class AddLinkHandler(Handler):
    """Handler for the signup."""

    def get(self):
        """Define get method."""
        self.render(
            'links/add_link.html',
            original_url=''
        )

    def post(self):
        original_url = self.request.get('original_url')
        shortened_url = Link.shorten_url(original_url)

        self.render(
            'links/add_link.html',
            original_url=original_url,
            shortened_url=shortened_url,
            url=self.request.application_url)


class RedirectShortLinkHandler(Handler):
    """Handler for the signup."""

    def get(self, shortened_url):
        """Define get method."""
        redirect_url = Link.get_original_url(shortened_url)
        if redirect_url:
            self.redirect(redirect_url)
        else:
            self.redirect('/')


class LinkStatsHandler(Handler):
    """Handler for the signup."""

    def get(self):
        """Define get method."""
        stats = Link.get_stats()
        self.render(
            'links/get_stats.html',
            stats=stats,
            url=self.request.application_url
        )

class CSVHandler(Handler):
    def get(self):
        self.render(
            'links/upload_csv.html',
        )
