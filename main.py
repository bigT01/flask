import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
db = SQLAlchemy()

app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'


db.init_app(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    image = db.Column(db.String)
    source = db.Column(db.String)

class Veritification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

# user = Users(email='Tanat8511@gmail.com', password='Tanat2004')
# user2 = Users(email='212103@astanait.edu.kz', password='212103')
# user3 = Users(email='Ayau@mail.ru', password='qwerty123456')
# user4 = Users(email='Diana@astanait.edu.kz', password='12345678')

# news1 = News(idUser=1,
#              title='hey hey hey hey hey hey hey hey hey',
#              content='Hello world',
#              category='business',
#              image='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.agilenative.com%2F2017%2F01%2Fhello-world%2F&psig=AOvVaw1WwccZ7fu8q3W-tY32PsYr&ust=1667487048177000&source=images&cd=vfe&ved=0CA0QjRxqFwoTCMjborvfj_sCFQAAAAAdAAAAABAE',
#              source='link')
#
# news2 = News(idUser=2,
#              title='flowers is die',
#              content='some flowers is going to die eeee',
#              category='economics',
#              image='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.farmersalmanac.com%2Fforget-me-not-blue-flowers&psig=AOvVaw2F48_dgB8PGrk2xSPdZFLy&ust=1667487257558000&source=images&cd=vfe&ved=0CA0QjRxqFwoTCNCU5aDgj_sCFQAAAAAdAAAAABAE',
#              source='link')
#
# news3 = News(idUser=3,
#              title='fast food',
#              content=' fast food is very danger if eat it a lot',
#              category='eat',
#              image='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.wired.com%2Fstory%2Fmcdonalds-big-data-dynamic-yield-acquisition%2F&psig=AOvVaw2zBMHDaykw14-QUMD0SSK7&ust=1667487427901000&source=images&cd=vfe&ved=0CA0QjRxqFwoTCODJpPDgj_sCFQAAAAAdAAAAABAE',
#              source='link')


# db.session.add(news1)
# db.session.add(news2)
# db.session.add(news3)

# db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/checking', methods=['GET', 'POST'])
def checking():
    email = (request.form['email'])
    password = (request.form['password'])
    for i in Users.query.all():
        if(email == i.email and password == i.password):
            verity = Veritification(idUser=i.id, email=i.email, password=i.password)
            db.session.add(verity)
            db.session.commit()
            return flask.redirect('/news')
    return flask.redirect('/login')


@app.route('/news', methods=['GET', 'POST'])
def news():
    if (Veritification.query.all()[0].idUser != -1):
        return render_template('news.html', responce=News.query.all())
    else:
        return flask.redirect('/error')


@app.route('/mynews')
def mynews():
    if (Veritification.query.all()[0].idUser != -1):
        sortedData = News.query.filter_by(idUser=Veritification.query.all()[0].idUser).all()
        return render_template('myNews.html', response=sortedData)
    else:
        return flask.redirect('/error')


@app.route('/addnews')
def addnews():
    if (Veritification.query.all()[0].idUser != -1):
        return render_template('addNews.html')
    else:
        return flask.redirect('/error')



@app.route('/posting', methods=['GET', 'POST'])
def posting():
    if (Veritification.query.all()[0].idUser != -1):
        title = (request.form['title'])
        content = (request.form['content'])
        image = (request.form['image'])
        addingNews = News(idUser=Veritification.query.all()[0].idUser,
                     title=title,
                     content=content,
                     category='business',
                     image=image,
                     source='link')
        db.session.add(addingNews)
        db.session.commit()

        return flask.redirect('/news')
    else:
        return flask.redirect('/error')

@app.route('/logout')
def logout():
    db.session.query(Veritification).delete()
    db.session.commit()
    return flask.redirect('/')

@app.route('/error')
def error():
    return render_template('error.html')










if __name__ == '__main__':
    app.run(debug=True)

