"""Handlers for adding links and check for stats."""
import csv

from handlers import Handler
from models.link import Link

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

MAX_URLS_TO_CONVERT = 500000


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
            self.error(404)


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
        upload_url = blobstore.create_upload_url('/links/upload_csv')
        self.render(
            'links/upload_csv.html',
            upload_url=upload_url,
        )

class UploadCSVHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        # prepare the csv file for reading
        upload_files = self.get_uploads('csv_file')
        blob_info = upload_files[0]
        blob_reader = blobstore.BlobReader(blob_info.key())
        reader = csv.reader(blob_reader, delimiter=',')

        # set up the csv file for download
        self.response.headers['Content-Type'] = 'text/csv'
        self.response.headers['Content-Disposition'] = 'attachment; filename=shorterned_urls.csv'
        writer = csv.writer(self.response.out)
        writer.writerow(['Original Url', 'Short Url'])

        # maximum link to convert is 500,000
        if len(list(reader)) > MAX_URLS_TO_CONVERT:
            raise ValueError("The maximum number of links to be converted is 500,000")
            # A better way to handle this would be with flash messages or alerts, etc

        # convert links, save to DB and download CSV
        for row in reader:
            if len(row) > 1:
                raise ValueError("Input must have a single url per line")
                # better checks can be implemented
            original_url = row[0]
            shortened_url = '{}/{}'.format(
                self.request.application_url,
                Link.shorten_url(original_url))

            writer.writerow([original_url, shortened_url])
