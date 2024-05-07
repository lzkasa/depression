from flask import Flask, render_template, request, url_for, redirect, g
import sqlite3
import csv

DATABASE = 'user_database.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 在数据库中查找用户信息
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            # 用户存在，重定向到 zcb 页面
            return redirect(url_for('zcb'))
        else:
            # 用户不存在或密码错误，重新显示登录页面
            return render_template('login.html', error="用户名或密码错误")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        try:
            # 将新用户的用户名和密码存入数据库
            cursor = get_db().cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            get_db().commit()
        except sqlite3.IntegrityError:
            # 用户名已存在，显示错误信息
            return render_template('register.html', error="用户名已存在")

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/zcb')
def zcb():
    return render_template('zcb.html')

@app.route("/fenxi", methods=["POST"])
def calculate_score():
    global score, ba
    score = 0
    for cc in range(1, 21):
        cc = 't' + str(cc)
        answer = request.form.get(cc)
        score += int(answer)
        ba = score / 80

    return render_template('fenxi.html', score=ba)

@app.route("/zz", methods=['POST'])
def sub():
    if ba >= 0.8:
        label = 'suicide'
    else:
        label = 'non-suicide'
    name = request.form['name']
    introduction = request.form['jieshao']
    phone = request.form['phone']
    label = label
    with open('data.csv', mode='a', newline='', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name, phone, introduction, label])
    return render_template('222.html')

if __name__ == '__main__':
    app.run(debug=True)
