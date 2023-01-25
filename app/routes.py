#import app into route file:
from app import app
#import for jinja2:
from flask import render_template, request, redirect, url_for
from.forms import signupform, loginform, pokemonform, postform
import requests
from .models import User
from flask_login import login_user, logout_user, current_user
import requests as r

# create definitions of all of our routes through:
@app.route('/')
def homePage():
    return render_template('index.html')


@app.route('/pokemon', methods=["POST"])    
def pokemon():
    form = pokemonform()
    if request.method == 'POST':
        pokeName = form.pokemon.data
        url = 'https://pokeapi.co/api/v2/pokemon/'
        response = requests.get(url + pokeName)
        print (response)
        print (response.ok)
        if response.ok:
            data = response.json()

            names = data['forms'][0]['name']
            drivers = data['abilities'][0]['ability']
            experience = data['base_experience']
            sprites = data['sprites']['front_shiny']
            hp_stats = data['stats'][0]['base_stat']
            attack_stats = data['stats'][1]['base_stat']
            defense_stats = data['stats'][2]['base_stat']

            pokemon = {
                'name': names,
                'driver': drivers,
                'experince': experience,
                'sprite': sprites,
                'hp_stat': hp_stats,
                'attack_stat': attack_stats,
                'defense_stat': defense_stats
            }
            return render_template('pokemon.html', form = form, pokemon = pokemon)

        # return(f'Pokemon:\nName: {names}, ability: {drivers}, base-experience: {experience}, sprite: {sprites}, and stats: {hp_stats}, {attack_stats}, {defense_stats}.')

    return render_template('pokemon.html', form = form)



# create form route:
@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = signupform()
    print(request.method)
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            print(username, email, password)
            
            #add user to database
            user = User(username, email, password)
            print(user)

            user.saveToDB()

            return redirect(url_for('homePage'))

    return render_template('signup.html', form = form)




@app.route('/login', methods=["GET", "POST"])
def login():
    form = loginform()
    
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    
                    login_user(user)
                
                else:
                    print ('Wrong Password, please try again.')
            
            else:
                print('Username does not exist.')

    return render_template('login.html', form = form)







@app.route('/logout', methods=["GET"])
def logout():
    logout_user()

    return redirect(url_for('login'))


@app.route('/posts/create', methods=["GET", "POST"])
def createPost():
    form = postform()
    if request.method == 'POST':
        if form.validate():
            title = form.title.data
            caption = form.caption.data
            img_url = form.img_url.dta

            post = Post(title, caption, img_url)
            post.saveToDB()
         


    return render_template('createpost.html', form = form)