from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(), 
        Length(min=3, max=64, message="Le nom d'utilisateur doit contenir entre 3 et 64 caractères")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(), 
        Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères")
    ])
    password2 = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), 
        EqualTo('password', message="Les mots de passe doivent correspondre")
    ])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cette adresse email est déjà utilisée.')

class ProfileForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[
        DataRequired(), 
        Length(min=3, max=64)
    ])
    current_password = PasswordField('Mot de passe actuel')
    new_password = PasswordField('Nouveau mot de passe', validators=[
        Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères")
    ])
    confirm_password = PasswordField('Confirmer le nouveau mot de passe', validators=[
        EqualTo('new_password', message="Les mots de passe doivent correspondre")
    ])
    profile_photo = FileField('Photo de profil', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Seules les images sont autorisées!')
    ])

class VoiceTranslationForm(FlaskForm):
    target_language = SelectField('Langue cible', choices=[
        ('en', 'Anglais'),
        ('es', 'Espagnol'),
        ('de', 'Allemand'),
        ('it', 'Italien'),
        ('pt', 'Portugais'),
        ('ru', 'Russe'),
        ('ja', 'Japonais'),
        ('ko', 'Coréen'),
        ('zh', 'Chinois'),
        ('ar', 'Arabe')
    ], validators=[DataRequired()])
    transcribed_text = HiddenField()

class FileTranslationForm(FlaskForm):
    file = FileField('Fichier à traduire', validators=[
        FileRequired(),
        FileAllowed(['txt', 'json'], 'Seuls les fichiers .txt et .json sont autorisés!')
    ])
    target_language = SelectField('Langue cible', choices=[
        ('en', 'Anglais'),
        ('es', 'Espagnol'),
        ('de', 'Allemand'),
        ('it', 'Italien'),
        ('pt', 'Portugais'),
        ('ru', 'Russe'),
        ('ja', 'Japonais'),
        ('ko', 'Coréen'),
        ('zh', 'Chinois'),
        ('ar', 'Arabe'),
        ('fr', 'Français')
    ], validators=[DataRequired()])

class EditTranslationForm(FlaskForm):
    translated_text = TextAreaField('Texte traduit', validators=[DataRequired()])

class TextTranslationForm(FlaskForm):
    source_text = TextAreaField('Texte à traduire', validators=[
        DataRequired(message="Veuillez saisir le texte à traduire")
    ], render_kw={"placeholder": "Saisissez ou collez votre texte ici...", "rows": 6})
    target_language = SelectField('Langue cible', choices=[
        ('en', 'Anglais'),
        ('es', 'Espagnol'),
        ('de', 'Allemand'),
        ('it', 'Italien'),
        ('pt', 'Portugais'),
        ('ru', 'Russe'),
        ('ja', 'Japonais'),
        ('ko', 'Coréen'),
        ('zh', 'Chinois'),
        ('ar', 'Arabe'),
        ('fr', 'Français')
    ], validators=[DataRequired()])
