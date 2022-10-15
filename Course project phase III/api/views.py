from flask import jsonify, request
from .models import Dashboard, User, Product
from api import app, db

session= {}

@app.route('/login-ajax', methods=['POST'])
def login_user():
    global fernet
    req_json = request.json
    print(req_json)
    email = req_json['email']
    password = req_json['password']
    user= User.query.filter_by(email=email).first()
    if user is not None:
        if user.password == password:
            session["logged_in"] = True
            session["username"]= user.username
            session["email"]=user.email
            print(session)
            if user.username=="admin":
                return "admin"
            else:
                return "user"
    return "No User Found. Try Again!!"


@app.route('/logout-ajax', methods=['POST'])
def logout_user():
    global session
    session = {}
    return 'success'

@app.route('/register-ajax', methods=['POST'])
def register_user():
    global fernet
    req_json = request.json
    print(req_json)
    try:
        username = req_json['username']
        firstname = req_json['fname']
        lastname = req_json['lname']
        email = req_json['email']
        password = req_json['password']
        values = User(email=email, username=username, fname=firstname,
                        lname=lastname, password=password)
        db.session.add(values)
        db.session.commit()
    except Exception as e:
        return str(e)
        
    return "success"

@app.route('/get-profile-ajax', methods=['GET'])
def get_profile():
    if session.get("email") is not None:
        email = session.get("email")
        print("Email: ",email)
        user= User.query.filter_by(email=email).first()

        response = jsonify({'name': user.fname + " " + user.lname, "email": session['email'], "username":session['username']})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        return "Failed"

@app.route('/add-product-ajax', methods=['POST'])
def add_product():
    if session.get("email") is not None:
        req_json = request.json
        print(req_json)
        try:
            product_name = req_json['product_name']
            category_name = req_json['category_name']
            quantity = req_json['quantity']
            if int(quantity) < 1:
                return "quantity_error"
            product_data = Product.query.filter_by(product_name=product_name).first()
            if product_data is not None:
                    product_data.quantity += int(quantity)
                    db.session.commit()
                    return "updated"
            else:
                values = Product(product_name=product_name, category_name=category_name, quantity=quantity)
                db.session.add(values)
                db.session.commit()
                return "success"
        except Exception as e:
            return str(e)
    else:
        return "Failed"


@app.route('/get-admin-dashboard-ajax', methods=['GET'])
def get_admin_dashboard():
    datas = Dashboard.query.all()
    data_list = []
    for d in datas:
        data_list.append([d.id, d.product_id, d.email, d.product_name, d.category_name, d.status])
    print(data_list)
    user = len(User.query.all())
    products = len(Product.query.all())
    issued_products = Dashboard.query.filter_by(status="Approved").count()
    requested_products = Dashboard.query.filter_by(status="Requested").count()
    
    response = jsonify({"data_list": data_list,"username":session['username'], "total_user": user, "total_products": products, "total_issued_products": issued_products, "requested_products" :requested_products})
    print({"data_list": data_list,"username":session['username'], "total_user": user, "total_products": products, "total_issued_products": issued_products, "requested_products" :requested_products})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

