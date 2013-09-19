from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Data.models import *
from calculate import fitToCurve
    

def index(request):
	return render(request, 'Data/index.html')


def addData(request):
	return render(request, 'Data/addData.html')


def addFilter(request):
	if request.method == 'POST':
		filterform = FilterForm(request.POST)
		try:
			filterform.save()
			return HttpResponseRedirect('/Data/AddData/')
		except:
			return render(request, 'Data/addFilter.html', {'filterform': filterform})
	else:
		filterform = FilterForm()

	return render(request, 'Data/addFilter.html', { 'filterform': filterform, })	


def addRawData(request):
	if (request.method == 'POST'):
		rawDataForm = RawDataForm(request.POST)
		try:
			print rawDataForm.is_valid()
			if rawDataForm.is_valid():
				rawDataForm.save()
				return HttpResponseRedirect('/Data/AddRawData/')
			else:
				return render(request, 'Data/addRawData.html', { 'rawDataForm': rawDataForm,})	
		except:
			return render(request, 'Data/addRawData.html', { 'rawDataForm': rawDataForm,})
		
	rawDataForm = RawDataForm()

	return render(request, 'Data/addRawData.html', { 'rawDataForm': rawDataForm,})


def checkData(request, filter_id=0):
	if (request.method == 'POST' and filter_id == 0):
		getFilterForm = GetFilterForm(request.POST)
		if getFilterForm.is_valid():
			selection = getFilterForm.cleaned_data['filterID']
			return HttpResponseRedirect('/Data/AddRawData/CheckData/' + str(selection.id) + '/')
	elif (request.method == 'POST' and filter_id != 0):
		mainFilter = Filter.objects.get(id=filter_id)
		if not mainFilter.activityCalculated:
			rawData = RawData.objects.filter(Filter=filter_id)
			rawData = rawData.order_by('time')
			for data in rawData:
				activity = Activity()
				activity.Filter = mainFilter
				activity.RawData = data
				activity.fillData()
				activity.save()
			mainFilter.activityCalculated = True
			mainFilter.save()
			return HttpResponseRedirect('/Data/FitToCurve/' + str(filter_id) + '/')
		else:
			HttpResponseRedirect('/Data/ViewData/' + str(filter_id) + '/')
	elif filter_id != 0:
		try:
			mainFilter = Filter.objects.get(id=filter_id)
			if mainFilter.activityCalculated:
				return HttpResponseRedirect('/Data/ViewData/' + str(filter_id) + '/')
			rawData = RawData.objects.filter(Filter=filter_id)
			rawData = rawData.order_by('time')
			activityData = []
			for data in rawData:
				activity = Activity()
				activity.Filter = mainFilter
				activity.RawData = data
				activity.fillData()
				activityData.append(activity)
			getFilterForm = None
		except:
			getFilterForm = GetFilterForm()
			filter_id = 0
			mainFilter = None
			activityData = None
	else:
		getFilterForm = GetFilterForm()			
		mainFilter = None
		activityData = None
	context ={ 'getFilterForm': getFilterForm, 'filter_id': filter_id, 'mainFilter': mainFilter, 'activityData': activityData} 
	return render(request, 'Data/checkData.html', context)


def viewData(request, filter_id=0):
	if request.method == 'POST':
		getFilterForm = GetFilterForm(request.POST)
		if getFilterForm.is_valid():
			selection = getFilterForm.cleaned_data['filterID']
			return HttpResponseRedirect('/Data/ViewData/' + str(selection.id) + '/')
	elif (filter_id != 0):
		try:
			mainFilter = Filter.objects.get(id=filter_id)
			activity = Activity.objects.filter(Filter=filter_id)
			activity = activity.order_by('deltaT')
			getFilterForm = None
		except:
			filter_id = 0
			mainFilter = None
			activity = None		
	else:
		mainFilter = None
		activity = None
	getFilterForm = GetFilterForm()
	context = {'getFilterForm': getFilterForm, 'filter_id': filter_id, 'activity': activity, 'mainFilter': mainFilter,}
 	return render(request, 'Data/viewData.html', context)


def fitCurve(request, filter_id=0):
	try:
		alphaCurve = AlphaCurve.objects.get(Filter=filter_id)
		betaCurve = BetaCurve.objects.get(Filter=filter_id)
		context = {'alphaCurve': alphaCurve, 'betaCurve': betaCurve,}
		return render(request, 'Data/fitCurve.html', context)
	except:
		if filter_id == 0:
			return HttpResponseRedirect('/Data/')
		else: 
			print filter_id
			fitToCurve(filter_id)
			return HttpResponseRedirect('/Data/FitToCurve/' + str(filter_id) + '/')



def uploadData(request):
	return render(request, 'Data/uploadData.html')
