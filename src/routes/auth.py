from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from src.database.helpeDB import create_user, get_user_by_email, get_user_by_id
import bcrypt

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email y contraseña son requeridos.', 'error')
            return render_template('login.html')

        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['PASSWORD_HASH'].encode('utf-8')):
            session['user_id'] = user['ID']
            session['user_name'] = user['NAME']
            return redirect(url_for('main.home'))
        else:
            flash('Email o contraseña incorrectos.', 'error')

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not email or not password:
            flash('Todos los campos son requeridos.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('register.html')

        existing_user = get_user_by_email(email)
        if existing_user:
            flash('Ya existe una cuenta con ese email.', 'error')
            return render_template('register.html')

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = create_user(name, email, password_hash)

        if user:
            session['user_id'] = user['ID']
            session['user_name'] = user['NAME']
            flash('Cuenta creada exitosamente.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Error al crear la cuenta. Intenta de nuevo.', 'error')

    return render_template('register.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
