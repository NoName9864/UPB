from auth import AuthManager
from windows import AppWindows

def main():
    auth_manager = AuthManager()
    app = AppWindows(auth_manager)
    app.show_login_window()

if __name__ == "__main__":
    main()