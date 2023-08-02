"""
Pages url config
"""

# Django
from django.urls import path

# AA Bulletin Board
from aa_bulletin_board import views

app_name: str = "aa_bulletin_board"

urlpatterns = [
    path(route="", view=views.dashboard, name="dashboard"),
    path(route="create/", view=views.create_bulletin, name="create_bulletin"),
    path(route="bulletin/<slug:slug>/", view=views.view_bulletin, name="view_bulletin"),
    path(route="edit/<slug:slug>/", view=views.edit_bulletin, name="edit_bulletin"),
    path(
        route="remove/<slug:slug>/", view=views.remove_bulletin, name="remove_bulletin"
    ),
]
