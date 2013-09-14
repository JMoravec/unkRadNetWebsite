from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Data.models import *
    

def index(request):
	return render(request, 'Data/index.html')

def addData(request):
	return render(request, 'Data/addData.html')

def addFilter(request):
	if request.method == 'POST':
		filterform = FilterForm(request.POST)
		try:
			filterform.save()
		except(e):
			print e
			return HttpResponseRedirect('/Data/AddData/')
	else:
		filterform = FilterForm()

	return render(request, 'Data/addFilter.html', { 'filterform': filterform, })	

def addRawData(request):
	if request.method == 'GET':
		rows = 1
		rowForm = rawDataRows()

	"""
	if (request.method == 'POST' and submit is True):
		rawDataForm = RawDataForm(request.POST)
		activityForm = ActivityForm(request.POST)
		try:
			rawDataForm.save()
			activityForm.save()
		except(e):
			print e
			return HttpResponseRedirect('/Data/AddData/')
	"""

	if (request.method == 'POST'):
		rowForm = rawDataRows(request.POST)
		if rowForm.is_valid():
			rows = rowForm.cleaned_data['rows']


	rawDataForm = [] 
	activityForm = []

	for i in range(0, rows):
		rawDataForm.append(RawDataForm())
		activityForm.append(ActivityForm())

	return render(request, 'Data/addRawData.html', { 'rawDataForm': rawDataForm, 'activityForm': activityForm,'rowForm': rowForm })


def viewData(request):
	return HttpResponse("view data page")

def uploadData(request):
	return render(request, 'Data/uploadData.html')

