"""
Pages url config
"""

# Django
from django.urls import path

# AA Bulletin Board
from aa_bulletin_board import views

app_name: str = "aa_bulletin_board"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create/", views.create_bulletin, name="create_bulletin"),
    path("bulletin/<slug:slug>/", views.view_bulletin, name="view_bulletin"),
    path("edit/<slug:slug>/", views.edit_bulletin, name="edit_bulletin"),
    path("remove/<slug:slug>/", views.remove_bulletin, name="remove_bulletin"),
]
