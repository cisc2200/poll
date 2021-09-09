from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import sqlite3
from collections import Counter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cisc2200'

DB_NAME = 'votes.db'


def reset_db():
    connection = sqlite3.connect(DB_NAME)
    with open('schema.sql') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def read_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    votes = []
    for row in cur.execute('SELECT choice FROM votes'):
        votes.extend(row[0].split(','))
    conn.close()
    return votes


def insert_or_update_vote(ip, vote):
    vote = ','.join(vote)
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO votes (ip, choice) VALUES (?, ?)',
                     (ip, vote))
        conn.commit()
    except sqlite3.IntegrityError:
        flash('You cannot submit more than once!')
    finally:
        conn.close()


@app.route("/<int:num_choices>", methods=('GET', 'POST'))
def index(num_choices=6):
    if request.method == 'POST':
        vote = request.form.getlist('vote')
        ip = request.remote_addr
        insert_or_update_vote(ip, vote)
        return redirect(url_for('results', num_choices=num_choices))
    choices = []
    for x in range(0, num_choices):
        choices.append(chr(ord('A') + x))
    return render_template('index.html', num_choices=num_choices, choices=choices)


@app.route("/<int:num_choices>/results")
def results(num_choices=6):
    count = [0 for _ in range(0, num_choices)]
    choices = []
    for x in range(0, num_choices):
        choices.append(chr(ord('A') + x))
    return render_template('results.html', num_choices=num_choices, choices=choices, count=count)


@app.route('/stuff', methods=['GET'])
def stuff():
    votes = read_from_db()
    c = Counter(votes)
    return jsonify(c)


@app.route("/<int:num_choices>/reset")
def reset(num_choices=6):
    reset_db()
    return redirect(url_for('results', num_choices=num_choices))
