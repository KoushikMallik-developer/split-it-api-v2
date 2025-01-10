from auth_api.export_types.validation_types.validation_result import ValidationResult
from groups.models.group import Group


def validate_group_uid(group_uid: str) -> ValidationResult:
    existing_group = True if Group.objects.filter(id=group_uid).count() > 0 else False
    if existing_group:
        return ValidationResult(
            is_validated=True,
            error=None,
        )
    return ValidationResult(is_validated=False, error="Group does not exists.")
