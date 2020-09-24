import webapp2

from handlers.links_handler import (
    AddLinkHandler,
    RedirectShortLinkHandler,
    LinkStatsHandler,
    CSVHandler,
    UploadCSVHandler,
)

from handlers.error_handler import handle_404

app = webapp2.WSGIApplication([
    ('/', AddLinkHandler),
    ('/links/stats', LinkStatsHandler),
    (r'/([a-zA-Z0-9]{5})', RedirectShortLinkHandler),
    ('/links/csv', CSVHandler),
    ('/links/upload_csv', UploadCSVHandler),
], debug=True)

app.error_handlers[404] = handle_404
