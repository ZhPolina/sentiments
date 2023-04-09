# -*- coding: utf-8 -*-
import sys
sys.path.append('./')
from flask import session
from main import sentiment, predict_emotion
import unittest

# Проверка функции подсчета процентной доли содержания каждой эмоции среди всех комментариев по выбранному месту досуга
class TestComments(unittest.TestCase):

    def test_sentiment_empty_reviews(self):
        result = sentiment([])
        self.assertEqual(result, (0, 0, 0))

    def test_sentiment_all_positive_reviews(self):
        reviews = [('review1', 'user1', 'date1', 'positive'), ('review2', 'user2', 'date2', 'positive')]
        result = sentiment(reviews)
        self.assertEqual(result, (0, 100, 0))

    def test_sentiment_all_negative_reviews(self):
        reviews = [('review1', 'user1', 'date1', 'negative'), ('review2', 'user2', 'date2', 'negative')]
        result = sentiment(reviews)
        self.assertEqual(result, (100, 0, 0))

    def test_sentiment_mixed_reviews(self):
        reviews = [('review1', 'user1', 'date1', 'positive'), ('review2', 'user2', 'date2', 'negative'), ('review3', 'user3', 'date3', 'neutral')]
        result = sentiment(reviews)
        self.assertEqual(result, (33, 33, 33))

# Проверка функции определения тональности
class TestPredictEmotion(unittest.TestCase):

    def test_predict_emotion_empty_review(self):
        result = predict_emotion('')
        self.assertEqual(result, ('neutral', 1.0))

    def test_predict_emotion_positive_review(self):
        result = predict_emotion('Хорошо:)')
        self.assertEqual(result, ('positive', 1.0))

    def test_predict_emotion_negative_review(self):
        result = predict_emotion('Плохо:(')
        self.assertEqual(result, ('negative', 1.0))

if __name__ == '__main__':
    unittest.main()
