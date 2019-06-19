from flask import Flask,render_template, request, session, Response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, validators
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

from flask_login import LoginManager,current_user, login_user


from database import connector
from model import entities
import json


db = connector.Manager()
engine = db.createEngine()
application = app = Flask(__name__)
application.secret_key = 'esta es una llave secreta'

@app.route('/')
def main():
    if 'logged_user' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/static/<content>')
def static_content(content):
    if content[0:4]=="crud" or content=="index.html":
        try:
            currentID = session['logged_user']
            db_session = db.getSession(engine)
            user = db_session.query(entities.Users).filter(entities.Users.id == currentID).one()
            if user.isAdmin:
                return render_template(content)
            else:
                raise Exception
        except Exception:
            session.clear()
            return render_template('login.html')
    else:
        return render_template(content)

# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - - D E V - E X T R E M E - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

@app.route('/crud/championship')
def crud_championship():
    try:
        currentID = session['logged_user']
        db_session = db.getSession(engine)
        user = db_session.query(entities.Users).filter(entities.Users.id == currentID).one()
        if user.isAdmin:
            return render_template('crud_championship.html')
        else:
            raise Exception
    except Exception:
        session.clear()
        return render_template('login.html')

@app.route('/crud/notification')
def crud_notification():
    try:
        currentID = session['logged_user']
        db_session = db.getSession(engine)
        user = db_session.query(entities.Users).filter(entities.Users.id == currentID).one()
        if user.isAdmin:
            return render_template('crud_notifications.html')
        else:
            raise Exception
    except Exception:
        session.clear()
        return render_template('login.html')

@app.route('/crud/payments')
def crud_payments():
    try:
        currentID = session['logged_user']
        db_session = db.getSession(engine)
        user = db_session.query(entities.Users).filter(entities.Users.id == currentID).one()
        if user.isAdmin:
            return render_template('crud_payments.html')
        else:
            raise Exception
    except Exception:
        session.clear()
        return render_template('login.html')

@app.route('/crud/sailing')
def crud_sailing():
    try:
        currentID = session['logged_user']
        db_session = db.getSession(engine)
        user = db_session.query(entities.Users).filter(entities.Users.id == currentID).one()
        if user.isAdmin:
            return render_template('crud_sailing.html')
        else:
            raise Exception
    except Exception:
        session.clear()
        return render_template('login.html')

@app.route('/crud/soccer')
def crud_soccer():
    try:
        currentID = session['logged_user']
        db_session = db.getSession(engine)
        user = db_session.query(entities.Users).filter(entities.Users.id == currentID).one()
        if user.isAdmin:
            return render_template('crud_soccer.html')
        else:
            raise Exception
    except Exception:
        session.clear()
        return render_template('login.html')

@app.route('/crud/users')
def crud_users():
    try:
        currentID = session['logged_user']
        db_session = db.getSession(engine)
        user = db_session.query(entities.Users).filter(entities.Users.id == currentID).one()
        if user.isAdmin:
            return render_template('crud_users.html')
        else:
            raise Exception
    except Exception:
        session.clear()
        return render_template('login.html')


# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - - - - - L O G I N - - - - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/authenticate', methods = ["POST"])
def authenticate():
    message = json.loads(request.data)
    email = message['email']
    password = message['password']
    #2. look in database
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.Users).filter(entities.Users.email == email).one()
        session['logged_user']=user.id
        if check_password_hash(user.password, password):
            message = {'message': 'Authorized'}
            return Response(message, status=200, mimetype='application/json')
        else:
            message = {'message': 'Unauthorized'}
            return Response(message, status=401, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

#current
@app.route('/current', methods = ['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.Users).filter(
        entities.Users.id==session['logged_user']).first()
    return Response(json.dumps(user,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')

# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - - - -  L O G O U T  - - - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return render_template('login.html')

# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - -  C R E A T E - U S E R - - - - -  - #
# - - - - - - - - - - - - - - - - - - - - - - - #

@app.route("/register")
def register():
    session.clear()
    return render_template('register.html')


@app.route('/createUser', methods = ["POST"])
def createUser():
    message = json.loads(request.data)
    hashed_password = generate_password_hash(message['password'], method='sha256')
    user = entities.Users(
    firstName=message['firstName'],
    lastName=message['lastName'],
    password=hashed_password,
    email=message['email']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    message = {'message': 'User Created'}
    return Response(message, status=200, mimetype='application/json')

# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - -  C R U D - U S E R S  - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Users)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users', methods = ['POST'])
def post_users():
    c =  json.loads(request.form['values'])
    hashed_password = generate_password_hash(c['password'], method='sha256')
    user = entities.Users(
        firstName =c['firstName'],
        lastName =c['lastName'],
        password = hashed_password,
        email =c['email']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/users', methods = ['PUT'])
def update_users():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.Users).filter(entities.Users.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.Users).filter(entities.Users.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "User Deleted"\


# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - -  O L D - M E T H O D  - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

@app.route("/loginold", methods=['GET', 'POST'])
def loginold():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)


"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(email=form.email.data, firstName=form.firstName.data, lastName=form.lastName.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('register.html', form=form)

"""

# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - C R U D - C H A M P I O N S H I P - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

#create championship
@app.route('/championship', methods = ['POST'])
def post_championship():
    c =  json.loads(request.form['values'])
    championship = entities.Championship(
        title =c['title'],
        maxCompetitors =c['maxCompetitors'],
        category =c['category'],
        price=c['price'],
        location =c['location'],
        description = c['description'],
        startDate = c['startDate'],
        endDate = c['endDate']
    )
    session = db.getSession(engine)
    session.add(championship)
    session.commit()
    return 'Created Championship'

#read championship
@app.route('/championship', methods = ['GET'])
def get_championship():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Championship)
    data = []
    for championship in dbResponse:
        data.append(championship)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

#update championship
@app.route('/championship', methods = ['PUT'])
def update_championship():
    session = db.getSession(engine)
    id = request.form['key']
    championship = session.query(entities.Championship).filter(entities.Championship.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(championship, key, c[key])
    session.add(championship)
    session.commit()
    return 'Updated Championship'

#delete championship
@app.route('/championship', methods = ['DELETE'])
def delete_championship():
    id = request.form['key']
    session = db.getSession(engine)
    championships = session.query(entities.Championship).filter(entities.Championship.id == id)
    for championship in championships:
        session.delete(championship)
    session.commit()
    return "Championship Deleted"

# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - - C R U D - S A I L I N G - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #
#create sailing
@app.route('/sailing', methods = ['POST'])
def post_sailing():
    c =  json.loads(request.form['values'])
    inscription = entities.InscriptionSailing(
        sailingNumber=c['sailingNumber'],
        category=c['category'],
        user_id=c['user_id'],
        championship_id=c['championship_id']
    )
    session = db.getSession(engine)
    session.add(inscription)
    session.commit()
    return 'Created Sailing Inscription'

#read sailing
@app.route('/sailing', methods = ['GET'])
def get_sailing():
    session = db.getSession(engine)
    dbResponse = session.query(entities.InscriptionSailing)
    data = []
    for inscription in dbResponse:
        data.append(inscription)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

#update sailing
@app.route('/sailing', methods = ['PUT'])
def update_sailing():
    session = db.getSession(engine)
    id = request.form['key']
    inscription = session.query(entities.InscriptionSailing).filter(entities.InscriptionSailing.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(inscription, key, c[key])
    session.add(inscription)
    session.commit()
    return 'Updated Sailing Inscription'

#delete sailing
@app.route('/sailing', methods = ['DELETE'])
def delete_sailing():
    id = request.form['key']
    session = db.getSession(engine)
    inscriptions = session.query(entities.InscriptionSailing).filter(entities.InscriptionSailing.id == id)
    for inscription in inscriptions:
        session.delete(inscription)
    session.commit()
    return "Deleted Sailing Inscription"



# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - - C R U D - S O C C E R - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

#create soccer
@app.route('/soccer', methods = ['POST'])
def post_soccer():
    j = json.loads(request.form['values'])
    inscription = entities.InscriptionSoccer(
        soccerTeam=j['soccerTeam'],
        category=j['category'],
        user_id=j['user_id'],
        championship_id=j['championship_id']
        )
    session = db.getSession(engine)
    session.add(inscription)
    session.commit()
    return 'Created Soccer Inscription'

#read soccer
@app.route('/soccer', methods = ['GET'])
def get_soccer():
    session = db.getSession(engine)
    dbResponse = session.query(entities.InscriptionSoccer)
    data = []
    for inscription in dbResponse:
        data.append(inscription)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

#update soccer
@app.route('/soccer', methods = ['PUT'])
def update_soccer():
    session = db.getSession(engine)
    id = request.form['key']
    inscription = session.query(entities.InscriptionSoccer).filter(entities.InscriptionSoccer.id == id).first()
    j = json.loads(request.form['values'])
    for key in j.keys():
        setattr(inscription, key, j[key])
    session.add(inscription)
    session.commit()
    return 'Updated Soccer Inscription'

#delete soccer
@app.route('/soccer', methods = ['DELETE'])
def delete_soccer():
    id = request.form['key']
    session = db.getSession(engine)
    inscriptions = session.query(entities.InscriptionSoccer).filter(entities.InscriptionSoccer.id == id)
    for inscription in inscriptions:
        session.delete(inscription)
    session.commit()
    return "Deleted Soccer Inscription"


# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - - LOAD INSCRIPTION DATA - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #
#Sailing
@app.route('/loadSailData', methods = ["POST"])
def load_sail():
    message = json.loads(request.data)
    try:
        data = entities.InscriptionSailing(
        sailingNumber=message['sailingNumber'],
        category=message['category'],
        user_id=message['user_id'],
        championship_id=message['championship_id']
        )
        session = db.getSession(engine)
        session.add(data)
        session.commit()
        message = {'message': 'User Created'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Error'}
        return Response(message, status=401, mimetype='application/json')


#Soccer
@app.route('/loadSoccerData', methods = ["POST"])
def load_soccer():
    message = json.loads(request.data)
    try:
        data = entities.InscriptionSoccer(
        soccerTeam=message['soccerTeam'],
        category=message['category'],
        user_id=message['user_id'],
        championship_id=message['championship_id']
        )
        session = db.getSession(engine)
        session.add(data)
        session.commit()
        message = {'message': 'User Created'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Error'}
        return Response(message, status=401, mimetype='application/json')

# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - N O T I F I C A T I O N S - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #

#create notification
@app.route('/notifications', methods = ['POST'])
def post_notification():
    c =  json.loads(request.form['values'])
    notification = entities.Notification(
        text=c['text'],
        type=c['type']
    )
    session = db.getSession(engine)
    session.add(notification)
    session.commit()
    return 'Created Notification'

#read notification
@app.route('/notifications', methods = ['GET'])
def get_notification():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Notification)
    data = []
    for notification in dbResponse:
        data.append(notification)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

#update notification
@app.route('/notifications', methods = ['PUT'])
def update_notification():
    session = db.getSession(engine)
    id = request.form['key']
    notification = session.query(entities.Notification).filter(entities.Notification.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(notification, key, c[key])
    session.add(notification)
    session.commit()
    return 'Updated Notification'


#delete notification
@app.route('/notifications', methods = ['DELETE'])
def delete_notification():
    id = request.form['key']
    session = db.getSession(engine)
    notifications = session.query(entities.Notification).filter(entities.Notification.id == id)
    for notification in notifications:
        session.delete(notification)
    session.commit()
    return "Deleted Notification"


# - - - - - - - - - - - - - - - - - - - - - - - #
# - - - - - - - - P A Y M E N T - - - - - - - - #
# - - - - - - - - - - - - - - - - - - - - - - - #
#create payment
@app.route('/paymentCULQUI', methods = ['POST'])
def post_payment_culqui():
    c = json.loads(request.data)
    payment = entities.Payment(
        paymentToken=c['paymentToken'],
        user_id=c['user_id'],
        championship_id=c['championship_id']
    )
    session = db.getSession(engine)
    session.add(payment)
    session.commit()
    message = {'message': 'Authorized'}
    return Response(message, status=200, mimetype='application/json')


#create payment
@app.route('/payments', methods = ['POST'])
def post_payment():
    c =  json.loads(request.form['values'])
    payment = entities.Payment(
        paymentToken=c['paymentToken'],
        user_id=c['user_id'],
        championship_id=c['championship_id']
    )
    session = db.getSession(engine)
    session.add(payment)
    session.commit()
    return 'Created Payment'

#read payment
@app.route('/payments', methods = ['GET'])
def get_payment():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Payment)
    data = []
    for payment in dbResponse:
        data.append(payment)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

#update payment
@app.route('/payments', methods = ['PUT'])
def update_payment():
    session = db.getSession(engine)
    id = request.form['key']
    payment = session.query(entities.Payment).filter(entities.Payment.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(payment, key, c[key])
    session.add(payment)
    session.commit()
    return 'Updated Payment'

#delete payment
@app.route('/payments', methods = ['DELETE'])
def delete_payment():
    id = request.form['key']
    session = db.getSession(engine)
    payments = session.query(entities.Payment).filter(entities.Payment.id == id)
    for payment in payments:
        session.delete(payment)
    session.commit()
    return "Deleted Payment"

@app.route("/inscripcion")
def inscripcion():
    return render_template('form1.html')


if __name__ == '__main__':
    application.debug = True
    application.run(host='127.0.0.1', debug=True)
