"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, session, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from helpers import new_cupcake, pre_fill_form, validate_req
from form import Cupcake_form
from env_keys import env_secrets

app = Flask(__name__)
# app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = env_secrets.APP_CONFIG_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
connect_db(app)

# These routes are for the UI


@app.route('/', methods=["GET", "POST"])
def show_all_cupcakes_and_form():
    """GET and show all of the cupcakes, POST new cupcakes to the DB and Return JSON to the client of the new cupcake"""
    form = Cupcake_form()
    if form.validate_on_submit():
        # res should be json from the api
        res = requests.post('http://127.0.0.1:5000/api/cupcakes',
                            json={
                                'flavor': form.flavor.data,
                                'size': form.size.data,
                                'rating': form.rating.data,
                                'image': form.image.data
                            })
        return (res.json(), 201)
    else:
        # cheeting here a bit because im accessing the DB without makeing a request
        # to the API.
        all_cupcakes = Cupcake.query.all()
        return render_template('home.html', form=form, all_cupcakes=all_cupcakes)


@app.route('/cupcake/<int:id>', methods=["GET", "PATCH"])
def show_cupcake_by_id(id):
    """get a single cupcake by id and show its edit form"""
    """send edit form as a PATCH to API as JSON data"""
    form = Cupcake_form()
    if form.validate_on_submit():
        res = requests.patch(f'http://127.0.0.1:5000/api/cupcakes/{id}',
                             json={
                                 'flavor': form.flavor.data,
                                 'size': form.size.data,
                                 'rating': form.rating.data,
                                 'image': form.image.data
                             })
        return (res.json(), 201)
    else:
        res = requests.get(f'http://127.0.0.1:5000/api/cupcakes/{id}')
        if res.status_code == 404:
            flash(res.reason)
            return redirect('/')
        else:
            one_cupcake = res.json()['cupcake']
            form = pre_fill_form(form, one_cupcake)
            return render_template('show_cupcake.html', cupcake=one_cupcake, form=form)


# if i use axios to reach this route then how do you refresh the page once you delete the cupcake?
# maybe js should triggera page refress appon 200 status returned....?
@app.route('/delete/<int:id>')
def delete_cupcake_by_id(id):
    """route to request API delete cupcake by ID"""
    res = requests.delete(f'http://127.0.0.1:5000/api/cupcakes/{id}')
    if res.status_code == 404:
        flash(res.reason)
        return redirect('/')
    else:
        # flash(res.json()['message'])
        return redirect('/')
# _____________________________________________________________________________________________________________________________


# These routes are for the API.
@app.route('/api/cupcakes')
def get_all_cupcakes():
    """responds with json of all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@ app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_by_id(cupcake_id):
    """returns json if single cupcake by id"""
    single_cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=single_cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """post new cupcake to DB and returns json of new cupcake data"""
    # if validate_req(request.json):
    cupcake = new_cupcake(request.json)
    db.session.add(cupcake)
    db.session.commit()
    serialized_cupcake = cupcake.serialize()
    return (jsonify(cupcake=serialized_cupcake), 201)
    # else:
    #     return (jsonify(message='Invalid Form Data'), 400)


@ app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """delete single cupcake from DB"""
    single_cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(single_cupcake)
    db.session.commit()
    return jsonify(message='deleted')


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def patch_cupcake(cupcake_id):
    """Updates existing cupcake and return json of Updated cupcake data"""
    single_cupcake = Cupcake.query.get_or_404(cupcake_id)
    single_cupcake.flavor = request.json.get('flavor', single_cupcake.flavor)
    single_cupcake.size = request.json.get('size', single_cupcake.size)
    single_cupcake.rating = request.json.get('rating', single_cupcake.rating)
    single_cupcake.image = request.json.get('image', single_cupcake.image)
    db.session.commit()
    return (jsonify(cupcake=single_cupcake.serialize()), 201)
