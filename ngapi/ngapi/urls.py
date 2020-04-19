"""ngapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from task.views import MovieListView, CommentListView, TopListView

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^movie/$', MovieListView.as_view(), name='movie-list'),
    url(r'^comment/$', CommentListView.as_view(), name='comment-list'),
    url(r'^top/$', TopListView.as_view(), name='top-list')

    # url(r'^api/account/(?P<id>[0-9]+)/$', AccountView.as_view(), name='accountcount'),
    # url(r'^api/.*', WrongEndpointView.as_view(), name='wrong-endpoint'),
]
