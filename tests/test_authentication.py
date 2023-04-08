# -*- coding: utf-8 -*-
import unittest
import path
from main import app, mysql

class TestLogin(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()

    # Проверка входа в систему пользователем, который зарегестрирован
    def test_successful_login(self):
        with self.app as client:
            with client.session_transaction() as sess:
                sess['loggedin'] = True
                sess['id'] = 0
                sess['username'] = 'pzheleznikova'
            result = self.app.get('/', follow_redirects=True)
            self.assertEqual(result.status_code, 200)
            self.assertIn('Выход'.encode('utf-8'), result.data)
            self.assertNotIn('Ошибка сервера'.encode('utf-8'), result.data)

    # Проверка обработки некорректных данных при попытке входа в систему
    def test_incorrect_login(self):
        result = self.app.post('/login', data=dict(username='wronguser', password='wrongpassword'), follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Неверный логин или пароль!".encode('utf-8'), result.data)
        self.assertIn('Вход'.encode('utf-8'), result.data)
        self.assertNotIn('Ошибка сервера'.encode('utf-8'), result.data)


    # Проверка обработки некорректного ввода данных при попытке регистрации в системе        
    def test_register_failure(self):
        result = self.app.post('/register', data=dict(
            username='test_user',
            password='test_user_password',
            email='not_an_email'
        ), follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('Неверный email!'.encode('utf-8'), result.data)
        self.assertNotIn('Вы успешно зарегистрировались!'.encode('utf-8'), result.data)
        self.assertNotIn('Ошибка сервера'.encode('utf-8'), result.data)
    
    # Проверка обработки случая, когда пользователь ввел корректные данные и успешно зарегистрировался        
    def test_register_success(self):
        result = self.app.post('/register', data=dict(
            username='test_user',
            password='test_user_password',
            email='test_user@example.com'
        ), follow_redirects=True)
        
        self.assertEqual(result.status_code, 200)
        self.assertIn('Вы успешно зарегистрировались!'.encode('utf-8'), result.data)
        self.assertNotIn('Неверный email!'.encode('utf-8'), result.data)
        self.assertNotIn('Ошибка сервера'.encode('utf-8'), result.data)

    # Удаление тестовых данных
    def tearDown(self):
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM accounts WHERE email = 'test_user@example.com'")
            mysql.connection.commit()
        
        self.app_context.pop()            


if __name__ == '__main__':
    unittest.main()