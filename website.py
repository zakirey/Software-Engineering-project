import smtplib
import csv
from flask import Flask, url_for, render_template, request, redirect, flash
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_login import UserMixin
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required, current_user, logout_user
from SecretWinsWebsite.AllBestBetsScrapper import ABBAPI, scope

global select
select = "0"

# Website
secret_site = Flask(__name__)
secret_site.config['SECRET_KEY'] = 'super secret key'
secret_site.config['SESSION_TYPE'] = 'filesystem'

# Database
engine = create_engine(r'sqlite:///D:\Document\Python\Secret-Wins\Database\User.db', echo=True)
Base = declarative_base(engine)

# db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(secret_site)


all_best_bets = scope()


@login_manager.user_loader
def load_user(user_id):
    session = loadSession()
    log = session.query(Customer).get(int(user_id))
    session.remove()
    return log


class Customer(UserMixin, Base):
    """"""
    __tablename__ = 'Customer'
    __table_args__ = {'autoload': True}

    def get_id(self):
        return self.idCustomer


# ----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata
    Session = scoped_session(sessionmaker(bind=engine))
    return Session


# https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4Pv1QsDO9aVqx9gJsqlqxLgUxL9Hv7jl_rzmRifLqSGthiQG9Q05_EUIiq8TKkqc5uXOPsnEKALGQjTWTGAt9avxLwP0A
def send_email(email, message="Your account was successfully registered!"):
    config = {}
    srv = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    srv.ehlo()
    with open('config.csv', 'r') as con:
        data_reader = csv.reader(con)
        for row in data_reader:
            l_data = row
            config[l_data[0]] = l_data[1]
    srv.login(config["username"], config["password"])
    to = email
    srv.sendmail(config["username"], to, message)
    srv.quit()


@secret_site.route('/')
def index():
    return render_template('index.html')


@secret_site.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session = loadSession()
        customer = session.query(Customer).filter_by(Email=request.form['email']).first()
        if customer is not None:
            if customer.Password == request.form['password']:
                session.remove()
                try:
                    remember = True if request.form['remember'] else False

                    login_user(customer, remember=remember)
                    return redirect(url_for('profile'))
                except KeyError:
                    login_user(customer)
                    return redirect(url_for('profile'))
            else:
                error = 'Invalid Password'
                session.remove()
                return render_template("login.html", error=error)
        else:
            error = 'Invalid Email'
            session.remove()
            return render_template("login.html", error=error)
    return render_template("login.html")


@secret_site.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        session = loadSession()
        customer = session.query(Customer).filter_by(
            Email=request.form['email']).all()

        if len(customer) > 0:
            error = 'Given Email was already registered'
            session.remove()
            return render_template("register.html", error=error)
        else:
            new_id = session.query(Customer).all()[-1].idCustomer
            new_customer = Customer(idCustomer=new_id + 1, Username=username, Email=email, Password=password)
            session.add(new_customer)
            session.commit()
            send_email(str(new_customer.Email))
            session.remove()
        return redirect("/login")

    return render_template("register.html")


@secret_site.route('/retrieve_password', methods=["GET", "POST"])
def retrieve_password():
    if request.method == "POST":
        session = loadSession()
        customer = session.query(Customer).filter_by(Email=request.form['email']).first()
        if customer is not None:
            session.remove()
            send_email(str(customer.Email), "Here is your password " + str(customer.Password) + " Enjoy")
            return redirect("/login")
        else:
            error = 'Invalid Email'
            session.remove()
            return render_template("retrieve_password.html", error=error)
    return render_template("retrieve_password.html")


@secret_site.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@secret_site.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.Username)


@secret_site.route('/arbitrageinfo')
def arbitrageinfo():
    return render_template('arbitrageinfo.html')


@secret_site.route('/arbitragelogin', methods=["GET", "POST"])
@login_required
def arbitragelogin():
    global select
    if request.method == "POST":
        select = request.form["select"]
        print(select, type(select))
        data = ABBAPI(all_best_bets, select)
        return render_template('arbitragelogin.html', arbs=data)
    else:
        data = ABBAPI(all_best_bets, select)
        return render_template('arbitragelogin.html', arbs=data)


@secret_site.route('/subscriptioninfo')
def subscriptioninfo():
    return render_template('subscriptioninfo.html')


@secret_site.route('/subscriptionlogin')
@login_required
def subscriptionlogin():
    return render_template('subscriptionlogin.html')


@secret_site.route('/faq')
def faq():
    return render_template('faq.html')


@secret_site.route('/faqlogin')
@login_required
def faqlogin():
    return render_template('faqlogin.html')


@secret_site.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404


@secret_site.errorhandler(403)
def page_not_found(e):
    return render_template('error.html'), 403


@secret_site.errorhandler(410)
def page_not_found(e):
    return render_template('error.html'), 403


@secret_site.errorhandler(500)
def page_not_found(e):
    return render_template('error.html'), 500


@secret_site.route('/payment')
@login_required
def payment():
    return render_template('payment.html')


if __name__ == "__main__":
    session = loadSession()

    secret_site.run()
