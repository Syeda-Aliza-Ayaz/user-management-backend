def has_permission(user, code):
    if user.is_superuser:
        return True
    if code == "can_view_users" and user.userpermission_set.filter(permission__code="can_delete_users").exists():
        return True
    return user.userpermission_set.filter(permission__code=code).exists()