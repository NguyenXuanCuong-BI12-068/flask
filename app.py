# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask.sign_in import Sign_in
from flask.sign_up import Sign_up
from flask.dashboard import Dashboard
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

 
# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/Account'  
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, customer_id, file):
        self.customer_id = customer_id
        self.file = file

@app.route('/login', methods=['GET', 'POST'])
def login():
    return Sign_in()

@app.route('/dashboard/<username>')
def dashboard(username):
    return Dashboard(username)



@app.route('/dashboard<username>', methods=['GET'])
def get_files():
    files = File.query.all()
    file_list = []
    for file in files:
        file_data = {
            'id' : file.id,
            'customer_id': file.customer_id,
            'file': file.file
        }
        file_list.append(file_data)
    return jsonify(file_list)

@app.route('/dashboard/<username>', methods=['POST'])
def create_files():
    data = request.get_json()
    customer_id = data.get('customer_id')
    file = data.get('file')
    file_data = File(customer_id=customer_id,file=file)
    db.session.add(file_data)
    db.session.commit()
    return jsonify({'message': 'File created successfully'})

@app.route('/dashboard/<username>/<int:file_id>', methods=['PUT'])
def update_file(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({'error': 'File not found'})
    data = request.get_json()
    file.customer_id = data.get('customer_id')
    file.file = data.get('file')
    db.session.commit()
    return jsonify({'message': 'File updated successfullly'})

@app.route('/dashboard/<username>/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({'error': 'File not found'})
    
    db.session.delete(file)
    db.session.commit()
    return jsonify({'message': 'File deleted successfullly'})

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    return Sign_up()




# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug = True, port=8080)