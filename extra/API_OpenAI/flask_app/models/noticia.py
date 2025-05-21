## Coding Dojo - Python Bootcamp Jan 2025
## Roberto Alvarez, 2025

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Noticia:

    def __init__(self, data):
        self.id = data['id']
        self.news = data['news']
        self.type = data['type']
        self.explanation = data['explanation']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM news;"
        results = connectToMySQL().query_db(query)
        all_news = []
        for news in results:
            all_news.append(cls(news))
        return all_news


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM news WHERE id = %(id)s;"
        data = {"id": id}
        result = connectToMySQL().query_db(query, data)
        return cls(result[0])


    @classmethod
    def get_by_user(cls, user_id):
        query = "SELECT * FROM news WHERE user_id = %(user_id)s;"
        data = {
            'usuario_id': usuario_id
        }
        results = connectToMySQL().query_db(query, data)
        news_list = []
        for news in results:
            news_list.append(cls(news))
        return news_list


    @classmethod
    def save(cls, data):
        query = "INSERT INTO news (news, type, explanation, usuario_id, created_at, updated_at) VALUES (%(news)s, %(type)s, %(explanation)s, %(usuario_id)s, NOW(), NOW())"
        flash ("Noticia salva", "success")
        return connectToMySQL().query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM news WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL().query_db(query, data)


    @classmethod
    def update(cls, news_data):
        query = "UPDATE news SET news = %(news)s, type = %(type)s, explanation = %(explanation)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            "id": news_data.id,
            "news": news_data.news,
            "type": news_data.type,
            "explanation": news_data.explanation,
        }
        return connectToMySQL().query_db(query, data)


