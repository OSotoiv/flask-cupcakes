from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, URLField
from wtforms.validators import InputRequired, Optional, NumberRange, ValidationError, Length


class Cupcake_form(FlaskForm):

    flavor = StringField('Flavor', validators=[
                         InputRequired()])
    size = StringField('Size', validators=[InputRequired()])
    rating = FloatField('Rating', validators=[InputRequired()])
    image = URLField('Image', validators=[InputRequired()],
                     default='https://tinyurl.com/demo-cupcake')
