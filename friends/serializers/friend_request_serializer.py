from typing import Optional
from rest_framework import serializers

from auth_api.auth_exceptions.user_exceptions import UserNotFoundError
from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.services.helpers import validate_user_email
from friends.models.friend_request import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        is_validated_email = False

        email = data.get("user_email")

        # Friend request receiver Email Validation
        if email and isinstance(email, str):
            validation_result_email: ValidationResult = validate_user_email(email)
            is_validated_email = validation_result_email.is_validated
            if not is_validated_email:
                raise UserNotFoundError(msg="This user not registered with us.")
        if is_validated_email:
            return True
