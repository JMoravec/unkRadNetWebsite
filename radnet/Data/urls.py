from django.conf.urls import patterns, url
from Data import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^addData/$', views.addData, name='addData'),
	url(r'^viewData/$', views.viewData, name='viewData'),
	url(r'^uploadData/$', views.uploadData, name='uploadData')
)