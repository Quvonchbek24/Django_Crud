from django.urls import path
from .views import sign_up, sign_in, sign_out

urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', sign_in, name='sign_in'),
    path('sign-out/', sign_out, name='sign_out'),
]
