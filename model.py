"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from correlation import pearson

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def similarity(self, other):
        """Return Pearson rating for user compared to other user."""
        u_ratings = {}
        paired_ratings = []

        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append((u_r.score, r.score))

        if paired_ratings:
            return pearson(paired_ratings)
        else:
            return 0.0

    def __repr__(self):
        """Provide helpful representation when printed!"""
        return f"<User user_id={self.user_id} email={self.email}>"


class Rating(db.Model):
    """User/Movie ratings on ratings website"""

    __tablename__="ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, 
                         db.ForeignKey('movies.movie_id'), 
                         nullable=False)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    score = db.Column(db.Integer, nullable=False)

    user = db.relationship("User",
                            backref=db.backref("ratings", order_by=rating_id))

    movie = db.relationship("Movie", 
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):

        return f"<Rating_id={self.rating_id} score={self.score}>"

class Movie(db.Model):
    """Movie on ratings website"""

    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_title = db.Column(db.String(100), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):

        return f"<Movie_id={self.movie_id} movie_title={self.movie_title}>"

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
