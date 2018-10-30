# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

import json

from utils import parseCSVFileFromDjangoFile, isNumber, returnTestChartData
from getInsight import parseAuthorCSVFile, getReviewScoreInfo, getAuthorInfo, getReviewInfo, getSubmissionInfo

from auth import handle_login, handle_register
from query import handle_query
from state import handle_savestate, handle_loadstate

routes = {
	'login': handle_login,
	'register': handle_register,
	'query': handle_query,
	'savestate': handle_savestate,
	'loadstate': handle_loadstate,
}

# Create your views here.
# Note: a view is a func taking the HTTP request and returns sth accordingly

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

def test(request):
	return HttpResponse("<h1>This is the very first HTTP request!</h1>")

# Note: csr: cross site request, adding this to enable request from localhost
@csrf_exempt
def uploadCSV(request):
	print request.POST['token']
	print "Inside the upload function"
	if request.FILES:
		csvFile = request.FILES['file']
		fileName = str(csvFile.name)
		rowContent = ""

		if "author.csv" in fileName:
			rowContent = getAuthorInfo(csvFile)
		elif "score.csv" in fileName:
			rowContent = getReviewScoreInfo(csvFile)
		elif "review.csv" in fileName:
			rowContent = getReviewInfo(csvFile)
		elif "submission.csv" in fileName:
			rowContent = getSubmissionInfo(csvFile)
		else:
			rowContent = returnTestChartData(csvFile)

		print type(csvFile.name)

		if request.POST:
	# current problem: request from axios not recognized as POST
			# csvFile = request.FILES['file']
			print "Now we got the csv file"

		return HttpResponse(json.dumps(rowContent))
		# return HttpResponse("Got the CSV file.")
	else:
		print "Not found the file!"
		return HttpResponseNotFound('Page not found for CSV')

def parse_body(request):
	return json.load(request)

@csrf_exempt
def handle_request(request):
	request_type = request.path_info.replace('/', '')

	if request_type not in routes:
		print "Cannot find request handler: " + request_type
		return HttpResponseNotFound('404 not found')

	params = parse_body(request)
	response = routes[request_type](params)
	return HttpResponse(json.dumps(response))