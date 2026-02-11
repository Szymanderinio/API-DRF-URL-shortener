from django.urls import path

from .views import ExpandURLView, RedirectView, ShortenURLView

urlpatterns = [
    path('api/shorten/', ShortenURLView.as_view(), name='shorten'),
    path('api/expand/<str:short_code>/', ExpandURLView.as_view(), name='expand'),
    path('s/<str:short_code>/', RedirectView.as_view(), name='redirect'),
]
