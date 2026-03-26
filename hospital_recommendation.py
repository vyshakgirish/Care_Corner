from flask import Flask, request, render_template, Blueprint

# Initialize the Blueprint
hospital_recommendation = Blueprint('hospital_recommendation', __name__, template_folder="templates")

# Sample data: Dictionary mapping diseases to detailed hospital recommendations
hospital_data =  {
    "general medicine": [
        {
            "name": "SRM General Hospital, Kattankulathur", 
            "contact": "044 4743 2345", 
            "website": "https://www.srmist.edu.in/hospital/", 
            "location": "https://www.google.com/maps?sca_esv=5430cf780e99fb8b&rlz=1C1JJTC_enIN1065IN1066&biw=1536&bih=730&sxsrf=ADLYWILCi6jF0tinzpDvYcziIeCebLYF1A:1733754601564&uact=5&gs_lp=Egxnd3Mtd2l6LXNlcnAiJlNwaGVhcldlbGwgLSBTcGVlY2ggYW5kIEhlYXJpbmcgQ2VudGVyMgYQABgWGB4yCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMgUQABjvBTIIEAAYgAQYogRI6wVQAFgAcAB4AJABAJgB4AGgAeABqgEDMi0xuAEDyAEA-AEC-AEBmAIBoALjAZgDAJIHAzItMaAHjQg&um=1&ie=UTF-8&fb=1&gl=in&sa=X&geocode=KY_jOht2e687MYTR5S9tO1gy&daddr=%23209,+First+Floor,+Sharadadevi+Nagar,+Circle,+Mysuru,+Karnataka+5700229"
        },
        {
            "name": "K.R. Hospital, Guduvanchery", 
            "contact": "044 2746 5566", 
            "website": "https://www.krhospital.in/", 
            "location": "https://www.google.com/maps/dir//Kamakshi+Hospital+Rd,+Kuvempunagara+North,+Kuvempu+Nagara,+Mysuru,+Karnataka+570009/@12.2998162,76.5413332,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x3baf7ab735a0053f:0x36b46e10756a3e7d!2m2!1d76.6237351!2d12.2998285?entry=ttu&g_ep=EgoyMDI0MTIwMS4xIKXMDSoASAFQAw%3D%3D0"
        }
    ],
    "emergency medicine": [
        {
            "name": "SRM Global Hospitals, Kattankulathur", 
            "contact": "044 2745 1568", 
            "website": "https://srmglobalhospitals.com/", 
            "location": "https://www.google.com/maps/dir//Kamakshi+Hospital+Rd,+Kuvempunagara+North,+Kuvempu+Nagara,+Mysuru,+Karnataka+570009/@12.2998162,76.5413332,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x3baf7ab735a0053f:0x36b46e10756a3e7d!2m2!1d76.6237351!2d12.2998285?entry=ttu&g_ep=EgoyMDI0MTIwMS4xIKXMDSoASAFQAw%3D%3D1"
        },
        {
            "name": "SIMS Hospital, Vadapalani", 
            "contact": "044 2000 2001", 
            "website": "https://simshospitals.com/", 
            "location": "https://maps.app.goo.gl/vadapalani"
        }
    ],
    "orthopedics": [
        {
            "name": "BOSH - Brain Orthopaedic Spine Hospital", 
            "contact": "044 4292 4292", 
            "website": "https://boshhospital.com/", 
            "location": "https://www.google.com/maps/dir//Kamakshi+Hospital+Rd,+Kuvempunagara+North,+Kuvempu+Nagara,+Mysuru,+Karnataka+570009/@12.2998162,76.5413332,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x3baf7ab735a0053f:0x36b46e10756a3e7d!2m2!1d76.6237351!2d12.2998285?entry=ttu&g_ep=EgoyMDI0MTIwMS4xIKXMDSoASAFQAw%3D%3D2"
        },
        {
            "name": "Madras Joint Replacement Center (MJRC)", 
            "contact": "044 2499 1234", 
            "website": "https://www.mjrc.in/", 
            "location": "https://www.google.com/maps/dir//Kamakshi+Hospital+Rd,+Kuvempunagara+North,+Kuvempu+Nagara,+Mysuru,+Karnataka+570009/@12.2998162,76.5413332,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x3baf7ab735a0053f:0x36b46e10756a3e7d!2m2!1d76.6237351!2d12.2998285?entry=ttu&g_ep=EgoyMDI0MTIwMS4xIKXMDSoASAFQAw%3D%3D3"
        }
    ],
    "neurology": [
        {
            "name": "BOSH - Brain Orthopaedic Spine Hospital", 
            "contact": "044 4292 4292", 
            "website": "https://boshhospital.com/", 
            "location": "https://www.google.com/maps/dir//Kamakshi+Hospital+Rd,+Kuvempunagara+North,+Kuvempu+Nagara,+Mysuru,+Karnataka+570009/@12.2998162,76.5413332,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x3baf7ab735a0053f:0x36b46e10756a3e7d!2m2!1d76.6237351!2d12.2998285?entry=ttu&g_ep=EgoyMDI0MTIwMS4xIKXMDSoASAFQAw%3D%3D2"
        },
        {
            "name": "Apollo First Med Hospitals, Purasawalkam", 
            "contact": "044 2829 4444", 
            "website": "https://www.apollohospitals.com/", 
            "location": "https://www.google.com/maps/dir//Kamakshi+Hospital+Rd,+Kuvempunagara+North,+Kuvempu+Nagara,+Mysuru,+Karnataka+570009/@12.2998162,76.5413332,12z/data=!4m8!4m7!1m0!1m5!1m1!1s0x3baf7ab735a0053f:0x36b46e10756a3e7d!2m2!1d76.6237351!2d12.2998285?entry=ttu&g_ep=EgoyMDI0MTIwMS4xIKXMDSoASAFQAw%3D%3D4"
        }
    ],
    "pediatrics": [
        {
            "name": "SRM General Hospital (Paediatrics Wing)", 
            "contact": "044 4743 2345", 
            "website": "https://www.srmist.edu.in/hospital/", 
            "location": "https://www.google.com/maps?sca_esv=5430cf780e99fb8b&rlz=1C1JJTC_enIN1065IN1066&biw=1536&bih=730&sxsrf=ADLYWILCi6jF0tinzpDvYcziIeCebLYF1A:1733754601564&uact=5&gs_lp=Egxnd3Mtd2l6LXNlcnAiJlNwaGVhcldlbGwgLSBTcGVlY2ggYW5kIEhlYXJpbmcgQ2VudGVyMgYQABgWGB4yCxAAGIAEGIYDGIoFMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMgUQABjvBTIIEAAYgAQYogRI6wVQAFgAcAB4AJABAJgB4AGgAeABqgEDMi0xuAEDyAEA-AEC-AEBmAIBoALjAZgDAJIHAzItMaAHjQg&um=1&ie=UTF-8&fb=1&gl=in&sa=X&geocode=KY_jOht2e687MYTR5S9tO1gy&daddr=%23209,+First+Floor,+Sharadadevi+Nagar,+Circle,+Mysuru,+Karnataka+5700229"
        },
        {
            "name": "Dr. Mehta's Hospitals", 
            "contact": "044 4227 1001", 
            "website": "https://mehtahospital.com/", 
            "location": "https://maps.app.goo.gl/chetpet"
        }
    ]
}



# Blueprint routes
@hospital_recommendation.route('/')
def hospital_recommendation_home():
    return render_template('hospital_recommendation.html', hospital_data=hospital_data)

@hospital_recommendation.route('/recommend', methods=['GET'])
def recommend_hospital():
    disease = request.args.get('disease', '').lower()
    recommended_hospitals = hospital_data.get(disease, [])
    return render_template(
        'hospital_recommendation.html', 
        hospital_data=hospital_data,
        selected_disease=disease,
        recommended_hospitals=recommended_hospitals
    )

# Create Flask App
app = Flask(__name__)

# Register Blueprint
app.register_blueprint(hospital_recommendation, url_prefix='/hospital_recommendation')

# Main app route
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
