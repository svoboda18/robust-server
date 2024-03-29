"""
URL configuration for sequantchy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path

from user import urls as user_urls
from fcm import urls as fcm_urls
from search_indexes import urls as index_urls
from startup import urls as startup_urls

apipatterns = [
    re_path(r'^user/?', include(user_urls)),
    re_path(r'^fcm/?', include(fcm_urls)),
    re_path(r'^search/?', include(index_urls)),
    re_path(r'^startup/?', include(startup_urls)),
]

urlpatterns = [
    re_path(r'^admin/?', admin.site.urls),
    re_path(r'^api/?', include(apipatterns)),
]
