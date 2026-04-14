import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime


class AppWindows:
    def __init__(self, auth_manager):
        self.auth_manager = auth_manager
        self.db = auth_manager.db
        self.current_window = None

    def clear_window(self):
        """Очистка текущего окна"""
        if self.current_window:
            self.current_window.destroy()

    def show_login_window(self):
        """Страница входа"""
        self.clear_window()
        self.current_window = tk.Tk()
        self.current_window.title("Авторизация - Сервисный центр")
        self.current_window.geometry("400x350")
        self.current_window.resizable(False, False)

        # Заголовок
        tk.Label(self.current_window, text="Добро пожаловать!",
                 font=("Arial", 20, "bold")).pack(pady=30)

        # Форма входа
        frame = tk.Frame(self.current_window)
        frame.pack(pady=20)

        tk.Label(frame, text="Логин:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10)
        self.login_entry = tk.Entry(frame, font=("Arial", 12), width=25)
        self.login_entry.grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Пароль:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10)
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=25)
        self.password_entry.grid(row=1, column=1, pady=10)

        # Кнопки
        btn_frame = tk.Frame(self.current_window)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Войти", command=self.do_login,
                  bg="#4CAF50", fg="white", font=("Arial", 12), width=15).pack(pady=5)
        tk.Button(btn_frame, text="Регистрация", command=self.show_register_window,
                  bg="#2196F3", fg="white", font=("Arial", 12), width=15).pack(pady=5)

        self.current_window.mainloop()

    def do_login(self):
        """Обработка входа"""
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return

        if self.auth_manager.login(login, password):
            user = self.auth_manager.get_current_user()
            messagebox.showinfo("Успех", f"Добро пожаловать, {user['fio']}!")
            self.show_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_register_window(self):
        """Страница регистрации"""
        self.clear_window()
        self.current_window = tk.Tk()
        self.current_window.title("Регистрация - Сервисный центр")
        self.current_window.geometry("450x500")
        self.current_window.resizable(False, False)

        tk.Label(self.current_window, text="Регистрация нового пользователя",
                 font=("Arial", 18, "bold")).pack(pady=20)

        frame = tk.Frame(self.current_window)
        frame.pack(pady=20)

        tk.Label(frame, text="ФИО:", font=("Arial", 11)).grid(row=0, column=0, pady=8, padx=10, sticky="e")
        self.fio_entry = tk.Entry(frame, font=("Arial", 11), width=30)
        self.fio_entry.grid(row=0, column=1, pady=8)

        tk.Label(frame, text="Телефон:", font=("Arial", 11)).grid(row=1, column=0, pady=8, padx=10, sticky="e")
        self.phone_entry = tk.Entry(frame, font=("Arial", 11), width=30)
        self.phone_entry.grid(row=1, column=1, pady=8)

        tk.Label(frame, text="Логин:", font=("Arial", 11)).grid(row=2, column=0, pady=8, padx=10, sticky="e")
        self.reg_login_entry = tk.Entry(frame, font=("Arial", 11), width=30)
        self.reg_login_entry.grid(row=2, column=1, pady=8)

        tk.Label(frame, text="Пароль:", font=("Arial", 11)).grid(row=3, column=0, pady=8, padx=10, sticky="e")
        self.reg_password_entry = tk.Entry(frame, show="*", font=("Arial", 11), width=30)
        self.reg_password_entry.grid(row=3, column=1, pady=8)

        tk.Label(frame, text="Подтверждение пароля:", font=("Arial", 11)).grid(row=4, column=0, pady=8, padx=10,
                                                                               sticky="e")
        self.confirm_password_entry = tk.Entry(frame, show="*", font=("Arial", 11), width=30)
        self.confirm_password_entry.grid(row=4, column=1, pady=8)

        tk.Label(frame, text="Тип пользователя:", font=("Arial", 11)).grid(row=5, column=0, pady=8, padx=10, sticky="e")
        self.user_type_var = tk.StringVar(value="Заказчик")
        user_types = ["Заказчик", "Мастер"]
        user_type_menu = ttk.Combobox(frame, textvariable=self.user_type_var, values=user_types, state="readonly",
                                      width=27)
        user_type_menu.grid(row=5, column=1, pady=8)

        btn_frame = tk.Frame(self.current_window)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Зарегистрироваться", command=self.do_register,
                  bg="#4CAF50", fg="white", font=("Arial", 12), width=20).pack(pady=5)
        tk.Button(btn_frame, text="Назад к входу", command=self.show_login_window,
                  bg="#9E9E9E", fg="white", font=("Arial", 12), width=20).pack(pady=5)

        self.current_window.mainloop()

    def do_register(self):
        """Обработка регистрации"""
        fio = self.fio_entry.get()
        phone = self.phone_entry.get()
        login = self.reg_login_entry.get()
        password = self.reg_password_entry.get()
        confirm = self.confirm_password_entry.get()
        user_type = self.user_type_var.get()

        if not all([fio, phone, login, password]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        if password != confirm:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        if self.auth_manager.register(fio, phone, login, password, user_type):
            messagebox.showinfo("Успех", "Регистрация успешна! Теперь войдите в систему.")
            self.show_login_window()
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")

    def show_main_window(self):
        """Главное окно (в зависимости от роли)"""
        self.clear_window()
        self.current_window = tk.Tk()
        self.current_window.title("Сервисный центр - Главная")
        self.current_window.geometry("1200x700")

        user = self.auth_manager.get_current_user()
        user_type = user['type']

        # Меню
        menubar = tk.Menu(self.current_window)
        self.current_window.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выйти", command=self.logout)

        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

        # Верхняя панель
        top_frame = tk.Frame(self.current_window, bg="#f0f0f0", height=80)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text=f"Сервисный центр \"ТехноМастер\"",
                 font=("Arial", 18, "bold"), bg="#f0f0f0").pack(side="left", padx=20, pady=20)

        user_info = f"Пользователь: {user['fio']} ({user['type']})"
        tk.Label(top_frame, text=user_info, font=("Arial", 11), bg="#f0f0f0").pack(side="right", padx=20, pady=25)

        # Основная область
        self.main_frame = tk.Frame(self.current_window)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Боковое меню
        sidebar = tk.Frame(self.main_frame, width=200, bg="#e0e0e0", relief="sunken", bd=1)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        # Кнопки в боковом меню в зависимости от роли
        if user_type in ['Администратор', 'Менеджер', 'Оператор']:
            tk.Button(sidebar, text="Все заявки", command=self.show_all_requests,
                      bg="#2196F3", fg="white", font=("Arial", 11), width=18, pady=5).pack(pady=10)
            tk.Button(sidebar, text="Новая заявка", command=self.show_add_request,
                      bg="#4CAF50", fg="white", font=("Arial", 11), width=18, pady=5).pack(pady=10)

        if user_type == 'Мастер':
            tk.Button(sidebar, text="Мои заявки", command=self.show_master_requests,
                      bg="#FF9800", fg="white", font=("Arial", 11), width=18, pady=5).pack(pady=10)

        if user_type == 'Заказчик':
            tk.Button(sidebar, text="Мои заявки", command=self.show_client_requests,
                      bg="#FF9800", fg="white", font=("Arial", 11), width=18, pady=5).pack(pady=10)
            tk.Button(sidebar, text="Новая заявка", command=self.show_add_request,
                      bg="#4CAF50", fg="white", font=("Arial", 11), width=18, pady=5).pack(pady=10)

        # Область контента
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Приветственное сообщение
        tk.Label(self.content_frame, text="Добро пожаловать в систему управления заявками!",
                 font=("Arial", 16), fg="#333").pack(expand=True, pady=50)
        tk.Label(self.content_frame, text="Выберите нужный раздел в боковом меню.",
                 font=("Arial", 12), fg="#666").pack()

        self.current_window.mainloop()

    def show_all_requests(self):
        """Страница всех заявок (для менеджера/администратора)"""
        self.clear_content()

        tk.Label(self.content_frame, text="Все заявки", font=("Arial", 18, "bold")).pack(anchor="w", pady=10)

        # Таблица заявок
        columns = ('ID', 'Тип техники', 'Модель', 'Проблема', 'Статус', 'Клиент', 'Мастер', 'Дата завершения')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.column('Проблема', width=200)
        tree.column('ID', width=50)

        # Загрузка данных
        requests = self.db.get_all_requests()
        for req in requests:
            tree.insert('', 'end', values=(
                req['request_id'],
                req['hometechtype'],
                req['hometechmodel'],
                req['problemdescription'][:50] + ('...' if len(req['problemdescription']) > 50 else ''),
                req['statusofrequest'],
                req['client_name'] or '-',
                req['master_name'] or 'Не назначен',
                req['dateofcompletion'] or '-'
            ))

        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки управления
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Просмотреть", command=lambda: self.show_request_info(self.get_selected_id(tree)),
                  bg="#2196F3", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Редактировать", command=lambda: self.show_edit_request(self.get_selected_id(tree)),
                  bg="#FF9800", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить", command=lambda: self.delete_request(self.get_selected_id(tree)),
                  bg="#f44336", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.show_all_requests,
                  bg="#9E9E9E", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)

    def show_master_requests(self):
        """Страница заявок мастера"""
        self.clear_content()

        tk.Label(self.content_frame, text="Мои заявки (мастер)", font=("Arial", 18, "bold")).pack(anchor="w", pady=10)

        user = self.auth_manager.get_current_user()
        requests = self.db.get_requests_by_master(user['user_id'])

        columns = ('ID', 'Тип техники', 'Модель', 'Проблема', 'Статус', 'Клиент', 'Дата завершения')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.column('Проблема', width=200)
        tree.column('ID', width=50)

        for req in requests:
            tree.insert('', 'end', values=(
                req['request_id'],
                req['hometechtype'],
                req['hometechmodel'],
                req['problemdescription'][:50] + ('...' if len(req['problemdescription']) > 50 else ''),
                req['statusofrequest'],
                req['client_name'],
                req['dateofcompletion'] or '-'
            ))

        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Просмотреть", command=lambda: self.show_request_info(self.get_selected_id(tree)),
                  bg="#2196F3", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.show_master_requests,
                  bg="#9E9E9E", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)

    def show_client_requests(self):
        """Страница заявок клиента"""
        self.clear_content()

        tk.Label(self.content_frame, text="Мои заявки", font=("Arial", 18, "bold")).pack(anchor="w", pady=10)

        user = self.auth_manager.get_current_user()
        requests = self.db.get_requests_by_client(user['user_id'])

        columns = ('ID', 'Тип техники', 'Модель', 'Проблема', 'Статус', 'Мастер', 'Дата завершения')
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings', height=20)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.column('Проблема', width=200)
        tree.column('ID', width=50)

        for req in requests:
            tree.insert('', 'end', values=(
                req['request_id'],
                req['hometechtype'],
                req['hometechmodel'],
                req['problemdescription'][:50] + ('...' if len(req['problemdescription']) > 50 else ''),
                req['statusofrequest'],
                req['master_name'] or 'Не назначен',
                req['dateofcompletion'] or '-'
            ))

        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Просмотреть", command=lambda: self.show_request_info(self.get_selected_id(tree)),
                  bg="#2196F3", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", command=self.show_client_requests,
                  bg="#9E9E9E", fg="white", font=("Arial", 10), width=12).pack(side="left", padx=5)

    def show_request_info(self, request_id):
        """Страница с информацией о заявке"""
        if not request_id:
            messagebox.showwarning("Предупреждение", "Выберите заявку")
            return

        request = self.db.get_request_by_id(request_id)
        if not request:
            messagebox.showerror("Ошибка", "Заявка не найдена")
            return

        comments = self.db.get_comments_by_request(request_id)

        self.clear_content()

        # Заголовок
        top_frame = tk.Frame(self.content_frame)
        top_frame.pack(fill="x", pady=10)
        tk.Label(top_frame, text=f"Заявка №{request['request_id']}", font=("Arial", 18, "bold")).pack(side="left")
        tk.Button(top_frame, text="Назад", command=self.show_all_requests,
                  bg="#9E9E9E", fg="white", font=("Arial", 10)).pack(side="right")

        # Основная информация
        info_frame = tk.LabelFrame(self.content_frame, text="Информация о заявке", font=("Arial", 12, "bold"))
        info_frame.pack(fill="x", pady=10, padx=10)

        info_text = f"""
Тип техники: {request['hometechtype']}
Модель: {request['hometechmodel']}
Описание проблемы: {request['problemdescription']}
Статус: {request['statusofrequest']}
Клиент: {request['client_name']}
Мастер: {request['master_name'] or 'Не назначен'}
Запчасти: {request['repairparts'] or 'Не указаны'}
Дата завершения: {request['dateofcompletion'] or 'Не завершена'}
        """
        tk.Label(info_frame, text=info_text, font=("Arial", 11), justify="left").pack(anchor="w", padx=10, pady=10)

        # Комментарии
        comments_frame = tk.LabelFrame(self.content_frame, text="Комментарии", font=("Arial", 12, "bold"))
        comments_frame.pack(fill="both", expand=True, pady=10, padx=10)

        comments_text = scrolledtext.ScrolledText(comments_frame, height=8, font=("Arial", 10))
        comments_text.pack(fill="both", expand=True, padx=10, pady=10)

        for comment in comments:
            comments_text.insert(tk.END, f"[{comment['user_name']} ({comment['type']})]: {comment['message']}\n")
        comments_text.config(state="disabled")

        # Добавление комментария
        add_frame = tk.Frame(comments_frame)
        add_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(add_frame, text="Новый комментарий:", font=("Arial", 10)).pack(anchor="w")
        self.new_comment_text = tk.Text(add_frame, height=3, font=("Arial", 10))
        self.new_comment_text.pack(fill="x", pady=5)

        def add_comment():
            message = self.new_comment_text.get("1.0", tk.END).strip()
            if message:
                user = self.auth_manager.get_current_user()
                if self.db.add_comment(request_id, user['user_id'], message):
                    messagebox.showinfo("Успех", "Комментарий добавлен")
                    self.show_request_info(request_id)
                else:
                    messagebox.showerror("Ошибка", "Не удалось добавить комментарий")

        tk.Button(add_frame, text="Добавить комментарий", command=add_comment,
                  bg="#4CAF50", fg="white", font=("Arial", 10)).pack()

    def show_edit_request(self, request_id):
        """Страница редактирования заявки (для менеджера)"""
        if not request_id:
            messagebox.showwarning("Предупреждение", "Выберите заявку")
            return

        request = self.db.get_request_by_id(request_id)
        if not request:
            messagebox.showerror("Ошибка", "Заявка не найдена")
            return

        self.clear_content()

        tk.Label(self.content_frame, text=f"Редактирование заявки №{request_id}",
                 font=("Arial", 18, "bold")).pack(anchor="w", pady=10)

        frame = tk.Frame(self.content_frame)
        frame.pack(pady=20)

        # Статус
        tk.Label(frame, text="Статус:", font=("Arial", 11)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
        status_var = tk.StringVar(value=request['statusofrequest'])
        statuses = self.db.get_all_statuses()
        status_menu = ttk.Combobox(frame, textvariable=status_var, values=statuses, state="readonly", width=30)
        status_menu.grid(row=0, column=1, pady=10)

        # Мастер
        tk.Label(frame, text="Назначить мастера:", font=("Arial", 11)).grid(row=1, column=0, pady=10, padx=10,
                                                                            sticky="e")
        masters = self.db.get_all_masters()
        master_values = {f"{m['fio']} (ID:{m['user_id']})": m['user_id'] for m in masters}
        master_var = tk.StringVar(value=list(master_values.keys())[0] if masters else "")
        master_menu = ttk.Combobox(frame, textvariable=master_var, values=list(master_values.keys()), state="readonly",
                                   width=30)
        master_menu.grid(row=1, column=1, pady=10)

        # Запчасти
        tk.Label(frame, text="Использованные запчасти:", font=("Arial", 11)).grid(row=2, column=0, pady=10, padx=10,
                                                                                  sticky="e")
        parts_entry = tk.Entry(frame, width=33, font=("Arial", 11))
        parts_entry.insert(0, request['repairparts'] or "")
        parts_entry.grid(row=2, column=1, pady=10)

        # Дата завершения
        tk.Label(frame, text="Дата завершения (ГГГГ-ММ-ДД):", font=("Arial", 11)).grid(row=3, column=0, pady=10,
                                                                                       padx=10, sticky="e")
        date_entry = tk.Entry(frame, width=33, font=("Arial", 11))
        date_entry.insert(0, request['dateofcompletion'] or "")
        date_entry.grid(row=3, column=1, pady=10)

        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=20)

        def save_changes():
            master_id = master_values.get(master_var.get(), None)
            success = self.db.update_request(
                request_id,
                statusofrequest=status_var.get(),
                master_id=master_id,
                repairparts=parts_entry.get() or None,
                dateofcompletion=date_entry.get() or None
            )
            if success:
                messagebox.showinfo("Успех", "Заявка обновлена")
                self.show_all_requests()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить заявку")

        tk.Button(btn_frame, text="Сохранить", command=save_changes,
                  bg="#4CAF50", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Отмена", command=self.show_all_requests,
                  bg="#f44336", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)

    def show_add_request(self):
        """Страница добавления новой заявки"""
        self.clear_content()

        tk.Label(self.content_frame, text="Новая заявка", font=("Arial", 18, "bold")).pack(anchor="w", pady=10)

        frame = tk.Frame(self.content_frame)
        frame.pack(pady=20)

        tk.Label(frame, text="Тип техники:", font=("Arial", 11)).grid(row=0, column=0, pady=10, padx=10, sticky="e")
        tech_type_entry = tk.Entry(frame, width=40, font=("Arial", 11))
        tech_type_entry.grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Модель:", font=("Arial", 11)).grid(row=1, column=0, pady=10, padx=10, sticky="e")
        model_entry = tk.Entry(frame, width=40, font=("Arial", 11))
        model_entry.grid(row=1, column=1, pady=10)

        tk.Label(frame, text="Описание проблемы:", font=("Arial", 11)).grid(row=2, column=0, pady=10, padx=10,
                                                                            sticky="e")
        problem_text = tk.Text(frame, height=5, width=35, font=("Arial", 11))
        problem_text.grid(row=2, column=1, pady=10)

        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(pady=20)

        def add_request():
            tech_type = tech_type_entry.get().strip()
            model = model_entry.get().strip()
            problem = problem_text.get("1.0", tk.END).strip()

            if not all([tech_type, model, problem]):
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            user = self.auth_manager.get_current_user()
            if self.db.add_request(tech_type, model, problem, user['user_id']):
                messagebox.showinfo("Успех", "Заявка создана!")
                if user['type'] == 'Заказчик':
                    self.show_client_requests()
                else:
                    self.show_all_requests()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать заявку")

        tk.Button(btn_frame, text="Создать заявку", command=add_request,
                  bg="#4CAF50", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Отмена", command=self.show_main_window,
                  bg="#9E9E9E", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)

    def delete_request(self, request_id):
        """Удаление заявки"""
        if not request_id:
            messagebox.showwarning("Предупреждение", "Выберите заявку")
            return

        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить заявку №{request_id}?"):
            if self.db.delete_request(request_id):
                messagebox.showinfo("Успех", "Заявка удалена")
                self.show_all_requests()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить заявку")

    def get_selected_id(self, tree):
        """Получение ID выбранной записи"""
        selection = tree.selection()
        if selection:
            values = tree.item(selection[0])['values']
            return values[0] if values else None
        return None

    def clear_content(self):
        """Очистка области контента"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_about(self):
        """О программе"""
        messagebox.showinfo("О программе",
                            "Сервисный центр 'ТехноМастер'\n"
                            "Версия 1.0\n"
                            "Система управления заявками на ремонт бытовой техники")

    def logout(self):
        """Выход из системы"""
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.auth_manager.logout()
            self.show_login_window()