"""
Granular Role-Based Access Control (RBAC) Matrix
"""
class RBACMatrix:
    ROLES = {
        "GUEST": {
            "problems:view", "contests:view", "courses:view"
        },
        "USER": {
            "problems:view", "problems:submit",
            "contests:view", "contests:join",
            "courses:view", "courses:enroll",
            "projects:create", "projects:edit", "projects:delete",
            "profile:edit", "ai:assist"
        },
        "INSTRUCTOR": {
            "problems:view", "problems:submit", "problems:create",
            "courses:view", "courses:create", "courses:manage",
            "projects:create", "projects:edit", "projects:delete",
            "profile:edit", "ai:assist"
        },
        "MODERATOR": {
            "problems:view", "problems:manage",
            "contests:view", "contests:manage",
            "content:moderate", "users:flag"
        },
        "ADMIN": {
            "*"  # Wildcard superuser
        }
    }

    @classmethod
    def has_permission(cls, role: str, permission: str) -> bool:
        r = (role or "GUEST").upper()
        perms = cls.ROLES.get(r, set())
        if "*" in perms:
            return True
        return permission in perms
