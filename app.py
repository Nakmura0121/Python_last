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
    

#新規ユーザー登録
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
    return render_template('register_result.html')

#ログイン
@app.route('/login')
def login_form():
    return render_template('login.html')
    
@app.route('/login_exe', methods=['POST'])
def login_exe():
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if db.admin_login(mail,password):
         session['admin'] = True
         session.permanent = True
         return redirect(url_for('admin_login'))
    elif db.login(mail, password):
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
    
#管理者ログイン
@app.route('/admin')
def admin_login():
    if 'admin' in session:
        return render_template('admin.html') 
    else :
        return redirect(url_for('index'))

#マイページ  
@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html') 
    else :
        return redirect(url_for('index'))

#ログアウト
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# 図書登録
@app.route('/register_book')
def register_book():
    return render_template('register_book_form.html')

@app.route('/register_book_exe', methods=['POST'])
def register_book_exe():
    title = request.form.get('title')
    author = request.form.get('author')
    company = request.form.get('company')
    isbn =request.form.get('isbn')
    if title=='':
        error='図書名が未入力です'
        return render_template('register_book_form.html', error=error)
    if author =='':
        error='著者が未入力です'
        return render_template('register_book_form.html', error=error)
    if company=='':
        error='出版社が未入力です'
        return render_template('register_book_form.html', error=error)
    if isbn=='':
        error='ISBNが未入力です'
        return render_template('register_book_form.html', error=error)
    count = db.insert_book(title, author, company, isbn)
    if count == 1:
        msg = '図書の登録が完了しました。'
        return redirect(url_for('register_book_result', msg=msg))    
    else: 
        error = '図書の登録に失敗しました。'
        return render_template('register_book_form.html', error=error)
    
@app.route('/register_book_result')
def register_book_result():
    return render_template('register_book_result.html')

#図書一覧
@app.route('/select_book')
def select_book():
    select_book = db.select_book()
    return render_template('select_book.html', book=select_book)

#図書削除
@app.route('/delete_book')
def delete_book():
    return render_template('delete_book.html')

@app.route('/delete_book_exe', methods=['POST'])
def delete_book_exe():
    id = request.form.get('id')
    
    if id == '':
        error = '図書IDが入力されていません'
        return render_template('delete_book.html', error=error)
    
    count = db.delete_book(id)
    
    if count == 1:
        msg = '対象の図書を削除しました。'
        return redirect(url_for('delete_book_success', msg=msg))
    else:
        error = '対象の図書の削除に失敗しました。'
        return render_template('delete_book.html', error=error )
    
@app.route('/delete_book_success')
def delete_book_success():
    return render_template('delete_book_success.html')

#本検索
@app.route('/search_book')
def search_book():
    return render_template('search_book.html')

@app.route('/search_book_exe', methods=['POST'])
def search_book_exe():
    title = request.form.get('title')
    book_list = db.search_book(title)
    return render_template('select_book.html', book=book_list)
    
#図書情報更新
@app.route('/update_book')
def update_book():
    return render_template('update_book.html')

@app.route('/update_book_exe', methods=['POST'])
def update_book_exe():
   
    id = request.form.get('id')
    title = request.form.get('title')
    author = request.form.get('author')
    company = request.form.get('company')
    isbn = request.form.get('isbn')
    
    if id == '':
        error = '図書IDが入力されていません'
        return render_template('update_book.html', error=error)
    
    count = db.update_book(id, title, author, company, isbn)
    
    if count == 1:
        msg = '図書の情報を編集しました'
        return redirect(url_for('update_book_success', msg=msg))
    else:
        error = '図書の情報の編集に失敗しました'
        return render_template('update_book.html', error=error)
    
@app.route('/update_book_success')
def update_book_success():
    return render_template('update_book_success.html')
    

if __name__ == "__main__":
    app.run(debug=True)