from django.urls import path

from groups.view.add_members import AddMemberView
from groups.view.create_group import CreateGroupView

urlpatterns = [
    path("add-group", CreateGroupView.as_view(), name="Create-New-Group"),
    path("add-member", AddMemberView.as_view(), name="Add-Member"),
]
