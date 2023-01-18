#import app into route file:
from app import app
#import for jinja2:
from flask import render_template



# create definitions of all of our routes through:
@app.route('/')
def homePage():
    return render_template('index.html')


@app.route('/favorite5')
def favorite5():
    artists = ['Michael Jackson', 'Burna Boy', 'Sam Smith', 'Adele', 'Dexta Daps']
    return render_template('favorite5.html', artists = artists)