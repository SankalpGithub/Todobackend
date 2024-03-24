from flask import Flask, jsonify, request
from config.mongodb_con import con
from FlaskApp.utils import email_sender, otp_generator


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
                resp = jsonify({'message': 'email id already existing', 'status': 409})
                return resp
            else:
                count = MyCol.count_documents({})
                otp = otp_generator.generate_otp()
                #verify email via otp
                email_send = email_sender.email_sender(email,otp)
                if email_send: 
                    resp = jsonify({'message': 'otp sent successfully', 'status': 200})
                    return resp
                else:
                    resp = jsonify({'message': 'otp not sent successfully', 'status': 400})
                    return resp

                
            #insert user data in db


    except Exception as e:
        resp = jsonify(f"Exception: {e}")
        return resp