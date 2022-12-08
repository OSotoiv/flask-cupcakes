"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, session, jsonify
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from helpers import new_cupcake, pre_fill_form
from form import Cupcake_form

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'thehouseisyellow'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
connect_db(app)


@app.route('/', methods=["GET", "POST"])
def show_all_cupcakes_and_form():
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
        all_cupcakes = Cupcake.query.all()
        return render_template('home.html', form=form, all_cupcakes=all_cupcakes)


@app.route('/cupcake/<int:id>', methods=["GET", "PATCH"])
def show_cupcake_by_id(id):
    """get a single cupcake by id and show its edit form"""
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
        try:
            res = requests.get(f'http://127.0.0.1:5000/api/cupcakes/{id}')
            one_cupcake = res.json()['cupcake']
            form = pre_fill_form(form, one_cupcake)
            return render_template('show_cupcake.html', cupcake=one_cupcake, form=form)
        except Exception:
            return 404


@app.route('/delete/<int:id>')
def delete_cupcake_by_id(id):
    res = requests.delete(f'http://127.0.0.1:5000/api/cupcakes/{id}')
    flash('cupcake deleted')
    return redirect('/')
# _____________________________________________________________________________________________________________________________


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
    cupcake = new_cupcake(request.json)
    db.session.add(cupcake)
    db.session.commit()
    serialized_cupcake = cupcake.serialize()
    return jsonify(cupcake=serialized_cupcake)


@ app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    single_cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(single_cupcake)
    db.session.commit()
    return jsonify(message='deleted')


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def patch_cupcake(cupcake_id):
    single_cupcake = Cupcake.query.get_or_404(cupcake_id)
    single_cupcake.flavor = request.json.get('flavor', single_cupcake.flavor)
    single_cupcake.size = request.json.get('size', single_cupcake.size)
    single_cupcake.rating = request.json.get('rating', single_cupcake.rating)
    single_cupcake.image = request.json.get('image', single_cupcake.image)
    db.session.commit()
    return jsonify(cupcake=single_cupcake.serialize())
