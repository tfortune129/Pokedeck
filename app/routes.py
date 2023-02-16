#import app into route file:
from app import app
#import for jinja2:
from flask import render_template, request, redirect, url_for, flash
from.forms import signupform, loginform, pokemonform, PokeCaught
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

    # pokemon = Pokemon.query.all()
    # if current_user.is_authenticated:
    #     my_pokemon = Catch.query.filter_by(user_id=current_user.id).all()
    #     # pokemon = {pokemon.pokemon_id for pokemon in my_pokemon}

    #     for p in my_pokemon:
    #         print(p)
    #         if p.id in pokemon:
    #             p.caught = True


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
        
        else:
            flash('This Pokémon is not available, please try again.', category='warning')
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

    return render_template('pokemon.html', form = form)



@app.route('/catch/<int:pokemon_id>', methods=["GET", "POST"])
@login_required
def pokecatch(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    
    if pokemon.caught:
        flash(f'Sorry, {pokemon.name.title()} has already been caught.', category='warning')
    elif Catch.query.filter_by(user_id=current_user.id).count() >= 5:
        flash('Sorry, you can only catch up to 5 Pokemon.', category='warning')
    else:
        catch = Catch(user_id=current_user.id, pokemon_id=pokemon.id)
        catch.saveToDB()
        pokemon.caught = True
        pokemon.saveChanges()
        flash(f'{pokemon.name.title()} has been caught and added to your collection.', category='success')
    return redirect(url_for('pokemon'))




# @app.route('/catch/<int:pokemonName>', methods=["GET", "POST"])
# @login_required
# def pokecatch(pokemonName):
#         catch = Pokemon.query.filter_by(name = pokemonName)
#         # query, if, flash, redirect
#         # if len() caught_pokemon = Pokemon.query.filter_by(user_id = current_user.id)
#         # if catch and catch.user_id == current_user.id:
#         if catch.caught == False:
#             catch.saveToDB()
#             flash(f'{catch.name.title()} is now ready to fight', category='success')
#             return redirect(url_for('pokemon'))
#         else:
#             flash(f'Unfortunately, {catch.name.title()} is not available :(', category='warning')
#             return redirect(url_for('pokemon'))




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




@app.route('/mypokemon', methods=['GET'])
@login_required
def mypokemon():
    my_pokemon = Pokemon.query.join(Catch).filter(Catch.user_id==current_user.id).all()
    return render_template('catch.html', catch=my_pokemon)



@app.route('/release/<int:pokemon_id>', methods=['GET', 'POST'])
@login_required
def pokerelease(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    catch = Catch.query.filter(pokemon_id==pokemon_id).first()
    # catch = Pokemon.query.join(Catch).filter(Catch.user_id==current_user.id, Pokemon.id==pokemon_id).first()
    if catch:
        # pokemon = catch.catch
        # pokemon.deleteFromDB()
        catch.deleteFromDB()
        flash(f"{pokemon.name.title()} has been removed from your collection.", 'success')
    else:
        flash("You don't have that Pokémon in your collection.", 'warning')
    return redirect(url_for('mypokemon'))




# def pokerelease(pokemon_id):
#     pokemon = Pokemon.query.join(Catch).filter(Catch.user_id==current_user.id, Pokemon.id==pokemon_id).first()
#     if pokemon:
#         pokemon.deleteFromDB()
#         flash(f"{pokemon.name.title()} has been removed from your collection.", 'success')

#     else:
#         flash("You don't have that Pokémon in your collection.", 'warning')

#     return redirect(url_for('mypokemon'))
    
    
    
    
# pokemon = Pokemon.query.filter_by(id=pokemon_id).filter_by(user_id=current_user.id).first()



# def pokerelease(pokemon_id):
#     catch_instance = Catch.query.filter_by(pokemon_id=pokemon_id).filter_by(user_id=current_user.id).first()
#     catch_instance.deleteFromDB()

#     return redirect(url_for('pokemon'))
  


# @app.route('/mypokemon', methods=["POST"])
# @login_required
# def caught():
#     pokecatch = Pokemon.query.all()
#     if current_user.is_authenticated:
#         my_pokemon = Catch.query.filter_by(user_id=current_user.id).all()

#         for pokemon in my_pokemon:
#             if pokemon.id in pokemon:
#                 pokemon.caught = True
#     return render_template('mypokemon.html', pokecatch = pokecatch)















# JUNK:

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




    #   <!-- {% if current_user.is_authenticated %} -->

    #             <!-- {% if p.caught %} -->
    #       <a href="{{ url_for('pokecatch', pokemon_id=pokemon.id) }}" class="btn btn-primary">CATCH!</a>
    #             <!-- {% else %}
    #             <a href="{{ url_for('pokerelease', pokemon_id=pokemon.id) }}" class="btn btn-danger">Release</a>
    #             {% endif %} -->

    #         <!-- {% endif %} -->