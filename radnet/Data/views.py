from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Data.models import *
    

def index(request):
	return render(request, 'Data/index.html', {})

def addData(request):
	if request.method == 'POST':
		filterform = FilterForm(request.POST)
		try:
			filterform.save();
		except(e):
			print e
		return HttpResponseRedirect('/Data/uploadData/')
	else:
		filterform = FilterForm()

	return render(request, 'Data/addData.html', { 'filterform': filterform, })	

def viewData(request):
	return HttpResponse("view data page")

def uploadData(request):
	return render(request, 'Data/uploadData.html')

