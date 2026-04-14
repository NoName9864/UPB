import psycopg2
from psycopg2 import sql
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Подключение к базе данных"""
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                port="5432",
                database="service_center",
                user="postgres",
                password="root"
            )
            self.cursor = self.conn.cursor()
            print("Успешное подключение к БД")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Выполнение запроса и возврат результатов"""
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                columns = [desc[0] for desc in self.cursor.description]
                results = []
                for row in self.cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                self.conn.commit()
                return []
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка запроса: {e}")
            raise e

    def get_user_by_login(self, login: str, password: str) -> Optional[Dict]:
        """Получение пользователя по логину и паролю"""
        query = """
            SELECT user_id, fio, login, type 
            FROM Users 
            WHERE login = %s AND password = %s
        """
        results = self.execute_query(query, (login, password))
        return results[0] if results else None

    def register_user(self, fio: str, phone: str, login: str, password: str, user_type: str) -> bool:
        """Регистрация нового пользователя"""
        try:
            query = """
                INSERT INTO Users (fio, phone, login, password, type)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.execute_query(query, (fio, phone, login, password, user_type))
            return True
        except:
            return False

    def get_all_requests(self) -> List[Dict]:
        """Получение всех заявок"""
        query = """
            SELECT r.request_id, r.hometechtype, r.hometechmodel, 
                   r.problemdescription, r.statusofrequest, 
                   r.dateofcompletion, r.repairparts,
                   u.fio as client_name, m.fio as master_name
            FROM Requests r
            LEFT JOIN Users u ON r.user_id = u.user_id
            LEFT JOIN Users m ON r.master_id = m.user_id
            ORDER BY r.request_id DESC
        """
        return self.execute_query(query)

    def get_requests_by_master(self, master_id: int) -> List[Dict]:
        """Получение заявок для мастера"""
        query = """
            SELECT r.request_id, r.hometechtype, r.hometechmodel, 
                   r.problemdescription, r.statusofrequest, 
                   r.dateofcompletion, r.repairparts,
                   u.fio as client_name
            FROM Requests r
            LEFT JOIN Users u ON r.user_id = u.user_id
            WHERE r.master_id = %s
            ORDER BY r.request_id DESC
        """
        return self.execute_query(query, (master_id,))

    def get_requests_by_client(self, client_id: int) -> List[Dict]:
        """Получение заявок клиента"""
        query = """
            SELECT r.request_id, r.hometechtype, r.hometechmodel, 
                   r.problemdescription, r.statusofrequest, 
                   r.dateofcompletion, r.repairparts,
                   m.fio as master_name
            FROM Requests r
            LEFT JOIN Users m ON r.master_id = m.user_id
            WHERE r.user_id = %s
            ORDER BY r.request_id DESC
        """
        return self.execute_query(query, (client_id,))

    def get_request_by_id(self, request_id: int) -> Optional[Dict]:
        """Получение заявки по ID"""
        query = """
            SELECT r.*, u.fio as client_name, m.fio as master_name
            FROM Requests r
            LEFT JOIN Users u ON r.user_id = u.user_id
            LEFT JOIN Users m ON r.master_id = m.user_id
            WHERE r.request_id = %s
        """
        results = self.execute_query(query, (request_id,))
        return results[0] if results else None

    def get_comments_by_request(self, request_id: int) -> List[Dict]:
        """Получение комментариев к заявке"""
        query = """
            SELECT c.comments_id, c.message, c.user_id, u.fio as user_name, u.type
            FROM Comments c
            JOIN Users u ON c.user_id = u.user_id
            WHERE c.request_id = %s
            ORDER BY c.comments_id
        """
        return self.execute_query(query, (request_id,))

    def add_comment(self, request_id: int, user_id: int, message: str) -> bool:
        """Добавление комментария"""
        try:
            query = """
                INSERT INTO Comments (request_id, user_id, message)
                VALUES (%s, %s, %s)
            """
            self.execute_query(query, (request_id, user_id, message))
            return True
        except:
            return False

    def add_request(self, hometechtype: str, hometechmodel: str,
                    problemdescription: str, user_id: int) -> bool:
        """Добавление новой заявки"""
        try:
            query = """
                INSERT INTO Requests (hometechtype, hometechmodel, 
                                      problemdescription, statusofrequest, user_id)
                VALUES (%s, %s, %s, 'Новая заявка', %s)
            """
            self.execute_query(query, (hometechtype, hometechmodel, problemdescription, user_id))
            return True
        except:
            return False

    def update_request(self, request_id: int, statusofrequest: str = None,
                       master_id: int = None, repairparts: str = None,
                       dateofcompletion: str = None) -> bool:
        """Обновление заявки"""
        try:
            updates = []
            params = []

            if statusofrequest:
                updates.append("statusofrequest = %s")
                params.append(statusofrequest)
            if master_id:
                updates.append("master_id = %s")
                params.append(master_id)
            if repairparts:
                updates.append("repairparts = %s")
                params.append(repairparts)
            if dateofcompletion:
                updates.append("dateofcompletion = %s")
                params.append(dateofcompletion)

            if updates:
                params.append(request_id)
                query = f"""
                    UPDATE Requests 
                    SET {', '.join(updates)}
                    WHERE request_id = %s
                """
                self.execute_query(query, tuple(params))
            return True
        except:
            return False

    def delete_request(self, request_id: int) -> bool:
        """Удаление заявки"""
        try:
            # Сначала удаляем комментарии
            self.execute_query("DELETE FROM Comments WHERE request_id = %s", (request_id,))
            # Затем удаляем заявку
            self.execute_query("DELETE FROM Requests WHERE request_id = %s", (request_id,))
            return True
        except:
            return False

    def get_all_masters(self) -> List[Dict]:
        """Получение всех мастеров"""
        query = "SELECT user_id, fio FROM Users WHERE type = 'Мастер'"
        return self.execute_query(query)

    def get_all_statuses(self) -> List[str]:
        """Получение всех возможных статусов"""
        return ['Новая заявка', 'В процессе ремонта', 'Готова к выдаче', 'Завершена']

    def close(self):
        """Закрытие соединения"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()