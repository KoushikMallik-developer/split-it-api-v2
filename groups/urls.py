from django.urls import path

from groups.view.create_group import CreateGroupView

urlpatterns = [
    path("add-group", CreateGroupView.as_view(), name="Create-New-Group"),
]
