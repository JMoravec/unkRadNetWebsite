import sys
import traceback
from django.http import HttpResponseRedirect
from django.shortcuts import render
from Data.models import *
from calculate import fitToCurve
from datetime import datetime


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
            return render(request, 'Data/addFilter.html', {'filterform':
                          filterform})
    else:
        filterform = FilterForm()

    return render(request, 'Data/addFilter.html',
                  {'filterform': filterform, })


def addCoefficients(request, typeID=0):
    if request.method == 'POST' and str(typeID) == str(1):
        alphaForm = AlphaCoeffForm(request.POST)
        if alphaForm.is_valid():
            try:
                AlphaEfficiency.objects.\
                    get(coefficient=alphaForm.cleaned_data['coefficient'])
            except:
                alphaForm.save()

        betaForm = BetaCoeffForm()
    elif request.method == 'POST' and str(typeID) == str(2):
        betaForm = BetaCoeffForm(request.POST)
        if betaForm.is_valid():
            try:
                BetaEfficiency.objects.\
                    get(coefficient=betaForm.cleaned_data['coefficient'])
            except:
                betaForm.save()

        alphaForm = AlphaCoeffForm()
    else:
        alphaForm = AlphaCoeffForm()
        betaForm = BetaCoeffForm()

    return render(request, 'Data/addCoeffs.html',
                  {'alphaForm': alphaForm,
                   'betaForm': betaForm, })


def addRawData(request):
    if (request.method == 'POST'):
        rawDataForm = RawDataForm(request.POST)
        try:
            if rawDataForm.is_valid():
                rawDataForm.save()
                return HttpResponseRedirect('/Data/AddRawData/')
            else:
                return render(request, 'Data/addRawData.html',
                              {'rawDataForm': rawDataForm, })
        except:
            return render(request, 'Data/addRawData.html',
                          {'rawDataForm': rawDataForm, })

    rawDataForm = RawDataForm()

    return render(request, 'Data/addRawData.html',
                  {'rawDataForm': rawDataForm, })


def checkData(request, filter_id=0):
    if (request.method == 'POST' and filter_id == 0):
        getFilterForm = GetFilterForm(request.POST)
        if getFilterForm.is_valid():
            selection = getFilterForm.cleaned_data['filterID']
            return HttpResponseRedirect('/Data/AddRawData/CheckData/' +
                                        str(selection.id) + '/')
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
            return HttpResponseRedirect('/Data/FitToCurve/' +
                                        str(filter_id) + '/')
        else:
            HttpResponseRedirect('/Data/ViewData/' + str(filter_id) + '/')
    elif filter_id != 0:
        try:
            mainFilter = Filter.objects.get(id=filter_id)
            if mainFilter.activityCalculated:
                return HttpResponseRedirect('/Data/ViewData/' +
                                            str(filter_id) + '/')
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
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value,
                                               exc_traceback)
            print ''.join('!! ' + line for line in lines)
            getFilterForm = GetFilterForm()
            filter_id = 0
            mainFilter = None
            activityData = None
    else:
        getFilterForm = GetFilterForm()
        mainFilter = None
        activityData = None
    context = {'getFilterForm': getFilterForm,
               'filter_id': filter_id,
               'mainFilter': mainFilter,
               'activityData': activityData, }
    return render(request, 'Data/checkData.html', context)


def viewData(request, filter_id=0):
    if request.method == 'POST':
        getFilterForm = GetFilterForm(request.POST)
        if getFilterForm.is_valid():
            selection = getFilterForm.cleaned_data['filterID']
            return HttpResponseRedirect('/Data/ViewData/' +
                                        str(selection.id) + '/')
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
    context = {'getFilterForm': getFilterForm,
               'filter_id': filter_id,
               'activity': activity,
               'mainFilter': mainFilter, }
    return render(request, 'Data/viewData.html', context)


def fitCurve(request, filter_id=0):
    try:
        alphaCurve = AlphaCurve.objects.get(Filter=filter_id)
        betaCurve = BetaCurve.objects.get(Filter=filter_id)
        context = {'alphaCurve': alphaCurve,
                   'betaCurve': betaCurve, }
        return render(request, 'Data/fitCurve.html', context)
    except:
        if filter_id == 0:
            return HttpResponseRedirect('/Data/')
        else:
            fitToCurve(filter_id)
            return HttpResponseRedirect('/Data/FitToCurve/' +
                                        str(filter_id) + '/')


