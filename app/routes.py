#import app into route file:
from app import app
#import for jinja2:
from flask import render_template, request, redirect, url_for
from.forms import signupform, loginform, pokemonform, postform
import requests
from .models import User, Catch, Pokemon
from flask_login import login_user, logout_user, login_required, current_user
# import requests as r

# create definitions of all of our routes through:
@app.route('/')
def homePage():
    return render_template('index.html')


@app.route('/pokemon', methods=["GET","POST"])    
def pokemon():

    pokemon = Pokemon.query.all()
    if current_user.is_authenticated:
        my_pokemon = Catch.query.filter_by(user_id=current_user.id).all()
        # pokemon = {pokemon.pokemon_id for pokemon in my_pokemon}

        for p in my_pokemon:
            print(p)
            if p.id in pokemon:
                p.caught = True


    form = pokemonform()
    if request.method == 'POST':
        pokeName = form.pokemon.data
        pokemon = Pokemon.query.filter_by(name=pokeName).first()
        print(pokemon)
        
        if pokemon:
            return render_template('pokemon.html', form = form, pokemon = pokemon)

        url = 'https://pokeapi.co/api/v2/pokemon/'
        response = requests.get(url + pokeName)
        print (response)
        print (response.ok)
        if response.ok:
            data = response.json()

            names = data['forms'][0]['name']
            abilities = data['abilities'][0]['ability']['name']
            sprites = data['sprites']['front_shiny']
            hp_stats = data['stats'][0]['base_stat']
            attack_stats = data['stats'][1]['base_stat']
            defense_stats = data['stats'][2]['base_stat']
            moves = data['moves'][0]['move']['name']

            pokemon=Pokemon(names, abilities, sprites, hp_stats, attack_stats, defense_stats, moves)

            pokemon.saveToDB()
            # pokemon = {
            #     'name': names,
            #     'ability': abilities,
            #     'experience': experience,
            #     'sprite': sprites,
            #     'hp_stat': hp_stats,
            #     'attack_stat': attack_stats,
            #     'defense_stat': defense_stats,
            #     'move': moves
            # }
            return render_template('pokemon.html', form = form, pokemon = pokemon)

        # return(f'Pokemon:\nName: {names}, ability: {drivers}, base-experience: {experience}, sprite: {sprites}, and stats: {hp_stats}, {attack_stats}, {defense_stats}.')

    return render_template('pokemon.html', form = form)


# @app.route('/my_pokemon', methods=["GET"])
# def caught():
    
#      if len(my_pokemon) == 5:
#             print('Stop')
#     else:
#         print(my_pokemon)
# return render_template('my_pokemon.html')


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






# @app.route('/posts/create', methods=["GET", "POST"])
# def createPost():
#     form = postform()
#     if request.method == 'POST':
#         if form.validate():
#             title = form.title.data
#             caption = form.caption.data
#             img_url = form.img_url.dta

#             post = Pokemon(title, caption, img_url)
#             post.saveToDB()
         


#     return render_template('createpost.html', form = form)




@app.route('/mypokemon/<string:pokemonName>/catch', methods=["GET"])
@login_required
def pokecatch(pokemonName):
    pokemon=Pokemon.query.filter(Pokemon.name==pokemonName).first()
    catch_instance = Catch(current_user.id, pokemon.id)
    catch_instance.saveToDB()
    

    return redirect(url_for('pokemon'))
    
    # p = (self, name, ability, sprite, hp_stats, attack_stats, defense_stats, moves):
    # return render_template('catch.html')
    # limit to 5 pokemon   

@app.route('/mypokemon/<int:pokemon_id>/release', methods=["GET"])
@login_required
def pokerelease(pokemon_id):
    catch_instance = Catch.query.filter_by(pokemon_id=pokemon_id).filter_by(user_id=current_user.id).first()
    catch_instance.deleteFromDB()

    return redirect(url_for('pokemon'))
  












    #   <!-- {% if current_user.is_authenticated %} -->

    #             <!-- {% if p.caught %} -->
    #       <a href="{{ url_for('pokecatch', pokemon_id=pokemon.id) }}" class="btn btn-primary">CATCH!</a>
    #             <!-- {% else %}
    #             <a href="{{ url_for('pokerelease', pokemon_id=pokemon.id) }}" class="btn btn-danger">Release</a>
    #             {% endif %} -->

    #         <!-- {% endif %} -->