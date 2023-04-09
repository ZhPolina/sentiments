import sys
sys.path.append('./')
from main import app, mysql
import unittest

class TestUpdateRatingTrigger(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        self.app_context = app.app_context()
        self.app_context.push()
        
    def test_update_rating(self):
        with mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO reviews (id_places, emotion, rating) VALUES (3, 'positive', 0.4), (3, 'negative', 0.2), (3, 'neutral', 0.5), (3, 'neutral', 0.1)")
            mysql.connection.commit()
        
            # Проверка, что поля rating и avg_emotion в соответствующих записях place обновлены правильно
            cursor.execute("SELECT rating, avg_emotion FROM places WHERE id_places = 3")
            row = cursor.fetchone()
            # ожидаемый рейтинг - максимальный средний рейтинг среди всех тональностей комментариев для id_places=3, он равен 0.4 (позитивная эмоция имеет наибольший средний рейтинг)          
            self.assertEqual(row[0], 0.4)  
            # ожидаемая эмоция - "positive"
            self.assertEqual(row[1], 'positive') 

    # удаление тестовых данных        
    @classmethod
    def tearDownClass(self):
        with mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE id_places IN (3)")
            cursor.execute("UPDATE places SET rating=NULL, avg_emotion=NULL WHERE id_places IN (3)")
            mysql.connection.commit()
                 
if __name__ == '__main__':
    unittest.main()
