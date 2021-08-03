from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, emit, join_room
import os
import requests
import random
import html
import time

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")
socketio.init_app(app)

rooms = {}

@app.route("/")
def home():
    print('ON HOME PAGE')
    global next_que
    global question_list
    global correct_answers
    global final_answers
    global amount
    global score
    global database_list
    global played_solo
    global nickname
    played_solo = False
    next_que = 0
    amount = 0
    score = 0
    question_list = []
    final_answers = []
    correct_answers = []
    database_list = []
    return render_template("index.html")

@app.route("/solo/game", methods=["POST"])
def user_input():
    global amount
    global nickname
    played_solo = True
    categories_list = ['food_and_drink', 'art_and_literature', 'movies', 'music', 'society_and_culture', 'sport_and_leisure', 'geography']
    amount = request.form.get("amount")
    category = request.form.get("category")
    difficulty = request.form.get("difficulty")
    nickname = request.form.get("nickname")
    print(nickname)


    # if the category is food and drink, art and literature, movies, music, science, society and culture or sport and leisure use second api
    if (category in categories_list):
        url = getNewUrl(amount,category)
        Json = getNewJson(url)
        correct_answers, final_answers, question_list = newToDict(Json)

    else:
        url = getUrl(amount, category,difficulty)
        Json = getJson(url)
        correct_answers, final_answers, question_list = toDict(Json)
    

    return quiz(correct_answers, final_answers, question_list)

@app.route('/next/question', methods=["POST"])
def next_question():
    global next_que
    global question_list
    global correct_answers
    global final_answers
    #global amount
    global score

    answer = request.form.get("answers")

    if(final_answers[next_que][int(answer)] == correct_answers[next_que]):
        print(final_answers[next_que][int(answer)])
        print(correct_answers[next_que])
        score += 1
    
    print('NEXT QUE: ', next_que)
    print('AMOUNT ', amount)
    if int(next_que + 1) == int(amount):
        print('NEXT QUE: in if ', next_que)
        print('\n\n\nLAST QUESTION\n\n\n\n')
        link = "/display_score/" + str(score) + str(amount)
        return redirect(link)
        # print(score)
        
    next_que += 1
    print('SHOULD START AT 1', next_que)
    print('final answers: ')
    print(final_answers)
    question_name = question_list[next_que]

    return render_template(
        'quiz.html',
        question=str(
        next_que + 1) + ") " + html.unescape(question_name),
        answer1=html.unescape(
        final_answers[next_que][0]),
        answer2=html.unescape(
        final_answers[next_que][1]),
        answer3=html.unescape(
        final_answers[next_que][2]),
        answer4=html.unescape(
        final_answers[next_que][3]))
    
@app.route("/display_score/<score><amount>")
def display_score(score, amount):
    global nickname
    #time = stop stopwatch
    #addToDB(nickname,score,time)
    try:
        return render_template(
            "score.html",
            Nickname=nickname,
            score=score,
            amount=amount)
    except BaseException:
        return render_template(
            "score.html",
            Nickname="User",
            score=score,
            amount=amount)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/leaderboard")
def leaderboard():

    return render_template('leaderboard.html')

@app.route("/quiz<room>", methods=["POST"])
def quiz(room):
    global amount_2
    global nickname_2

    categories_list = ['food_and_drink', 'art_and_literature', 'movies', 'music', 'society_and_culture', 'sport_and_leisure', 'geography']
    amount_2 = request.form.get("amount")
    category = request.form.get("category")
    difficulty = request.form.get("difficulty")
    nickname_2 = request.form.get("nickname")
    print(nickname_2)


    # if the category is food and drink, art and literature, movies, music, science, society and culture or sport and leisure use second api
    if (category in categories_list):
        url = getNewUrl(amount_2,category)
        Json = getNewJson(url)
        correct_answers, final_answers, question_list = newToDict(Json)

    else:
        url = getUrl(amount_2, category,difficulty)
        Json = getJson(url)
        correct_answers, final_answers, question_list = toDict(Json)
    

    return quiz(correct_answers, final_answers, question_list)



