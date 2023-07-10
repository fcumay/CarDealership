from django.urls import path
from .views import RetrieveUserView, RegisterViewAPI

urlpatterns = [
    path("register", RegisterViewAPI.as_view()),
    path('me', RetrieveUserView.as_view()),

]
