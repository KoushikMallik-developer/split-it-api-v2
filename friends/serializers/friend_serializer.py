from typing import Optional
from rest_framework import serializers

from auth_api.export_types.validation_types.validation_result import ValidationResult
from auth_api.services.helpers import validate_user_email
from friends.models.friend import Friend


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"

    def validate(self, data: Optional[dict] = None) -> Optional[bool]:
        is_validated_email = False

        email = data.get("user_email")

        # Friend request receiver Email Validation
        if email and isinstance(email, str):
            validation_result_email: ValidationResult = validate_user_email(email)
            is_validated_email = validation_result_email.is_validated
            if not is_validated_email:
                raise serializers.ValidationError(detail=validation_result_email.error)
        if is_validated_email:
            return True

    # def create(self, data: dict) -> FriendRequest:
    #     email = data.get("user_email")
    #     receiver: User = User.objects.get(email=email)
    #     logging.error(f"Onion -- {receiver}")
    #     if self.validate(data):
    #         friend = FriendRequest(
    #             sender=User(),
    #             receiver=receiver,
    #         )
    #         friend.save()
    #         return friend
