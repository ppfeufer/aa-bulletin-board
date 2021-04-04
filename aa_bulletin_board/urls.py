"""
pages url config
"""

from django.urls import path

from aa_bulletin_board import views

app_name: str = "aa_bulletin_board"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("create/", views.create_bulletin, name="create_bulletin"),
    path("bulletin/<str:slug>/", views.view_bulletin, name="view_bulletin"),
    path("edit/<str:slug>/", views.edit_bulletin, name="edit_bulletin"),
    path("remove/<str:slug>/", views.remove_bulletin, name="remove_bulletin"),
]
