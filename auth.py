from database import Database


class AuthManager:
    def __init__(self):
        self.db = Database()
        self.current_user = None

    def login(self, login: str, password: str) -> bool:
        user = self.db.get_user_by_login(login, password)
        if user:
            self.current_user = user
            return True
        return False

    def register(self, fio: str, phone: str, login: str, password: str, user_type: str) -> bool:
        return self.db.register_user(fio, phone, login, password, user_type)

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    def has_permission(self, roles: list) -> bool:
        if not self.current_user:
            return False
        return self.current_user.get('type') in roles