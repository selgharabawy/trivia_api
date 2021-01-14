import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

#starter.backend.
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''


 
  @app.route('/categories', methods = ['GET','POST'])
  @cross_origin()
  def handle_categories():
    if request.method == 'POST':
      data = request.json
      error = False
      cat_body ={}
      try:
        category_new = Category(type = data['category'])
        db.session.add(category_new)
        db.session.commit()
        cat_body = {
          'success': True, 
          'category': category_new.format()
        }
      except:
        error = True
        db.session.rollback()
      finally:
        db.session.close()
      if error:
          abort(400) #Bad Request
      else:
          return jsonify(cat_body),201 #Created
    elif request.method == 'GET':
      categories_qr= db.session.query(Category).all()
      categories_dict = {category.id: category.type for category in categories_qr}
      if len(categories_qr)==0:
          abort (404) #Not Found
      else:
        cat ={
            'success' : True,
            'categories' : categories_dict
            }
        return jsonify(cat),200 #Ok
  

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  
  def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]
    return current_questions
  


  @app.route('/questions', methods = ['GET','POST'])
  @cross_origin()
  def handle_questions():
    categories= db.session.query(Category).all()
    categories_dict = {category.id: category.type for category in categories}
    categories_cur = [category.id for category in categories]
    if request.method == 'POST':
      data = request.json    
      if (data['searchTerm'] is None):  #Add a Question
        error = False
        body ={}
        try:
          question_new = Question(question = data['question'], answer =data['answer'], 
          category = data['category'], difficulty = data['difficulty'])
          db.session.add(question_new)
          db.session.commit()
          body = {
            'success': 'true', 
            'question': question_new.format()
          }
        except:
          error = True
          db.session.rollback()
          body = {'success': 'false'}
        finally:
          db.session.close()
        if error:
            abort(400) #Bad Request
        else:
            return jsonify(body),201 #created
      else:  #Search for a Question
        questions = db.session.query(Question).filter(Question.question.ilike('%'+data['searchTerm']+'%')).all()
        if len(questions)==0:
              abort(404) #Not Found
        else:
          quest ={
            'total_questions' : db.session.query(Question).count(),
            'questions' : paginate_questions(request,questions),
            'categories' : categories_dict,
            "current_category": categories_cur
          } 
          return jsonify(quest),200 #Ok
    elif request.method == 'GET':  
      questions = db.session.query(Question).all()
      if len(questions)==0:
              abort(404) #Not Found
      else:
        if (request.args.get('page', 1, type=int) != 1 and db.session.query(Question).count()/QUESTIONS_PER_PAGE < request.args.get('page', 1, type=int)):
          abort(404)
        else:
          quest ={
          'total_questions' : db.session.query(Question).count(),
          'questions' : paginate_questions(request,questions),
          'categories' : categories_dict,
          "current_category": categories_cur
          } 
          return jsonify(quest),200 #Ok
    

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def retrieve_entree(question_id):
    if (db.session.query(Question).get(question_id) is None):
      print('error')
      abort(422) #Unprocessable
    else:
      db.session.query(Question).get(question_id).delete()
      return jsonify({
        "success": True,
        "message": "Question deleted"}),200 #Ok


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions', methods = ['GET'])
  @cross_origin()
  def question_by_cat(cat_id):
    questions = db.session.query(Question).filter(Question.category == cat_id).all()
    categories_qr= db.session.query(Category).all()
    category_cur_qr= db.session.query(Category).get(cat_id)
    categories_dict = {category.id: category.type for category in categories_qr}
    categories_cur = [cat_id]
    if ( request.args.get('page', 1, type=int) != 1 and db.session.query(Question).filter(Question.category == cat_id).count()/QUESTIONS_PER_PAGE < request.args.get('page', 1, type=int)):
          abort(404)
    else:
      quest ={
          'total_questions' : db.session.query(Question).filter(Question.category == cat_id).count(),
          'questions' : paginate_questions(request,questions),
          'categories' : categories_dict,
          "current_category": categories_cur
          }
      if len(questions)==0:
        abort(404) #Not Found
      else:
        return jsonify(quest),200

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  @cross_origin()
  def handle_quizzes():
    data = request.json
    if data['quiz_category']['id'] == 0:
      questions = db.session.query(Question).filter().all()
      questions_per_cat = db.session.query(Question).filter().count()
    else:
      questions = db.session.query(Question).filter(Question.category == data['quiz_category']['id']).all()
      questions_per_cat = db.session.query(Question).filter(Question.category == data['quiz_category']['id']).count()
    
    if len(questions)==0:
        abort(404)
    elif len(data['previous_questions'] ) == 0:
      current_quest = questions[random.randint(0, len(questions)-1)].format()
      quest ={
          'success' : True,
          'questions_per_cat': questions_per_cat,
          'question' : current_quest
          } 
      return jsonify(quest),200
    elif len(data['previous_questions'] ) == questions_per_cat:
      quest ={
        'success' : False,
        'questions_per_cat': questions_per_cat,
        'message':'Questions are over'
        }
      return jsonify(quest)
    else:
      while True:
        i = random.randint(0, len(questions)-1)
        is_in_prev = False
        for j in range(0,len(data['previous_questions'])):
            if (questions[i].id == data['previous_questions'][j]):
                is_in_prev = True
        if (is_in_prev == False):
              current_quest = questions[i].format()
              quest ={
                  'success' : True,
                  'questions_per_cat': questions_per_cat,
                  'question' : current_quest
                  } 
              return jsonify(quest),200 
    
  
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400

  return app

    