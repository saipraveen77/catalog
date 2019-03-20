from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, SocCompany, SocName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///chipset.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Chips"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
tbs_cat = session.query(SocCompany).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    tbs_cat = session.query(SocCompany).all()
    tbes = session.query(SocName).all()
    return render_template('login.html',
                           STATE=state, tbs_cat=tbs_cat, tbes=tbes)
    # return render_template('myhome.html', STATE=state
    # tbs_cat=tbs_cat,tbes=tbes)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'],
                 email=login_session['email'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# Home


@app.route('/')
@app.route('/home')
def home():
    tbs_cat = session.query(SocCompany).all()
    return render_template('myhome.html', tbs_cat=tbs_cat)

# SocHub for admins


@app.route('/SocHub')
def SocHub():
    try:
        if login_session['username']:
            name = login_session['username']
            tbs_cat = session.query(SocCompany).all()
            tbs = session.query(SocCompany).all()
            tbes = session.query(SocName).all()
            return render_template('myhome.html', tbs_cat=tbs_cat,
                                   tbs=tbs, tbes=tbes, uname=name)
    except:
        return redirect(url_for('SocHub'))

# Showing items


@app.route('/SocHub/<int:tbid>/Allsocs')
def showChipsets(tbid):
    tbs_cat = session.query(SocCompany).all()
    tbs = session.query(SocCompany).filter_by(id=tbid).one()
    tbes = session.query(SocName).filter_by(soccompanyid=tbid).all()
    try:
        if login_session['username']:
            return render_template('showChipsets.html', tbs_cat=tbs_cat,
                                   tbs=tbs, tbes=tbes,
                                   uname=login_session['username'])
    except:
        return render_template('showChipsets.html',
                               tbs_cat=tbs_cat, tbs=tbs, tbes=tbes)

# Add New item


@app.route('/SocHub/addSocCompanyName', methods=['POST', 'GET'])
def addSocCompany():
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        soccompany = SocCompany(name=request.form['name'],
                                user_id=login_session['user_id'])
        session.add(soccompany)
        session.commit()
        return redirect(url_for('SocHub'))
    else:
        return render_template('addSocCompany.html', tbs_cat=tbs_cat)

# Edit Chipset Company


@app.route('/SocHub/<int:tbid>/edit', methods=['POST', 'GET'])
def editSocCompany(tbid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    editSocCompany = session.query(SocCompany).filter_by(id=tbid).one()
    creator = getUserInfo(editSocCompany.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this SocName."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('SocHub'))
    if request.method == "POST":
        if request.form['name']:
            editSocCompany.name = request.form['name']
        session.add(editSocCompany)
        session.commit()
        flash("editSocCompany Edited Successfully")
        return redirect(url_for('SocHub'))
    else:
        # tbs_cat is global variable we can them in entire application
        return render_template('editSocCompany.html',
                               tb=editSocCompany, tbs_cat=tbs_cat)

# Delete Chipset Company


@app.route('/SocHub/<int:tbid>/delete', methods=['POST', 'GET'])
def deleteSocCompany(tbid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    tb = session.query(SocCompany).filter_by(id=tbid).one()
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Soc name."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('SocHub'))
    if request.method == "POST":
        session.delete(tb)
        session.commit()
        flash("SocCompanyName Deleted Successfully")
        return redirect(url_for('SocHub'))
    else:
        return render_template('deleteSocCompany.html', tb=tb, tbs_cat=tbs_cat)

# Add New Chipset Name Details


@app.route('/SocHub/addSocCompany/addChipsetDetails/<string:tbname>/add',
           methods=['GET', 'POST'])
def addChipsetDetails(tbname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    tbs = session.query(SocCompany).filter_by(name=tbname).one()
    # See if the logged in user is not the owner of byke
    creator = getUserInfo(tbs.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new chipset edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showChipsets', tbid=tbs.id))
    if request.method == 'POST':
        name = request.form['name']
        build = request.form['build']
        cores = request.form['cores']
        frequency = request.form['frequency']
        chipsetdetails = SocName(name=name, build=build,
                                 cores=cores,
                                 frequency=frequency,
                                 date=datetime.datetime.now(),
                                 soccompanyid=tbs.id,
                                 user_id=login_session['user_id'])
        session.add(chipsetdetails)
        session.commit()
        return redirect(url_for('showChipsets', tbid=tbs.id))
    else:
        return render_template('addChipsetDetails.html',
                               tbname=tbs.name, tbs_cat=tbs_cat)

#  Edit Chipset deatils


@app.route('/SocHub/<int:tbid>/<string:tbename>/edit',
           methods=['GET', 'POST'])
def editChipset(tbid, tbename):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    tb = session.query(SocCompany).filter_by(id=tbid).one()
    chipsetdetails = session.query(SocName).filter_by(name=tbename).one()
    # See if the logged in user is not the owner of byke
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this chipset edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showChipsets', tbid=tb.id))
    # POST methods
    if request.method == 'POST':
        chipsetdetails.name = request.form['name']
        chipsetdetails.build = request.form['build']
        chipsetdetails.cores = request.form['cores']
        chipsetdetails.frequency = request.form['frequency']
        chipsetdetails.date = datetime.datetime.now()
        session.add(chipsetdetails)
        session.commit()
        flash("chipset Edited Successfully")
        return redirect(url_for('showChipsets', tbid=tbid))
    else:
        return render_template('editChipset.html',
                               tbid=tbid, chipsetdetails=chipsetdetails,
                               tbs_cat=tbs_cat)

# Delete Chipset


@app.route('/SocHub/<int:tbid>/<string:tbename>/delete',
           methods=['GET', 'POST'])
def deleteChipset(tbid, tbename):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    tb = session.query(SocName).filter_by(id=tbid).one()
    chipsetdetails = session.query(SocName).filter_by(name=tbename).one()
    # See if the logged in user is not the owner of byke
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showChipsets', tbid=tb.id))
    if request.method == "POST":
        session.delete(chipsetdetails)
        session.commit()
        flash("Deleted chipset item Successfully")
        return redirect(url_for('showChipsets', tbid=tbid))
    else:
        return render_template('deleteChipset.html',
                               tbid=tbid, chipsetdetails=chipsetdetails,
                               tbs_cat=tbs_cat)


# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type':
                           'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully'
                                            'disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Json


@app.route('/SocHub/JSON')
def allChipsetsJSON():
    soccompanies = session.query(SocCompany).all()
    category_dict = [c.serialize for c in soccompanies]
    for c in range(len(category_dict)):
        chipsetnames = [i.serialize for i in session.query(
                 SocName).filter_by(soccompanyid=category_dict[c]["id"]).all()]
        if chipsetnames:
            category_dict[c]["chipsets"] = chipsetnames
    return jsonify(SocCompany=category_dict)


@app.route('/SocHub/socCompany/JSON')
def categoriesJSON():
    chipsets = session.query(SocCompany).all()
    return jsonify(socCompany=[c.serialize for c in chipsets])


@app.route('/SocHub/chipsets/JSON')
def itemsJSON():
    items = session.query(SocName).all()
    return jsonify(chipsets=[i.serialize for i in items])


@app.route('/SocHub/<path:soccompany>/chipsets/JSON')
def categoryitemsJSON(soccompany):
    socCompany = session.query(SocCompany).filter_by(name=soccompany).one()
    chipsets = session.query(SocName).filter_by(soccompany=socCompany).all()
    return jsonify(socCompany=[i.serialize for i in chipsets])


@app.route('/SocHub/<path:soccompany>/<path:chipset_name>/JSON')
def ItemJSON(soccompany, chipset_name):
    socCompany = session.query(SocCompany).filter_by(name=soccompany).one()
    chipsetName = session.query(SocName).filter_by(
           name=chipset_name, soccompany=socCompany).one()
    return jsonify(chipsetName=[chipsetName.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
