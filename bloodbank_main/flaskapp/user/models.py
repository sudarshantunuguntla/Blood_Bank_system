from flask import jsonify,request,redirect,session
from flaskapp import db
# from passlib.hash import pbkdf2_sha256
import uuid
class User:
    def start_session(self,user):
        del user['password']
        session['logged_in']=True
        session['user']=user
        return jsonify(user),200
    
    def signup(self):
        print(request.form)
        user={
            "_id": uuid.uuid4().hex,
            "first_name":request.form.get("firstname"),
            "last_name":request.form.get("lastname"),
            "age":request.form.get("age"),
            "gender":request.form.get("gender"),
            "phone_number":request.form.get("phonenumber"),
            "email":request.form.get("email"),
            "password":request.form.get("password"),
            "bloodgroup":request.form.get("bloodgroup"),
            "address":"123 Main Street, City, Country",
            "total_donations":0,
            "total_received":0,
            "total_pending":0,
        }
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email address already in use" }), 400
        if db.users.insert_one(user):
            return self.start_session(user)
        return jsonify({ "error": "Signup failed" }), 400
    
    def signout(self):
        session.clear()
        return redirect('/')
    
    def login(self):
        user=db.users.find_one({
            "email":request.form.get('email')
        })

        print(user)
        print("loggedin")
        # print(pbkdf2_sha256.verify(request.form.get('password'), user['password']))
        # pbkdf2_sha256.verify(request.form.get('password'), user['password'])
        if user and user['password']==request.form.get('password'):
            return self.start_session(user)
        
        return jsonify({"error":"Invalid login credentials"}),401
    
    def editprof(self):
        # print("yehs yehs yehs yehs")
        new_data={
            'first_name':request.form.get('first_name'),
            'last_name':request.form.get('last_name'),
            'email':request.form.get('email'),
            'phone_number':request.form.get('phone_number'),
            'bloodgroup':request.form.get('blood_group'),
            'age':request.form.get('age'),
            'address':request.form.get('address')
        }
        print(new_data)
        existing_record=db.users.find_one({'email':session['user']['email']})
        if existing_record:
            existing_record.update(new_data)
            db.users.update_one({'email':session['user']['email']},{'$set':existing_record})
            session['user']=db.users.find_one({'email':session['user']['email']})
            print("record updation successfull")
        else:
            print("record with email {} not found ".format(session['user']['email']))
        return jsonify(existing_record),200
