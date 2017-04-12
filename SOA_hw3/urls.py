"""SOA_hw3 URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from views import index_view
# from views import test_view
from views import login_view
from views import main_view
from views import profile_view
from views import register_view
from views import error_view
from views import predict_view
from views import luis_view
from views import voice_view

urlpatterns = [
    url(r'^$', index_view.index_view, name="Index page"),
    url(r'^index$', index_view.index_view, name="Index page"),
    # url(r'^get_snapshot$', test_view.test_view, name="Test upload image"),
    url(r'^login_face_jump$', login_view.login_with_face_jump, name="Login jump 1"),
    # Deprecated
    # url(r'^login_password$', login_view.login_with_password, name="Login with password"),
    url(r'^login_pw_jump$', login_view.login_with_password_jump, name="Login jump 2"),
    url(r'^logout$', login_view.logout, name="Logout"),
    url(r'^register$', register_view.register, name="Register"),
    url(r'^register_jump$', register_view.register_jump, name="Register jump"),
    url(r'^add_face$', profile_view.add_face, name="Add face"),
    url(r'^add_face_jump$', profile_view.add_face_jump, name="Add face jump"),
    url(r'^profile$', profile_view.profile_view, name="User profile view"),
    url(r'^main$', main_view.main_view, name="Main menu"),
    url(r'^predict$', predict_view.predict_view, name="Predict view"),
    url(r'^luis$', luis_view.luis_view, name="Language understanding API"),
    url(r'^voice_accumulate$', voice_view.voice_acc, name="Voice Accumulation"),
    url(r'^voice_digest$', voice_view.voice_view, name="Digest recorded voice"),
    url(r'^error$', error_view.error_view, name="Error view"),
    url(r'^.*?$', index_view.index_view, name="Error"),
    url(r'^admin/', admin.site.urls),
]

# To avoid conflict with the cloud
from django.contrib.auth.models import User
User.objects.all().delete()
