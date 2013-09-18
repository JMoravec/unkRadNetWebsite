from django.conf.urls import patterns, url
from Data import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^AddData/$', views.addData, name='addData'),
	url(r'^ViewData/$', views.viewData, name='viewData'),
	url(r'^ViewData/(?P<filter_id>\d+)/$', views.viewData, name='viewData'),
	url(r'^UploadData/$', views.uploadData, name='uploadData'),
	url(r'^AddFilter/$', views.addFilter, name='addFilter'),
	url(r'^AddRawData/$', views.addRawData, name='addRawData'),
	url(r'^AddRawData/CheckData/$', views.checkData, name='checkData'),
	url(r'^AddRawData/CheckData/(?P<filter_id>\d+)/$', views.checkData, name='checkData'),
)