import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

#starter.backend.
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres:pepsi@localhost:5432', 'trivia_test')
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()



        
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_cat(self):
        res= self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_get_quest(self):
        res= self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
    
    def test_get_quest_large_page(self):
        res= self.client().get('/questions?page=300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)

    def test_get_quest_cat_not_exist(self):
        res= self.client().get('/categories/11/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)

    def test_quiz_wrong_cat(self):
        res= self.client().post('/quizes', json={'quiz_category':10})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()