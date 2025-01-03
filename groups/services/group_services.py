from groups.export_types.create_group import CreateGroupRequestType


class GroupServices:
    @staticmethod
    def create_new_group_service(
        request_data: CreateGroupRequestType, uid: str
    ) -> dict:
        print(f"request_data__{request_data}")
        print(f"uid__{uid}")
        return {"successMessage": None, "errorMessage": "None215"}
