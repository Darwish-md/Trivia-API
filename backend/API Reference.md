Getting started:

Base URL:  This app can be run locally and there is no base URL currently. To       access the backend, it is hosted on https://127.0.0.1:5000 which is set as a proxy in the frontend configuration. To interact with the API through the frontend, it is hosted on https://127.0.0.1:3000

Authentication: there is no authentication or API keys for the app.

Error Handling:

There are four error types returned by the API if requests fail. Errors are returned as JSON objects in the following format:

•	400: Bad request
{
            "success": False,
            "error": 400,
            "message": "Bad request :("
        }

•	404: Resource not found
      {
            "success": False,
            "error": 404,
            "message": "Sorry, couldn't find a resource matching your request :("
        }
•	422: not processable
{
            "success": False,
            "error": 422,
            "message": "Sorry, couldn't process your request :("
        }
•	500: Method not allowed
{
            "success": False,
            "error": 500,
            "message": "Method not allowed"
        }



End Points:

I-	GET /categories
•	General: returns a dictionary of the categories, the number of the categories, and the success value.
•	Sample: curl http://127.0.0.1:5000/categories
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "number_of_categories": 6,
  "success": true
}

II-	GET /questions
•	General: 
      • returns a dictionary of the categories, the current category as null, a list of the questions, the total number of questions, and the success value.
      • questions are paginated in a group of 10. include a request argument to  choose page number starting from 1
•	Sample: curl http://127.0.0.1:5000/questions?page=1
{ 
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
 },
  "current_category": null,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category_id": 4,
      "difficulty": 1,
      "id": 8,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category_id": 5,
      "difficulty": 4,
      "id": 9,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 10,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category_id": 5,
      "difficulty": 3,
      "id": 11,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category_id": 6,
      "difficulty": 3,
      "id": 12,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category_id": 6,
      "difficulty": 4,
      "id": 13,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category_id": 4,
      "difficulty": 2,
      "id": 14,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category_id": 3,
      "difficulty": 2,
      "id": 15,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category_id": 3,
      "difficulty": 3,
      "id": 16,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category_id": 3,
      "difficulty": 2,
      "id": 17,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 21
}

III- DELETE /questions/<int:question_id>
•	General: Deletes the question associated with id equals to the number passed in the URL which is question_id, then returns the id of the deleted question, the total number of questions, and the success value.
•	Sample: curl -X DELETE http://127.0.0.1:5000/questions/22
{
  "deleted_question": 22,
  "success": true,
  "total_questions": 20
}

IV-	POST /questions
•	General: creates a new question, then returns the question posted, the total number of questions, and the success value.
•	Sample: curl -X POST -H "Content-Type: application/json" -d '{"question": "How old is the Earth", "answer": "4.543 billion years","difficulty": 4,"category": 1}' http://127.0.0.1:5000/questions

{
  "posted": {
    "answer": "4.543 billion years",
    "category_id": 1,
    "difficulty": 4,
    "id": 31,
    "question": "How old is the Earth"
  },
  "success": true,
  "total_questions": 21
}

V-	POST /search_questions
•	General: returns a list of all questions that match the search term entered, the current category as null, the total number of questions matching the search term, and the success value.
•	Sample: curl -X POST -H "Content-Type: application/json" -d '{"search_term": "How"}' http://127.0.0.1:5000/search_questions

{
  "current_category": null,
  "questions": [
    {
      "answer": "One",
      "category_id": 2,
      "difficulty": 4,
      "id": 20,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "4.543 billion years",
      "category_id": 1,
      "difficulty": 4,
      "id": 28,
      "question": "How old is the Earth"
    }
  ],
  "success": true,
  "total_questions": 2
}

VI-	GET /categories/<int:category_id>/questions
•	General: returns the current category id, questions that match the category_id entered, the total number of questions matching that belong to that specific category, and the success value.
•	Sample: curl http://127.0.0.1:5000/categories/5/questions

{
  "current_category": 5,
  "questions": [
    {
      "answer": "Apollo 13",
      "category_id": 5,
      "difficulty": 4,
      "id": 9,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 10,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category_id": 5,
      "difficulty": 3,
      "id": 11,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 3
}

VIII- POST /quizzes
•	General: returns the play category id if chosen by the user, the random question which is chosen randomly and not one of the previous questions, and the success value.
•	Sample: curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":
[
    {"question": "How old is the Earth",
     "answer": "4.543 billion years",
     "difficulty": 4,
     "category": 1,
     "id":20},
 {
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination"}
],"quiz_category": 4}' http://127.0.0.1:5000/quizzes

{
  "play_category": 4,
  "question": {
    "answer": "Muhammad Ali",
    "category_id": 4,
    "difficulty": 1,
    "id": 8,
    "question": "What boxer's original name is Cassius Clay?"
  },
  "success": true
}


