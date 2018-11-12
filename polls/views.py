import auth
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from route import Route
from auth import handle_login, handle_register
from statistics import handle_query
from state import handle_savestate, handle_loadstate
from upload import handle_upload

routes = {
	'login': Route(handle_login, False),
	'register': Route(handle_register, False),
	'upload': Route(handle_upload),
	'query': Route(handle_query),
	'savestate': Route(handle_savestate),
	'loadstate': Route(handle_loadstate),
}

# Create your views here.
# Note: a view is a func taking the HTTP request and returns sth accordingly

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

def test(request):
	return HttpResponse("<h1>This is the very first HTTP request!</h1>")

def parse_body(request):
	return json.load(request)

@csrf_exempt
def handle_request(request):
	request_type = request.path_info.replace('/', '')

	if request_type not in routes:
		print "Cannot find request handler: " + request_type
		return HttpResponseNotFound('404 not found')

	route = routes[request_type]

	print "Request " + request_type

	if request.FILES:
		params = request.POST.copy()
		params['file'] = request.FILES
	else:
		params = parse_body(request)
	if route.requires_auth:
		if 'HTTP_AUTHORIZATION' not in request.META:
			return HttpResponse(json.dumps({
				'result': False,
				'message': 'Missing Auth Token'
			}))
		username = auth.verify_token(request.META['HTTP_AUTHORIZATION'])
		if username is None:
			return HttpResponse(json.dumps({
				'result': False,
				'message': 'Invalid Token'
			}))
		params['username'] = username
	response = route.handler(params)

	return HttpResponse(json.dumps(response))