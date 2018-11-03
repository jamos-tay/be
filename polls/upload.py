# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from utils import parseCSVFileFromDjangoFile, isNumber, returnTestChartData
from getInsight import parseAuthorCSVFile, getReviewScoreInfo, getAuthorInfo, getReviewInfo, getSubmissionInfo
import json

@csrf_exempt
def handle_upload(request):
	if 'username' not in request.POST:
		return {
			'result': False,
			'message': 'Missing username'
		}
	username = request.POST['username']
	if request.FILES:
		csvFile = request.FILES['file']
		fileName = str(csvFile.name)
		rowContent = ""

		if "author.csv" in fileName:
			rowContent = getAuthorInfo(username, csvFile)
		elif "score.csv" in fileName:
			rowContent = getReviewScoreInfo(csvFile)
		elif "review.csv" in fileName:
			rowContent = getReviewInfo(username, csvFile)
		elif "submission.csv" in fileName:
			rowContent = getSubmissionInfo(username, csvFile)
		else:
			rowContent = returnTestChartData(csvFile)

		print type(csvFile.name)

		if request.POST:
	# current problem: request from axios not recognized as POST
			# csvFile = request.FILES['file']
			print "Now we got the csv file"

		return rowContent
		# return HttpResponse("Got the CSV file.")
	else:
		print "Not found the file!"
		return {
            'result' : False,
            'message' : 'Page not found for CSV'
        }