"""
pages url config
"""

from django.urls import path

from aa_bulletin_board import views


app_name: str = "aa_bulletin_board"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("<str:slug>/", views.view_bulletin, name="view_bulletin"),
]
