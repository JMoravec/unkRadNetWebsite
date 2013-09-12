from django.db import models


class BetaEfficiency(models.Model):
	coefficient = models.FloatField()


class AlphaEfficiency(models.Model):
	coefficient = models.FloatField()


class Filter(models.Model):
	filterNum = models.IntegerField(unique=True)
	startDate = models.DateField()
	endDate = models.DateField()
	sampleTime = models.FloatField()
	sampleVolume = models.FloatField()
	timeStart = models.FloatField()
	alphaCoeff = models.ForeignKey(AlphaEfficiency)
	betaCoeff = models.ForeignKey(BetaEfficiency)

class RawData(models.Model):
	Filter = models.ForeignKey(Filter)
	time = models.IntegerField()
	alphaReading = models.FloatField()
	betaReading = models.FloatField()
	cleanFilterCount = models.FloatField()


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