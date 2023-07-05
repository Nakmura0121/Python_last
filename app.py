from flask import Flask, render_template, request, redirect, url_for, session
import db, string, random
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


@app.route('/', methods=['GET'])
def index():
    msg=request.args.get('msg')
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)
    

#新規登録
@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    if user_name=='':
        error='名前が未入力です'
        return render_template('register.html', error=error)
    if mail =='':
        error='メールアドレスが未入力です'
        return render_template('register.html', error=error)
    if password=='':
        error='パスワードが未入力です'
        return render_template('register.html', error=error)
    count = db.insert_user(user_name, mail, password)
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('register_result', msg=msg))    
    else: 
        error = '登録に失敗しました。'
        return render_template('register.html', error=error)
    
@app.route('/register_result')
def register_result():
    return render_template('register-result.html')

#ログイン
@app.route('/login')
def login_form():
    return render_template('login.html')
    
@app.route('/login_exe', methods=['POST'])
def login_exe():
    mail = request.form.get('mail')
    password = request.form.get('password')
    if db.login(mail, password):
        session['user'] = True
        session.permanent = True
        return redirect(url_for('mypage'))
    else :
        error ='ログインに失敗しました。'
        input_data = {
            'mail': mail,
            'password': password
        }
        return render_template('index.html', error = error, data = input_data)
    
@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html') 
    else :
        return redirect(url_for('index'))
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# ブック
@app.route('/register_book')
def register_book():
    return render_template('register-book-form.html')

@app.route('/register_book_exe', methods=['POST'])
def register_book_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    company = request.form.get('company')
    isbn =request.form.get('isbn')
    if title=='':
        error='図書名が未入力です'
        return render_template('register-book-form.html', error=error)
    if author =='':
        error='著者が未入力です'
        return render_template('register-book-form.html', error=error)
    if company=='':
        error='出版社が未入力です'
        return render_template('register-book-form.html', error=error)
    if isbn=='':
        error='ISBNが未入力です'
        return render_template('register-book-form.html', error=error)
    count = db.insert_book(title, author, company, isbn)
    if count == 1:
        msg = '図書の登録が完了しました。'
        return redirect(url_for('register_book_result', msg=msg))    
    else: 
        error = '図書の登録に失敗しました。'
        return render_template('register-book-form.html', error=error)
    
@app.route('/register_book_result')
def register_book_result():
    return render_template('register-book-result.html')
    
    
if __name__ == "__main__":
    app.run(debug=True)