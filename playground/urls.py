# mao urls to view functions
from django.urls import path
from .views import sayHello, contact_view

urlpatterns = [
    # path("greeting/", greeting),
    # path("fullname/",fullName),
    path("sayhello/",sayHello),
    path('contact/',contact_view, name='contact')
    # path("sum/<int:a>/<int:b>",sumNumbers),
    # path("multiply/<int:a>/<int:b>/<int:c>", multiplyNumbers)
]