from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ResumeViewSet

urlpatterns = [
    path('resume/', ResumeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='resume'),
    path('resume/export-pdf/', ResumeViewSet.as_view({'get': 'export_pdf'}), name='resume-export-pdf'),
    path('login/', obtain_auth_token, name='api_token_auth'),
]