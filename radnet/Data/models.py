from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import *


class BetaEfficiency(models.Model):
	coefficient = models.FloatField()

	def __unicode__(self):
		return str(self.coefficient)


class AlphaEfficiency(models.Model):
	coefficient = models.FloatField()

	def __unicode__(self):
		return str(self.coefficient)


class Filter(models.Model):
	filterNum = models.IntegerField(unique=True)
	startDate = models.DateField()
	endDate = models.DateField()
	sampleTime = models.FloatField()
	sampleVolume = models.FloatField()
	timeStart = models.FloatField()
	alphaCoeff = models.ForeignKey(AlphaEfficiency)
	betaCoeff = models.ForeignKey(BetaEfficiency)

	activityCalculated = models.BooleanField()

	def __unicode__(self):
		return str(self.filterNum) + ': ' + str(self.startDate) + ' - ' + str(self.endDate)

	def clean(self):
		#super(models.Model, self).clean()
		if len(str(int(self.timeStart))) != 6:
			raise ValidationError('Time Start must be HHMMSS format')


class RawData(models.Model):
	Filter = models.ForeignKey(Filter)
	time = models.IntegerField()
	alphaReading = models.FloatField()
	betaReading = models.FloatField()
	cleanFilterCount = models.FloatField()

	def __unicode__(self):
		return str(self.Filter) + ' ' + str(self.time)

	def clean(self):
		if len(str(int(self.time))) != 6:
			raise ValidationError('Time must be HHMMSS format')


class Activity(models.Model):
	Filter = models.ForeignKey(Filter)
	RawData = models.ForeignKey(RawData)
	deltaT = models.FloatField()
	alphaAct = models.FloatField()
	betaAct = models.FloatField()

	netAlBet = models.FloatField()
	netBeta = models.FloatField()

	def fillData(self):
		startTime = timeToHours(str(self.Filter.timeStart))
		rawTime = timeToHours(str(self.RawData.time))
		if rawTime < startTime:
			rawTime += 24.0

		self.deltaT = rawTime - startTime
		self.netAlBet = self.RawData.betaReading - self.RawData.cleanFilterCount
		self.netBeta = self.netAlBet - self.RawData.alphaReading
		self.alphaAct = self.RawData.alphaReading * self.Filter.alphaCoeff.coefficient
		self.betaAct = self.netBeta * self.Filter.betaCoeff.coefficient


class AlphaCurve(models.Model):
	Filter = models.ForeignKey(Filter)
	alpha1 = models.FloatField()
	alpha1Lambda = models.FloatField()
	alpha2 = models.FloatField()
	alpha2Lambda = models.FloatField()

	def __unicode__(self):
		return str(self.Filter) + '\n' + str(self.alpha1) + '\n' + str(self.alpha1Lambda) + '\n' + str(self.alpha2) + '\n' + str(self.alpha2Lambda)

class BetaCurve(models.Model):
	Filter = models.ForeignKey(Filter)
	beta1 = models.FloatField()
	beta1Lambda = models.FloatField()
	beta2 = models.FloatField()
	beta2Lambda = models.FloatField()

	def __unicode__(self):
		return str(self.Filter) + '\n' + str(self.beta1) + '\n' + str(self.beta1Lambda) + '\n' + str(self.beta2) + '\n' + str(self.beta2Lambda)

class FilterForm(ModelForm):
	class Meta:
		model = Filter
		widgets = {
			'startDate': SelectDateWidget(),
			'endDate': SelectDateWidget(),
		}
		exclude = ['activityCalculated']

class RawDataForm(ModelForm):
	class Meta:
		model = RawData

class ActivityForm(ModelForm):
	class Meta:
		model = Activity

class AlphaCoeffForm(ModelForm):
	class Meta:
		model = AlphaEfficiency

class BetaCoeffForm(ModelForm):
	class Meta:
		model = BetaEfficiency

class GetFilterForm(forms.Form):
	filterID = forms.ModelChoiceField(queryset=Filter.objects.all(), empty_label=None)

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()

def timeToHours(timeString):
	timeString = str(timeString)
	print timeString
	time = float(timeString[0:2]) + float(timeString[2:4])/60.0 + float(timeString[4:6])/3600.0
	return time