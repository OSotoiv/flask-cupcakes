"""Models for Cupcake app."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    __tablename__ = 'cupcakes'

    def __repr__(self):
        return f'<Cupcake: id={self.id}, flavor={self.flavor}, size={self.size}, rating={self.rating}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(), nullable=False,
                      default='https://tinyurl.com/demo-cupcake')

    def serialize(self):
        """instance method, serializes attributes for API"""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }
