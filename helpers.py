from models import Cupcake


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
