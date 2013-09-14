from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget


class BetaEfficiency(models.Model):
	coefficient = models.FloatField()

	def __unicode__(self):
		return self.coefficient


class AlphaEfficiency(models.Model):
	coefficient = models.FloatField()

	def __unicode__(self):
		return self.coefficient


class Filter(models.Model):
	filterNum = models.IntegerField(unique=True)
	startDate = models.DateField()
	endDate = models.DateField()
	sampleTime = models.FloatField()
	sampleVolume = models.FloatField()
	timeStart = models.FloatField()
	alphaCoeff = models.ForeignKey(AlphaEfficiency)
	betaCoeff = models.ForeignKey(BetaEfficiency)

	def __unicode__(self):
		return str(self.startDate) + ' - ' + str(self.endDate)

class RawData(models.Model):
	Filter = models.ForeignKey(Filter)
	time = models.IntegerField()
	alphaReading = models.FloatField()
	betaReading = models.FloatField()
	cleanFilterCount = models.FloatField()

	def __unicode__(self):
		return str(self.Filter) + ' ' + str(self.time)


class Activity(models.Model):
	filterID = models.ForeignKey(Filter)
	rawData = models.ForeignKey(RawData)
	deltaT = models.FloatField()
	alphaAct = models.FloatField()
	betaAct = models.FloatField()


class AlphaCurve(models.Model):
	filterID = models.ForeignKey(Filter)
	alpha1 = models.FloatField()
	alpha1Lambda = models.FloatField()
	alpha2 = models.FloatField()
	alpha2Lambda = models.FloatField()


class BetaCurve(models.Model):
	filterID = models.ForeignKey(Filter)
	beta1 = models.FloatField()
	beta1Lambda = models.FloatField()
	beta2 = models.FloatField()
	beta2Lambda = models.FloatField()

class FilterForm(ModelForm):
	class Meta:
		model = Filter
		widgets = {
			'startDate': SelectDateWidget(),
			'endDate': SelectDateWidget(),
		}

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

class rawDataRows(forms.Form):
	rows = forms.IntegerField()