from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import os, jwt, time

class Authenticate(MiddlewareMixin):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		try:

			# Here is an example how you could exclude specific paths 
			#if request.path.startswith('/snippets/'):
			#	return self.get_response(request)

			if 'HTTP_X_AUTH_TOKEN' not in request.META.keys(): 
				return JsonResponse({ 'ErrorType': 'MISSING_ELEMENT', 'ErrorMessage': 'x-auth-token' }, status=401)

			token = request.META['HTTP_X_AUTH_TOKEN']

			appPrivateKey = os.environ.get('PAASWORD_APP_PRIVATE_KEY')
			if appPrivateKey is None: 
				return JsonResponse({ 'ErrorType': 'MISSING_ELEMENT', 'ErrorMessage': 'PAASWORD_APP_PRIVATE_KEY' }, status=401)

			user = jwt.decode(token, appPrivateKey)

			if (user is not None and user['AutoLogout']['IsEnabled']):
				loginTime = user['iat']
				now = int(round(time.time()))
				hoursSinceLogin = round((now - loginTime)/3600000)
				if hoursSinceLogin > user['AutoLogout']['LogoutEveryXHours']:
					return JsonResponse({ 'ErrorType': 'SESSION_EXPIRED', 'ErrorMessage': '' }, status=401)

			request.user = user;
			return self.get_response(request)
		except:
			return JsonResponse({ 'ErrorType': 'INTERNAL_ERROR', 'ErrorMessage': '' }, status=401)