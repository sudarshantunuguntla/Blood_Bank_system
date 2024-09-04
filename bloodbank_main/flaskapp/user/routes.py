from flaskapp import app,login_required
from flaskapp.user.models import User
from flask import render_template
from flask import request
from flask import jsonify,request,redirect,session,url_for
from flaskapp import mydb
from flaskapp import db,mydb2,mydb3
from datetime import datetime

@app.route('/user/login',methods=['POST'])
def login():
    return User().login()

@app.route('/user/signout')
def signout():
    return User().signout()

@app.route('/user/signup',methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/editprof',methods=['POST'])
def editprof():
    return User().editprof()

@app.route('/aboutus')
def func():
    return render_template('bbs_aboutus.html')

@app.route('/bloodgroups')
def bloodgroups():
    return render_template('bbs_bloodgroups.html')

@app.route('/registration')
def registration():
    return render_template('bbs_registration.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('user_dashboard.html')

@app.route('/profile')
def profile():
    return render_template('user_profile.html')

@app.route('/editprofile')
def editprofile():
    return render_template('user_editprofile.html')

@app.route('/request_hospital')
def request_hospital():
    return render_template('bbs_user12.html')

@app.route('/tempest_hosp')
def tempest_hosp():
    hospitals_data = list(mydb.hospinfo.find())
    for index, record in enumerate(hospitals_data, start=1):
        record['id'] = index
    return render_template('bbs_user_temp12.html', hospitals=hospitals_data)

@app.route('/hospital/<int:hospital_id>')
def hospital_details(hospital_id):
    hospitals_data = list(mydb.hospinfo.find())
    for index, record in enumerate(hospitals_data, start=1):
        record['id'] = index
    hospital = next((h for h in hospitals_data if h['id'] == hospital_id), None)
    if hospital:
        return render_template('hospital_details.html', hospital=hospital)
    else:
        return 'Hospital not found', 404
    
@app.route('/submit_request', methods=['POST'])
def submit_request():
    # Handle form submission here
    hospital_id = request.form.get('hospital_id')
    blood_type = request.form.get('blood_type')
    units = int(request.form.get('units'))
    bloodgroup=request.form.get('bloodgroup')
    name1=request.form.get("hospital_name")
    reason=request.form.get("reason")
    print(hospital_id)
    print(blood_type)
    print(units)
    print(bloodgroup)
    

    mydb.hospinfo.update_one(
        {"name": name1},  # Assuming "_id" is the identifier field
        {
            "$inc": {
                f"blood_types.{blood_type}": -units,
                f"blood_types.{bloodgroup}": units
            }
        }
    )
    existing_record=db.users.find_one({'email':session['user']['email']})
    if existing_record:
        db.users.update_one({'email':session['user']['email']}, {"$inc": {"total_received": 1}})
        print("record updation successfull")
    session['user']=db.users.find_one({'email':session['user']['email']})
    
    hosp_details=mydb.hospinfo.find_one({"name": name1})

    record = {
        "received_blood_type": bloodgroup,
        "units": units,
        "donated_bloodgroup": blood_type,
        "hospital_name": hosp_details["name"],
        "email": session['user']['email'],
        "status": "done",
        "phone_number": hosp_details['phone'],
        "address": hosp_details['address'],
        "datetime": datetime.now(),
        "reason":reason
    }
    result = mydb2.req.insert_one(record)
    # return redirect(url_for('hospital_details', hospital_id=hospital_id))
    return render_template("success.html")

# request_history = [
#     {"hospital_name": "Hospital A", "hospital_phone": "555-1234", "hospital_address": "123 Main St",
#      "received_blood_type": "A+", "donated_blood_type": "B+", "units": 2, "attribute1": "value1", "attribute2": "value2"},
#     {"hospital_name": "Hospital B", "hospital_phone": "555-5678", "hospital_address": "456 Oak St",
#      "received_blood_type": "B+", "donated_blood_type": "O+", "units": 3, "attribute1": "value3", "attribute2": "value4"},
#     {"hospital_name": "Hospital C", "hospital_phone": "555-91011", "hospital_address": "789 Elm St",
#      "received_blood_type": "O+", "donated_blood_type": "A+", "units": 1, "attribute1": "value5", "attribute2": "value6"},
# ]

@app.route('/request_history')
def display_request_history():
    request_history=list(mydb2.req.find({'email':session['user']['email']}))
    return render_template('request_history.html', request_history=request_history)

@app.route('/blood_community')
def blood_community():
    return render_template('blood_community.html')

@app.route('/post_request')
def post_request():
    return render_template('blood_community1.html')

@app.route('/submit_request2', methods=['POST'])
def submit_request2():
    record={
    "patient_name": request.form['patient_name'],
    "phone_number": request.form['phone_number'],
    "email": session['user']['email'],
    "name":session['user']['email'],
    "need_date": request.form['need_date'],
    "purpose": request.form['purpose'],
    "blood_group": request.form['blood_group'],
    "units": request.form['units'],
    "current_date":datetime.now()
    }
    result = mydb3.comm_req.insert_one(record)
    # Here, you can handle the form submission, like saving the data to a database

    return render_template('success.html') 

@app.route('/view_request')
def view_request():
    # dummy_requests = [
    #     {"patient_name": "John Doe", "phone_number": "123-456-7890", "date_required": "July 15, 2022",
    #      "blood_group_needed": "A+", "units_needed": 2, "address": "123 Main Street, Cityville"},
    #     {"patient_name": "Jane Smith", "phone_number": "987-654-3210", "date_required": "August 5, 2022",
    #      "blood_group_needed": "O-", "units_needed": 3, "address": "456 Elm Street, Townsville"},
    # ]
    dummy_requests = list(mydb3.comm_req.find({'email': {'$ne': session['user']['email']}}))

    return render_template('bloodcomm_viewreq.html', requests=dummy_requests)

@app.route('/my_request')
def my_requests():
    active_requests = list(mydb3.comm_req.find({'email':session['user']['email']}))
    print(active_requests)
    for index, record in enumerate(active_requests, start=1):
        record['id'] = index
    # active_requests = [
    # {"id": 1, "patient_name": "John Doe", "phone_number": "123-456-7890", "date_required": "July 15, 2022",
    #  "blood_group_needed": "A+", "units_needed": 2, "address": "123 Main Street, Cityville"},
    # {"id": 2, "patient_name": "Jane Smith", "phone_number": "987-654-3210", "date_required": "August 5, 2022",
    #  "blood_group_needed": "O-", "units_needed": 3, "address": "456 Elm Street, Townsville"},
    # # Add more dummy requests as needed
    # ]
    # return render_template("my_request.html")
    return render_template('my_request.html', active_requests=active_requests)
@app.route('/delete_request/<int:id>')
def delete_request(id):
    request_index = id-1 # Assuming the index is sent via POST request
    active_requests = list(mydb3.comm_req.find({'email': session['user']['email']}))
    if 0 <= request_index < len(active_requests):
        mydb3.comm_req.delete_one(active_requests[request_index])
    return redirect('/my_request')