def uploadData(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filterid = uploadDataFromFile(request.FILES['file'])
            if filterid is None:
                filterid = 0
            return HttpResponseRedirect('/Data/AddRawData/CheckData/' +
                                        str(filterid) + '/')
    else:
        form = UploadFileForm()
    return render(request, 'Data/uploadData.html', {'form': form, })


def uploadDataFromFile(fileStuff):
    filterID = None
    with open(fileStuff.name, 'wb+') as destination:
        for chunk in fileStuff.chunks():
            destination.write(chunk)

    with open(fileStuff.name, 'rb') as f:
        try:
            #get initial values
            dataFilterNum = f.readline().rstrip()
            startDate = f.readline().rstrip()
            endDate = f.readline().rstrip()
            sampleTime = f.readline().rstrip()
            sampleVol = f.readline().rstrip()

            for line in f:
                # check if no line if len(line) != 0:
                    # check for comment lines
                    if line[0] != '#':
                        # Check if it's the initial value for time and set it
                        # this part is for the old typed data which didn't
                        # have the calibration numbers in the data textfile
                        if ',' not in line:
                            timeStart = timeToHours(line)
                            alphaCal = 1.63
                            betaCal = 1.15
                        elif len(line.split(',')) == 3:
                            timeStart, alphaCal, betaCal = \
                                line.rstrip().split(',')
                            timeStart = timeToHours(timeStart)
                            alphaCal = float(alphaCal)
                            betaCal = float(betaCal)

                        if ',' not in line or len(line.split(',')) == 3:
                            #check database to see if alphaCal is in already
                            if not AlphaEfficiency.\
                                    objects.filter(coefficient=alphaCal).\
                                    exists():
                                alphaEff = AlphaEfficiency()
                                alphaEff.coefficient = alphaCal
                                alphaEff.save()
                            else:
                                alphaEff = AlphaEfficiency.objects.\
                                    get(coefficient=alphaCal)

                            # check database to see if betaCal is in already
                            if not BetaEfficiency.objects.\
                                    filter(coefficient=betaCal).exists():
                                betaEff = BetaEfficiency()
                                betaEff.coefficient = betaCal
                                betaEff.save()
                            else:
                                betaEff = BetaEfficiency.objects.\
                                    get(coefficient=betaCal)

                            #make new filter entry if it doesn't exists
                            if not Filter.objects.\
                                    filter(filterNum=dataFilterNum).exists():
                                mainFilter = Filter()
                                mainFilter.filterNum = dataFilterNum
                                mainFilter.startDate = \
                                    datetime.strptime(startDate, '%Y%m%d').\
                                    date()
                                mainFilter.endDate = \
                                    datetime.strptime(endDate, '%Y%m%d').date()
                                mainFilter.sampleTime = sampleTime
                                mainFilter.sampleVolume = sampleVol
                                mainFilter.timeStart = timeStart
                                mainFilter.alphaCoeff = alphaEff
                                mainFilter.betaCoeff = betaEff
                                mainFilter.save()
                                mainFilter = Filter.objects.\
                                    get(filterNum=dataFilterNum)
                            else:
                                mainFilter = Filter.objects.\
                                    get(filterNum=dataFilterNum)
                            filterID = mainFilter.id
                        else:
                            #Set the values for each line
                            #det2 is beta+Alpha reading
                            #det1 is alpha reading
                            #cfc is clean filter count
                            time, det2, cfc, det1 = line.rstrip().split(',')
                            rawTime = time
                            det2 = int(det2)
                            cfc = int(cfc)
                            det1 = int(det1)

                            if not RawData.objects.\
                                    filter(Filter=mainFilter, time=rawTime):
                                newRawData = RawData()
                                newRawData.Filter = mainFilter
                                newRawData.time = rawTime
                                newRawData.alphaReading = det1
                                newRawData.betaReading = det2
                                newRawData.cleanFilterCount = cfc
                                newRawData.save()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type,
                                               exc_value, exc_traceback)
            print ''.join('!! ' + line for line in lines)
    return filterID
