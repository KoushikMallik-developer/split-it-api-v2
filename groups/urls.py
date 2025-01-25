from django.urls import path

from groups.view.add_members import AddMemberView
from groups.view.create_group import CreateGroupView
from groups.view.get_all_groups import GetAllGroupView
from groups.view.remove_group import RemoveGroupView
from groups.view.search_group import SearchGroupView
from groups.view.update_group import UpdateGroupView

urlpatterns = [
    path("add-group", CreateGroupView.as_view(), name="Create-New-Group"),
    path("add-member", AddMemberView.as_view(), name="Add-Member"),
    path("update-group", UpdateGroupView.as_view(), name="Update-Group"),
    path("remove-group", RemoveGroupView.as_view(), name="Remove-Group"),
    path("search-group", SearchGroupView.as_view(), name="Search-Group"),
    path("get-all-group", GetAllGroupView.as_view(), name="Get-all-Group"),
]
