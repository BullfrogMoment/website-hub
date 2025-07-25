from flask import Flask, redirect, render_template, request, url_for, jsonify
import random   
import smtplib
from email.mime.text import MIMEText
from db import storeOTP,getOTP,deleteOTP
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/receive_details", methods=['POST'])
def receive_details():        
    if request.method == "POST":
        user_contact_info = request.get_json()
        user_email = user_contact_info["email"]
        user_phone_number = user_contact_info["phone_number"]
        print(user_contact_info)
        if "email" in user_contact_info and user_email is not None and user_phone_number is None:
            main_num_arr = [str(random.randint(1,9)) for i in range(4)]
            main_num = int(''.join(main_num_arr))
            storeOTP(email=user_email, phonenum=None, otp=main_num)

            sender_email = "infinitycaptive78@gmail.com"
            receiver_email = user_email.strip()
            load_dotenv()
            print("DEBUG >>> CURRENT DIRECTORY:", os.getcwd())
            print("DEBUG >>> .env PATH EXISTS:", os.path.exists(".env"))
            app_password = os.getenv("EMAIL_APP_PASSWORD")
            print("DEBUG >>> Loaded app_password:", app_password) 

            # Create the message
            msg = MIMEText(f"Your OTP is: {main_num}")
            msg['Subject'] = "Your OTP Code"
            msg['From'] = sender_email
            msg['To'] = receiver_email

            # Send the email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, app_password)
                server.send_message(msg)

            print("OTP sent successfully!")
            return jsonify({"status": "success", "message": "OTP has been sent."})
        elif "phone_number" in user_contact_info and user_contact_info["phone_number"] is not None:
            print("not yet started on phone number")
            return jsonify({"status": "pending", "message": "Phone Number functionality is not completed"})
    else:
        return jsonify({"status": "failed", "message": "OTP has not been sent."})

@app.route("/verify_otp", methods=['POST'])
def verify_otp():
    user_OTP_JSON = request.get_json()
    user_OTP_list_str = [
        str(user_OTP_JSON.get("first_digit","N/A")),
        str(user_OTP_JSON.get("second_digit","N/A")),
        str(user_OTP_JSON.get("third_digit","N/A")),
        str(user_OTP_JSON.get("fourth_digit","N/A"))
    ]
    user_OTP = int(''.join(user_OTP_list_str))

    identifier = user_OTP_JSON.get("identifier",None)
    correct_otp = getOTP(identifier)
    if correct_otp and user_OTP == correct_otp.get("otp"):
        print("Correct")
        deleteOTP(phonenum=None, email=identifier)
        return jsonify({"status": "success", "message": "correct OTP"})
    else:
        print("Incorrect")
        return jsonify({"status": "failed", "message": "incorrect OTP"})


@app.route("/auth_page")
def auth_page():
    """hi"""
    return render_template("authpage.html")


@app.route("/")
def redirectwebsite():
    return redirect(url_for("auth_page"))

@app.route("/home")
def home():
    return render_template("home.html")




if __name__ == '__main__':
    app.run(debug=True)