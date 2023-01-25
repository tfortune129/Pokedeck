from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class pokemonform(FlaskForm):
    pokemon = StringField("Input Pokémon", validators = [DataRequired()])
    submit = SubmitField()

class signupform(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class loginform(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField()

class postform(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    img_url = StringField("Image URL", validators = [DataRequired()])
    caption = StringField("Caption", validators = [])
    submit = SubmitField()