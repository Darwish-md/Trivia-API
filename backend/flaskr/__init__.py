# pylint: disable=no-member  
# pylint: disable=import-error
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE 
  end = start + QUESTIONS_PER_PAGE 
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories", methods = ["GET"])
  def retrieve_categories():
    records = Category.query.order_by(Category.id).all()
    categories_list = [record.format() for record in records]
    
    categories = {}
    for category in categories_list:
      categories['{}'.format(category['id'])] = '{}'.format(category['type'])
    
    return jsonify({
      'success' : True,
      'categories' : categories,
      'number_of_categories' : len(records)
    })
  

  @app.route("/questions", methods = ["GET"])
  def retrieve_questions():
    selection = Question.query.order_by('id').all()
    current_questions = paginate(request, selection)
    records = Category.query.order_by(Category.id).all()
    categories_list = [record.format() for record in records]
    
    categories = {}
    for category in categories_list:
      categories['{}'.format(category['id'])] = '{}'.format(category['type'])

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': categories,
      'current_category': None
    })
      

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

  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()

    if question is None:
        abort(404)

    try:
      question.delete()
      selection = Question.query.order_by('id').all()

      return jsonify({
        'success': True,
        'deleted_question': question_id,
        'total_questions': len(selection)
      })
    except: 
      abort(422)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions', methods = ['POST'])
  def create_questions():
    body = request.get_json()
    
    try:
      question = body.get('question')
      answer = body.get('answer')
      difficulty = body.get('difficulty')
      category_id = body.get('category')

      new_question = Question(question = question, answer = answer,
                              difficulty = difficulty, category_id = category_id)
      new_question.insert()
      selection = Question.query.order_by('id').all()

      return jsonify({
        'success': True,
        'posted': new_question.format(),
        'total_questions': len(selection)
      })
  
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/search_questions', methods = ['POST'])
  def search_questions():
    body = request.get_json()
    
    try:
      search_term = body.get('search_term')
      search = '%{}%'.format(search_term)
      selection = Question.query.filter(Question.question.ilike(search)).order_by('id').all()
      current_questions = paginate(request, selection)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'current_category': None
      })
    
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/categories/<int:category_id>/questions", methods = ['GET'])
  def retrieve_questions_by_category_id(category_id):
    selection = Question.query.filter(Question.category_id == category_id).order_by('id').all()
    current_questions = paginate(request, selection)
    
    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'current_category': category_id
    })

  
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def quiz():
    body = request.get_json()
    
    try:
      previous_questions = body.get('previous_questions')
      quiz_category = body.get('quiz_category', None)

      if quiz_category:
        questions = Question.query.filter(Question.category_id == quiz_category).all()
      else:
        questions = Question.query.all()

      if len(questions) == 0:
        abort(404)
      
      questions_list = [question.format() for question in questions]

      for previous_question in previous_questions:
        for question in questions_list:
          if previous_question['id'] == question['id']:
            questions_list.remove(question)
      
      random_question = random.choice(questions_list)
        
      return jsonify({
          'success': True,
          'question': random_question,
          'play_category': quiz_category
      })
    except:
      abort(422)


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
  @app.errorhandler(400)
  def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad request :("
        }), 400


  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Sorry, couldn't find a resource matching your request :("
        }), 404


  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Sorry, couldn't process your request :("
        }), 422

    
  @app.errorhandler(500)
  def not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Method not allowed"
        }), 500

    """
    @app.errorhandler(404)
    def not_found(error=None):
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404

        return resp"""
    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    
