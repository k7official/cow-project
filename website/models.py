from . import db


class Cow(db.Model):
    animal_id = db.Column(db.Integer(), primary_key=True)
    ear_tag = db.Column(db.String(100), unique=True, nullable=False)
    animal_type = db.Column(db.String(250), nullable=False)
    breed = db.Column(db.String(250), nullable=False)
    color = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Cow {self.animal_id}>'


class Img(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    pic = db.Column(db.LargeBinary)

    def __repr__(self):
        return f'<Img {self.title}>'