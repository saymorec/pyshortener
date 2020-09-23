"""Handlers for Eagle Finance."""

import os
import jinja2
import webapp2

from models.link import Link

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=True)


def render_str(template, *args, **params):
    """Helper for rendering a template."""
    my_template = jinja_env.get_template(template)

    return my_template.render(params)


# HANDLERS
class Handler(webapp2.RequestHandler):
    """Set up the handler class."""

    def write(self, *args, **kwargs):
        """Write to response."""
        self.response.out.write(*args, **kwargs)

    def render(self, template, *args, **kwargs):
        """Render jinja template."""
        self.write(render_str(template, *args, **dict(kwargs)))
