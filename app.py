from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
app.secret_key = app.secret_key = 'a_very_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bodik.kovalchuk1998@gmail.com'
app.config['MAIL_PASSWORD'] = 'Omega/969809'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def __repr__(self):
    return '<Article %r>' % self.id
@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text= request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавленні статті сталась помилка"
    else:
        return render_template('create_article.html')

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message_content = request.form.get('message')
        msg = Message('Нове повідомлення з форми підтримки',
                      recipients=['bodik.kovalchuk1998@gmail.com'])
        msg.body = f"""
        Ім'я: {first_name} {last_name}
        Електронна пошта: {email}
        Телефон: {phone}
        Повідомлення: {message_content}
        """

        try:
            mail.send(msg)
            flash('Повідомлення успішно відправлено!', 'success')
            return redirect('/home')
        except Exception as e:
            flash(f'Помилка при відправці повідомлення: {str(e)}', 'danger')
            return redirect('/support')

    return render_template("support.html")

@app.route('/login')
def login():
    return render_template("loggin.html")

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/del')
def post_del(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При видаленні статті сталась помилка "


@app.route('/posts/<int:id>/up', methods=['POST', 'GET'])
def post_up(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text= request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавленні статті сталась помилка"
    else:
        article = Article.query.get(id)
        return render_template('post_up.html', article=article)



if __name__ == "__main__":
    app.run(debug=True)
