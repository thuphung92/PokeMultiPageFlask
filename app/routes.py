from flask import render_template, request, redirect, url_for
import requests
from app import app #from folder app, import app instance
from .forms import SearchForm, RegisterForm, LoginForm
from.models import User
from flask_login import login_user

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemon', methods=['GET','POST'])
def pokemon():
    pokemon_name = None
    form = SearchForm()
    # Validate Form
    if form.validate_on_submit():
        pokemon_name = form.pokemon_name.data.lower()
        form.pokemon_name.data = '' #clear form after hitting search
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            if not data:
                error_string = "Something went wrong. Couldn't connect the library."
                return render_template("pokemon.html.j2", form=form, error = error_string)
            
            pokemon_dict = {
                'pokemon_image': data['sprites']['other']['dream_world']['front_default'],
                'pokemon_name': data['name'],
                'ability_name': data['abilities'][0]['ability']['name'],
                'base_experience': data['base_experience'],
                'sprite_ULR': data['sprites']['front_shiny']
                }
            return render_template("pokemon.html.j2", form=form, pokemon = pokemon_dict)
        error_string = f'There is no pokemon named {pokemon_name}'
        return render_template("pokemon.html.j2", form=form, error=error_string)
    return render_template('pokemon.html.j2', form=form)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            #get info
            new_user_dict={
                'first_name': form.first_name.data.title(),
                'last_name': form.last_name.data.title(),
                'email': form.email.data,
                'password': form.password.data
            }
            #create & save new user
            new_user = User()
            new_user.from_dict(new_user_dict)
        except:
            error_string='There was a problem creating your account. Please try again!'
            return render_template('register.html.j2', form=form, error=error_string)
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email=form.email.data.lower()
        password=form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_hashed_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html.j2', form=form)
