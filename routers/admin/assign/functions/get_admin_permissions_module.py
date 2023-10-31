from . import get_admin_role, get_role_permissions

async def get_admin_permissions(username: str):
    # First, get roles for the given administrator's username
    roles = await get_admin_role(username)
    
    all_permissions = set()  # Use a set to avoid duplicate permissions
    
    for role in roles:
        permissions = await get_role_permissions(role.name)
        all_permissions.update(permissions)
    
    return list(all_permissions)