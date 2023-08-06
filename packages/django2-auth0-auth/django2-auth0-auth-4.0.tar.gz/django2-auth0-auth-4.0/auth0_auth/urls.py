from django.urls import path
from .views import auth, callback, logout


urlpatterns = [
    path('login/', auth, name='auth0_login'),
    path('logout/', logout, name='auth0_logout'),
    path('callback/', callback, name='auth0_callback'),
]
