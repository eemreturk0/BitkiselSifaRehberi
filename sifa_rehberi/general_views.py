from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required,current_user

from sifa_rehberi import db, app
from model import User, Bitki, Hastalik, Recete


# Hastalik ekleme
@app.route('/admin/hastalik_ekle', methods=['GET', 'POST'])
@login_required
def hastalik_ekle():
    if request.method == 'POST':
        ad = request.form['ad']
        new_hastalik = Hastalik(ad=ad)
        db.session.add(new_hastalik)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('hastalik_ekle.html')


# Recete ekleme
@app.route('/admin/recete_ekle', methods=['GET', 'POST'])
@login_required
def recete_ekle():
    bitkiler = Bitki.query.all()
    hastaliklar = Hastalik.query.all()

    if request.method == 'POST':
        ad = request.form['ad']
        icerik = request.form['icerik']
        bitki_id = request.form['bitki']
        hastalik_id = request.form['hastalik']

        # Bitki ve hastalık nesnelerini veritabanından çekin
        secili_bitki = Bitki.query.get(bitki_id)
        secili_hastalik = Hastalik.query.get(hastalik_id)

        new_recete = Recete(ad=ad, icerik=icerik, bitki=secili_bitki, hastalik=secili_hastalik)
        db.session.add(new_recete)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('recete_ekle.html', bitkiler=bitkiler, hastaliklar=hastaliklar)


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect("/login")
    elif current_user.has_role("admin"):
        return redirect("/admin")
    else:
        return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template("index.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)  # Kullanıcıyı oturum açmış olarak işaretle
            return redirect(url_for('index'))
        else:
            return "Kullanıcı adı veya şifre hatalı."

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


