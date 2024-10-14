# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy.orm import Session

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    session = Session(db.engine)
    earthquake = session.get(Earthquake, id)
    if earthquake:
        return jsonify({
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }), 200
    else:
        return jsonify({'message': f'Earthquake {id} not found.'}), 404

# View to get earthquakes matching a minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        'count': len(earthquakes),
        'quakes': [
            {
                'id': quake.id,
                'location': quake.location,
                'magnitude': quake.magnitude,
                'year': quake.year
            } for quake in earthquakes
        ]
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
