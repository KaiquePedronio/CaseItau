
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


class Residencias(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    host_id = db.Column(db.Integer, nullable=False)
    host_name = db.Column(db.String(50), nullable=False)
    neighbourhood = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.String(50), nullable=True)
    longitude = db.Column(db.String(50), nullable=True)
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    minimum_nights = db.Column(db.Integer, nullable=False)
    number_of_reviews = db.Column(db.Integer, nullable=True)
    last_review = db.Column(db.Date, nullable=True)
    reviews_per_month = db.Column(db.Float, nullable=True)
    calculated_host_listings_count = db.Column(db.Integer, nullable=True)
    availability_365 = db.Column(db.Integer, nullable=True)
    neighbourhood_group = db.Column(db.String(50), nullable=False)


class MediaPreco(db.Model):
    neighbourhood_group = db.Column(db.String(50), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)