def getNewUrl(amount,category):
    print('MADE IT TO GET NEW URL')
    base_url = 'https://trivia.willfry.co.uk/api/questions?'
    final_url = base_url + 'limit=' + str(amount)
    # print('before, ', final_url)
    if category != 'default_c':
        final_url = base_url + 'categories=' + category + '&limit=' + str(amount)
        # print(final_url)
    return final_url


def getNewJson(url):
    response = requests.get(url)
    data = response.json()
    return data


def newToDict(json):
    correct = []
    answers = []
    temp_list = []
    for value in json:
        #print(value['question'])
        question_list.append(value['question'])
        correct_answers.append(value['correctAnswer'])
        correct = value['correctAnswer']
        # Grabs only 3 incorrect answers to make sure corect answer will always be on screen
        answers = value['incorrectAnswers'][:3]
        answers.append(correct)
        random.shuffle(answers)
        final_answers.append(answers)
    return correct_answers, final_answers, question_list


def getUrl(amount, category, difficulty):
    Base_url = 'https://opentdb.com/api.php?amount=' + str(amount)
    final_url = Base_url
    # categoryA
    if category != 'default_c':
        final_url = final_url + '&category=' + str(category)

    # difficulty
    if difficulty != 'default_d':
        final_url = final_url + '&difficulty=' + str(difficulty)
    
    final_url = final_url + '&type=multiple'

    return final_url


def getJson(final_url):
    response = requests.get(final_url)
    data = response.json()
    return data


def toDict(json_data):
    correct = []
    answers = []
    for value in json_data['results']:
        # print(value)
        # questions.append(value['question'])
        question_list.append(value['question'])
        correct_answers.append(value['correct_answer'])
        correct = value['correct_answer']
        answers = value['incorrect_answers']
        answers.append(correct)
        random.shuffle(answers)
        final_answers.append(answers)
    print('q list ', question_list)
    # print('f answers ', final_answers)
    # print('c list' , correct_list)

    return correct_answers, final_answers, question_list


def quiz(correct_answers, final_answers, question_list):
    print("camehere")
    #start stopwatch
    global start_time
    start_time = time.time()
    question_name = question_list[0]

    return render_template(
        'quiz.html',
        question='1) ' +
        html.unescape(question_name),
        answer1=html.unescape(
            final_answers[0][0]),
        answer2=html.unescape(
            final_answers[0][1]),
        answer3=html.unescape(
            final_answers[0][2]),
        answer4=html.unescape(
            final_answers[0][3]))


next_que = 0
score = 0



def is_admin(id, room):
    return rooms[room] == id

@socketio.on('connection')
def on_connect(socket):
    print('user connected')

@socketio.on('disconnect')
def on_admin_disconnect():
    print('user disconnected')
    print(rooms)
    for room in rooms:
        if is_admin(request.sid, room):
            print(room)
            del rooms[room]
    emit('leave')

# only emitted by players

@socketio.on('join')
def on_join(data):
    name = data['name']
    room = data['room']
    join_room(room)
    emit('join', data, room=room)
    print(f'{name} joined {room}')

@socketio.on('buzz')
def on_buzz(data):
    name = data['name']
    room = data['room']
    emit('buzz', { 'name': name } , room=room)

@socketio.on('exists')
def exists(data):
    room = data['room']
    emit('exists', room in rooms)

# only emitted by admin

@socketio.on('create')
def on_create(data):
    room = data['room']
    if (room in rooms or len(room) < 3):
        emit('create', False)
    else:
        join_room(room)
        rooms[room] = request.sid
        emit('create', True)
        print(f'created room: {room}')

@socketio.on('reset')
def on_reset(data):
    room = data['room']
    #res = data['res']
    if is_admin(request.sid, room):
        emit('reset', room=room)

#@socketio.on('begin')
#def on_begin(data):
    #room = data['room']
    #if is_admin(request.sid, room):
        #emit('begin', room=room)

@socketio.on('score')
def on_score(data):
    leaderboard = data['leaderboard']
    room = data['room']
    if is_admin(request.sid, room):
        emit('score', { 'leaderboard' : leaderboard }, room=room)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    #socketio.run(app, debug=True)