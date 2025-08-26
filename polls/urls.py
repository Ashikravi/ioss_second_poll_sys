from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('poll/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('poll/<int:poll_id>/vote/', views.vote, name='vote'),
    path('poll/<int:poll_id>/results/', views.poll_results, name='poll_results'),
    path('poll/<int:poll_id>/results/json/', views.poll_results_json, name='poll_results_json'),
    path('poll/<int:poll_id>/export/', views.export_results_csv, name='export_results'),
    path('my-votes/', views.my_votes, name='my_votes'),
    path('register/', views.register_view, name='register'),
    
]
