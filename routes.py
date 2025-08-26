import os
import json
import csv
from io import StringIO
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file, make_response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app import db
from models import User, Translation
from forms import LoginForm, RegisterForm, ProfileForm, VoiceTranslationForm, FileTranslationForm, EditTranslationForm, TextTranslationForm
from utils import translate_text, detect_language, allowed_file

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.voice_translation'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Connexion réussie!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard.voice_translation'))
        flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.voice_translation'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))

# Main routes
@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.voice_translation'))
    return redirect(url_for('auth.login'))

# Dashboard routes
@dashboard_bp.route('/voice_translation', methods=['GET', 'POST'])
@login_required
def voice_translation():
    form = VoiceTranslationForm()
    if form.validate_on_submit():
        # Process voice translation
        transcribed_text = request.form.get('transcribed_text')
        target_language = form.target_language.data
        
        if transcribed_text:
            # Detect source language
            source_language = detect_language(transcribed_text)
            
            # Translate text
            translated_text = translate_text(transcribed_text, target_language, source_language)
            
            # Save to database
            translation = Translation(  # type: ignore
                user_id=current_user.id,
                original_text=transcribed_text,
                translated_text=translated_text,
                source_language=source_language,
                target_language=target_language,
                translation_type='voice'
            )
            db.session.add(translation)
            db.session.commit()
            
            flash('Traduction vocale sauvegardée!', 'success')
            return render_template('dashboard/voice_translation.html', 
                                 form=form, 
                                 translation=translation)
    
    return render_template('dashboard/voice_translation.html', form=form)

@dashboard_bp.route('/text_translation', methods=['GET', 'POST'])
@login_required
def text_translation():
    form = TextTranslationForm()
    if form.validate_on_submit():
        source_text = form.source_text.data.strip() if form.source_text.data else ""
        target_language = form.target_language.data
        
        if source_text:
            # Detect source language
            source_language = detect_language(source_text)
            
            # Translate text
            translated_text = translate_text(source_text, target_language, source_language)
            
            # Save to database
            translation = Translation(  # type: ignore
                user_id=current_user.id,
                original_text=source_text,
                translated_text=translated_text,
                source_language=source_language,
                target_language=target_language,
                translation_type='text'
            )
            db.session.add(translation)
            db.session.commit()
            
            flash('Traduction de texte sauvegardée!', 'success')
            return render_template('dashboard/text_translation.html', 
                                 form=form, 
                                 translation=translation)
    
    return render_template('dashboard/text_translation.html', form=form)

@dashboard_bp.route('/file_translation', methods=['GET', 'POST'])
@login_required
def file_translation():
    form = FileTranslationForm()
    if form.validate_on_submit():
        file = form.file.data
        target_language = form.target_language.data
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Read file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    if filename.endswith('.json'):
                        content = json.load(f)
                        original_text = json.dumps(content, ensure_ascii=False, indent=2)
                    else:
                        original_text = f.read()
                
                # Detect language and translate
                source_language = detect_language(original_text)
                translated_text = translate_text(original_text, target_language, source_language)
                
                # Create translated file
                translated_filename = f'translated_{filename}'
                translated_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], translated_filename)
                
                with open(translated_filepath, 'w', encoding='utf-8') as f:
                    if filename.endswith('.json'):
                        # For JSON files, translate values while preserving structure
                        translated_content = json.loads(translated_text) if translated_text.startswith('{') else {"translated_content": translated_text}
                        json.dump(translated_content, f, ensure_ascii=False, indent=2)
                    else:
                        f.write(translated_text)
                
                # Save to database
                translation = Translation(  # type: ignore
                    user_id=current_user.id,
                    original_text=original_text,
                    translated_text=translated_text,
                    source_language=source_language,
                    target_language=target_language,
                    translation_type='file',
                    filename=filename
                )
                db.session.add(translation)
                db.session.commit()
                
                flash('Fichier traduit avec succès!', 'success')
                return render_template('dashboard/file_translation.html', 
                                     form=form, 
                                     translation=translation,
                                     download_file=translated_filename)
                
            except Exception as e:
                flash(f'Erreur lors de la traduction du fichier: {str(e)}', 'error')
                os.remove(filepath)  # Clean up uploaded file
        else:
            flash('Type de fichier non autorisé.', 'error')
    
    return render_template('dashboard/file_translation.html', form=form)

@dashboard_bp.route('/download/<filename>')
@login_required
def download_file(filename):
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    flash('Fichier non trouvé.', 'error')
    return redirect(url_for('dashboard.file_translation'))

@dashboard_bp.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    translations = current_user.translations.order_by(Translation.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('dashboard/history.html', translations=translations)

@dashboard_bp.route('/edit_translation/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_translation(id):
    translation = Translation.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = EditTranslationForm(obj=translation)
    
    if form.validate_on_submit():
        translation.translated_text = form.translated_text.data
        translation.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Traduction mise à jour!', 'success')
        return redirect(url_for('dashboard.history'))
    
    return render_template('dashboard/edit_translation.html', form=form, translation=translation)

@dashboard_bp.route('/delete_translation/<int:id>')
@login_required
def delete_translation(id):
    translation = Translation.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(translation)
    db.session.commit()
    flash('Traduction supprimée!', 'success')
    return redirect(url_for('dashboard.history'))

@dashboard_bp.route('/export_history')
@login_required
def export_history():
    translations = current_user.translations.order_by(Translation.created_at.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Type', 'Langue source', 'Langue cible', 'Texte original', 'Texte traduit', 'Fichier'])
    
    for t in translations:
        writer.writerow([
            t.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            t.translation_type,
            t.source_language,
            t.target_language,
            t.original_text[:100] + '...' if len(t.original_text) > 100 else t.original_text,
            t.translated_text[:100] + '...' if len(t.translated_text) > 100 else t.translated_text,
            t.filename or ''
        ])
    
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=historique_traductions_{current_user.username}.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

@dashboard_bp.route('/statistics')
@login_required
def statistics():
    stats = current_user.get_translation_stats()
    recent_translations = current_user.translations.order_by(Translation.created_at.desc()).limit(5).all()
    return render_template('dashboard/statistics.html', stats=stats, recent_translations=recent_translations)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        # Check if username is being changed and if it's already taken
        if form.username.data != current_user.username:
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Ce nom d\'utilisateur est déjà utilisé.', 'error')
                return render_template('dashboard/profile.html', form=form)
        
        # Update username
        current_user.username = form.username.data
        
        # Update password if provided
        if form.new_password.data:
            if not form.current_password.data:
                flash('Veuillez saisir votre mot de passe actuel pour le changer.', 'error')
                return render_template('dashboard/profile.html', form=form)
            
            if not current_user.check_password(form.current_password.data):
                flash('Mot de passe actuel incorrect.', 'error')
                return render_template('dashboard/profile.html', form=form)
            
            current_user.set_password(form.new_password.data)
        
        # Handle profile photo upload
        if form.profile_photo.data:
            file = form.profile_photo.data
            if file and allowed_file(file.filename, ['jpg', 'jpeg', 'png', 'gif']):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = f"{current_user.id}_{timestamp}{filename}"
                filepath = os.path.join(current_app.config['PROFILE_PHOTOS_FOLDER'], filename)
                file.save(filepath)
                
                # Remove old profile photo if it's not the default
                if current_user.profile_photo != 'default_avatar.png':
                    old_photo_path = os.path.join(current_app.config['PROFILE_PHOTOS_FOLDER'], current_user.profile_photo)
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                
                current_user.profile_photo = filename
        
        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('dashboard.profile'))
    
    return render_template('dashboard/profile.html', form=form)

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
