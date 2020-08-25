from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///forecastcities.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.errorhandler(404)



class Forecast(db.Model):
    city = db.Column(db.TEXT(20), primary_key=True)
    temperature = db.Column(db.INTEGER, nullable=False)
    start_date = db.Column(db.DATE, nullable=False)
    stop_date = db.Column(db.DATE, nullable=False)
    vin = db.Column(db.INTEGER, nullable=False)


    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {"city": self.city,
                "temperature": self.temperature,
                "start_date": self.start_date,
                "stop_date": self.stop_date,
                "vin": self.vin}
    db.create_all()

@app.route('/dev/', methods=['GET'])
def index():
    return jsonify({'forecast': list(map(lambda dev: dev.serialize(), Forecast.query.all()))})


@app.route('/dev/<int:vin>/')
def get_dev(vin):
    return jsonify({'forecast': Forecast.query.get(id).serialize()})


@app.route('/dev/', methods=['POST'])
def create_dev():
    if not request.json or not 'name' in request.json:
        abort(400)
    dev = Forecast(request.json['name'])
    db.session.add(dev)
    db.session.commit()
    return jsonify({'forecast': dev.serialize()}), 201


@app.route('/dev/<int:vin>/', methods=['DELETE'])
def delete_dev(vin):
    db.session.delete(Forecast.query.get(vin))
    db.session.commit()
    return jsonify({'result': True})


@app.route('/dev/<int:vin>/', methods=['PUT'])
def update_dev(vin):
    dev = Forecast.query.get(vin)
    dev.name = request.json.get('name', dev.name)
    db.session.commit()
    return jsonify({'dev': dev.serialize()})


if __name__ == "__main__":
    app.run(debug=True)