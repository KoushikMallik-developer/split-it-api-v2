from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from groups.export_types.group_types.export_group import ExportGroup, ExportGroupList
from groups.export_types.request_data_type.add_member import AddMemberRequestType
from groups.export_types.request_data_type.create_group import CreateGroupRequestType
from groups.export_types.request_data_type.delete_group import DeleteGroupRequestType
from groups.export_types.request_data_type.search_group import SearchGroupRequestType
from groups.export_types.request_data_type.update_group import UpdateGroupRequestType
from groups.group_exceptions.group_exceptions import (
    MemberNotAddedError,
    NotAnGroupAdminError,
    GroupUpdateFailed,
    GroupNotFoundError,
)
from groups.models.group import Group
from groups.serializers.add_member_serializer import AddMemberSerializer
from groups.serializers.group_serializer import GroupSerializer


class GroupServices:
    @staticmethod
    def create_new_group_service(
        request_data: CreateGroupRequestType, uid: str
    ) -> dict:
        data: dict = {"request_data": request_data, "uid": uid}
        group: Group = GroupSerializer().create(data)
        return {
            "message": f"Group {group.name} is created",
            "data": ExportGroup(**group.model_to_dict()).model_dump(),
        }

    @staticmethod
    def add_member_group_service(request_data: AddMemberRequestType, uid: str) -> dict:
        data: dict = {"request_data": request_data, "uid": uid}
        group: Group = AddMemberSerializer().create(data)
        if group:
            return {
                "message": f"Member {request_data.user_email} is added in group {group.name}",
                "data": ExportGroup(**group.model_to_dict()).model_dump(),
            }
        else:
            raise MemberNotAddedError()

    @staticmethod
    def update_group(uid: str, request_data: UpdateGroupRequestType):
        try:
            if Group.objects.filter(id=request_data.group_id).exists():
                group: Group = Group.objects.get(id=request_data.group_id)
                if str(group.creator.id) != uid:
                    raise NotAnGroupAdminError()

                if not request_data.name and not request_data.image:
                    raise GroupUpdateFailed()

                if (
                    request_data.name
                    and isinstance(request_data.name, str)
                    and len(request_data.name) > 0
                ):
                    group.name = request_data.name

                if request_data.image and isinstance(request_data.image, str):
                    group.image = request_data.image

                group.save()
                return ExportGroup(**group.model_to_dict()).model_dump()
        except ObjectDoesNotExist:
            raise GroupNotFoundError()

    @staticmethod
    def remove_group(uid: str, request_data: DeleteGroupRequestType):
        try:
            if Group.objects.filter(id=request_data.group_id).exists():
                group: Group = Group.objects.get(id=request_data.group_id)
                if str(group.creator.id) != uid:
                    raise NotAnGroupAdminError()

                group.delete()
            else:
                raise GroupNotFoundError()
        except ObjectDoesNotExist:
            raise GroupNotFoundError()

    @staticmethod
    def get_all_groups_service(uid: str) -> Optional[list]:
        groups = Group.objects.filter(members__id=uid)
        if groups.exists():
            all_groups = ExportGroupList(
                group_list=[ExportGroup(**group.model_to_dict()) for group in groups]
            )
            return all_groups.model_dump().get("group_list")
        else:
            return None

    @staticmethod
    def get_searched_groups(
        request_data: SearchGroupRequestType, user_id: str
    ) -> Optional[list]:
        try:
            keywords = request_data.keyword.split(" ")
            query = Q()
            for keyword in keywords:
                query |= Q(name__icontains=keyword) | Q(description__icontains=keyword)

            groups = Group.objects.filter(members__id=user_id).filter(query)

            if groups.exists():
                all_groups = [
                    ExportGroup(**group.model_to_dict()) for group in groups
                ]
                return (
                    ExportGroupList(group_list=all_groups, user_id=user_id)
                    .model_dump()
                    .get("group_list")
                )
            else:
                return None

        except ObjectDoesNotExist:
            raise GroupNotFoundError()
