from weatherApp import db


class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    city_name = db.Column(db.String(30), unique=True, index=True, nullable=False)

    def __repr__(self):
        return f'City {self.city_name}'
