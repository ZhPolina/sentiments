import unittest
import path
from main import app, mysql

class TestDFunction(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        self.app.testing = True
        
    def test_d(self):
        # При вводе допустимых входных данных возвращаетcя успешный ответ и запрос к базе данных вовзращает не пустое значение
        response = self.app.post('/search_by_city', data=dict(city='Мурманск'))
        self.assertEqual(response.status_code, 200)

        # возвращается список мест досуга
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM places WHERE City = 'Мурманск'")
            result = cursor.fetchall()
            self.assertGreater(len(result), 0)

            # При вводе города, в котором отстуствуют данные о местах досуга база данных возвращает пустой список'
            cursor.execute("SELECT * FROM places WHERE City = 'Неправильно заданный город'")
            result = cursor.fetchall()
            self.assertEqual(len(result), 0)
            cursor.close()

        # При вводе города, в котором отстуствуют данные о местах досуга, выводится текст 'Нет результатов по Вашему запросу.'
        response = self.app.post('/search_by_city', data=dict(city='Неправильно заданный город'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Нет результатов по Вашему запросу.'.encode('utf-8'), response.data)
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()
