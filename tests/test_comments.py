import unittest
import path
from main import app, mysql

class TestAddComment(unittest.TestCase):

     # проверка добавления нового комментария 
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # внесение в базу данных информации о новом месте досуга с id = 4
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO places (id_places, name, link, image, description) VALUES (4, 'Test Place', 'Test Link', 'Test Image', 'Test Description')")
            mysql.connection.commit()
    
    # проверка работы функции добавления нового комментария в ранее созданное место досуга с id = 4
    # пользователь должен быть авторизован  
    def test_add_comment(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['loggedin'] = True
                session['id'] = '1'
                session['username'] = 'pzheleznikova'
            response = client.post('/comments/4', data=dict(comment='Новый комментарий'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/comments/4')
            with app.app_context():
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM reviews WHERE id_places = %s', ('4',))
                result = cursor.fetchall()
                self.assertEqual(len(result), 1)
                self.assertEqual(result[-1][2], 'Новый комментарий')
                self.assertEqual(result[-1][5], 'neutral')
    
    # удаление тестовых данных      
    def tearDown(self):
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE id_places = 4")
            cursor.execute("DELETE FROM places  WHERE id_places = 4")
            cursor.execute("DELETE FROM reviews WHERE id_places = 3 and id_user = 1")
            mysql.connection.commit()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()
