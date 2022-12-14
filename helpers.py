from models import Cupcake
from form import Cupcake_form
from env_keys.env_secrets import API_FORM_TOKEN


def new_cupcake(data):
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image']
    )
    return new_cupcake


def pre_fill_form(form, one_cupcake):
    form.flavor.data = one_cupcake.get('flavor')
    form.size.data = one_cupcake.get('size')
    form.rating.data = one_cupcake.get('rating')
    form.image.data = one_cupcake.get('image')
    return form


def validate_req(data):
    form = Cupcake_form()
    form.flavor.data = data['flavor'],
    form.size.data = data['size'],
    form.rating.data = data['rating'],
    form.image.data = data['image'],
    form.csrf_token.data = API_FORM_TOKEN
    if form.validate():
        return True
    else:
        return False
