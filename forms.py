from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from config import User


class SearchForm(FlaskForm):
    text = StringField('Poszukiwana wartosc', validators=[DataRequired()])
    choice = RadioField("Cytat", choices=["Cytat","Autor","Tag"])
    submit = SubmitField('Szukaj')
class LoginForm(FlaskForm):
    name = StringField('Nazwa uzytkownika', validators=[DataRequired()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    remember_me = BooleanField('Pamietaj mnie')
    submit = SubmitField('Zaloguj sie')


class RegistrationForm(FlaskForm):
    name = StringField('Nazwa uzytkownika', validators=[DataRequired()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    password2 = PasswordField(
        'Powtorz haslo:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different name.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')