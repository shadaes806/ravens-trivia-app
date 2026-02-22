import sqlite3
from flask import *



def init_db():
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()
init_db()


app = Flask(__name__)
app.secret_key = "supersecretkey"



def save_score(player_name, score):
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO scores(player_name, score) VALUES (?,?)""", (player_name, score))
    conn.commit()
    conn.close()


def get_top_players(limit=5):
    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    top = c.fetchall()
    conn.close()
    return top


app = Flask(__name__)
app.secret_key = "supersecretkey"


 #MAKING A DICTIONARY FOR MY TRIVIA QUESTIONS


questions =[
    {
        "question": "In what year were the Baltimore Ravens established as an NFL franchise?",
        "options": {"A": "1992", "B": "1996 ", "C": "1990 ", "D": "1985"},
        "correct": "B"
    },

    {
        "question": "The Ravens got their team name from a poem by which famous author?",
        "options": {"A": "Walt Whitman", "B": "Robert Frost ", "C": "Edgar Allan Poe ", "D": "Emily Dickinson"},
        "correct": "C"
    },

    {
        "question": "Which Ravens legend was named MVP of Super Bowl XXXV?",
        "options": {"A": "Joe Flacco", "B": "Ray Lewis", "C":"Jamal Lewis", "D": "Justin Tucker " },
        "correct": "B"

    },

    {
        "question": "How many Super Bowl titles have the Ravens won?",
        "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
        "correct": "B"
    },
    {

        "question": "Who is the Ravens’ all‑time leading scorer?",
        "options": {"A": "Jamal Lewis", "B": "Joe Flacco", "C": "Justin Tucker", "D": "Derrick Mason"},
        "correct": "C"
    },

    {
        "question": "What are the official team colors of the Baltimore Ravens?",
        "options": {"A": "Purple, Black, Gold ", "B": "Blue, Silver, Black", "C": "Purple, White, Black", "D": "Green, Yellow, Black "},
        "correct": "A"
    },

    {
        "question": "Which city did the franchise move from when it became the Ravens?",
        "options": {"A": "Los Angeles", "B": "St. Louis", "C":"Oakland ", "D":"Cleveland"},
        "correct": "D"
    },

    {
        "question": "Who was the Baltimore Ravens first ever draft pick?",
        "options": {"A": "Jonathan Ogden", "B": "Ray Lewis ", "C": "Justin Tucker", "D": "DeRon Jenkins"},
        "correct": "A"
    },

    {
        "question": "Who holds the franchise record for most career interceptions with the Ravens?",
        "options": {"A": "Ed Reed", "B": "Ray lewis", "C": "Terell Suggs", "D": "Peter Boulware" },
        "correct": "A"
    },

    {
        "question": "Which Ravens player is the franchise’s all‑time leader in career sacks?",
        "options": {"A": "Jonathan Ogden", "B": "Peter Boulware", "C": "Ray Lewis", "D": "Terell Suggs"},
        "correct": "D"
    }

]



#START PAGE
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['player_name']
        session['player_name'] = name
        session['score'] = 0
        return redirect(url_for('questions_page'))
    return render_template('Ravens.html')


#QUESTIONS PAGE
@app.route('/questions', methods=['GET', 'POST'])
def questions_page():
    q_index = int(request.args.get('q', 0))  # Default to 0
    message = ""

    # Check if we finished all questions
    if q_index >= len(questions):
        return redirect(url_for('results'))

    question_data = questions[q_index]

    if request.method == 'POST':
        selected_answer = request.form.get('answer') #get whatever radio button that was selected
        correct_answer = question_data['correct']

        if selected_answer == correct_answer:
            session['score'] = session['score'] + 1
            message = "Correct!"
        else:
            message = f"Wrong answer! The correct answer is {correct_answer}. "

        #move to the next question

        return redirect(url_for('questions_page', q=q_index + 1))

    return render_template('TriviaQuestions.html', question_data=question_data, message=message)

# RESULTS PAGE
@app.route('/results')
def results():
    player_name = session.get('player_name', "Player")
    score = session.get('score', 0)
    total = len(questions)

    # Ensure we calculate percentage correctly
    percentage = (score / total) * 100

    #save score to the database
    save_score(player_name, score)


    if percentage >= 70:
        message = "Congratulations"
    else:
        message = "Better luck next time"

    top_players = get_top_players()

    return render_template('Results.html', player_name=player_name, score=score, total=total, message=message,top_players=top_players)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    #app.run(debug=True)
