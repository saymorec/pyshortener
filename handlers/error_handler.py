"""Error handlers"""

def handle_404(request, response, exception):
    response.set_status(404)
    response.out.write('<h1>404</h1>')