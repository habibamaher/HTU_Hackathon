from django.urls import path
from . import views

urlpatterns = [
    # The home view handles both the initial page load (GET) and the chat submission (POST via AJAX)
    path('', views.home, name='home'),
]
