class LastVisitedMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		return response

		if request.method == 'GET':

			path = request.get_full_path()
			if not all(path.startswith(f'/{slug}') for slug in ['login', 'logout', 'register', 'admin', 'order']):
				request.session['last_visited'] = path

		return response