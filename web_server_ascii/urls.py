"""web_server_ascii URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from ascii_app.views import test, convert_to_ascii_view, main_page
from ascii_app.tests import main_test
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    url(r'^$', main_page),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/test$', test),
    url(r'^api/process$', convert_to_ascii_view)

]
# In case of debug false it will be disabled automatically
urlpatterns += static("/", document_root=settings.STATIC_ROOT)
