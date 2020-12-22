from flask_sqlalchemy import SQLAlchemy, sqlalchemy

db = SQLAlchemy()

database_path = 'postgres://postgres:root@localhost:5432/castingagency'

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:root@localhost:5432/castingagency'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Actor(db.Model):
    """A DB Model that defines an Actor"""

    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer)
    gender = db.Column(db.String())

    def __repr__(self):
        return '<Actor {} {}>'.format(self.name, self.age, self.gender)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    """A DB Model that defines a Movie"""

    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    release_date = db.Column(db.String())

    def __repr__(self):
        return '<Movie {} {}>'.format(self.title, self.release_date)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
