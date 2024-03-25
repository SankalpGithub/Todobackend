from flask import Flask, jsonify, request
from config.mongodb_con import con
from FlaskApp.utils import email_sender, otp_generator, password_hash
from datetime import datetime, timedelta


#get collection from mongodb
MyClient = con()
MyCol = MyClient['users']

#registration route
def register():
    try:
        #take inputs
        _json = request.json
        
        #check null values
        if 'name' not in _json or 'email' not in _json or 'password' not in _json:
            missing_values = []
            if 'name' not in _json:
                missing_values.append('name')
            if 'email' not in _json:
                missing_values.append('email')
            if 'password' not in _json:
                missing_values.append('password')
            message = f"The following fields are missing or empty: {', '.join(missing_values)}"
            resp = jsonify({'message': message, 'status': 400})
            return resp
        
        else:

            name = _json.get('name')
            email = _json.get('email')
            password = _json.get('password')

            #check for email in db
            query = {'email': email}
            existing_doc = MyCol.find_one(query)
            if existing_doc:
                if existing_doc['verify']:
                    resp = jsonify({'message': 'email id already existing', 'status': 409})
                    return resp
                else:
                    #resend otp
                    resp = jsonify({'message':'verify your otp', 'status': 200})
                    return resp
            else:
                count = MyCol.count_documents({})

                #hash password
                hash_password = password_hash.hash_password(password)

                #verify email via otp
                otp = otp_generator.generate_otp()
                email_send = email_sender.email_sender(email,otp)

                if email_send: 
                    otp_expiry = datetime.now() + timedelta(minutes=2)
                    resp = jsonify({'message': 'otp sent successfully', 'status': 200})

                    #insert user data in db
                    MyCol.insert_one({'_id': count, 'name': name, 'email': email, 'password': hash_password, 'otp_list': {'otp': otp, 'expiry': otp_expiry}, 'verify': False})
                    return resp
                else:
                    resp = jsonify({'message': 'otp not sent successfully', 'status': 400})
                    return resp

    except Exception as e:
        resp = jsonify(f"Exception: {e}")
        return resp
    
def resend_otp(id):
    otp = otp_generator.generate_otp()
    

                