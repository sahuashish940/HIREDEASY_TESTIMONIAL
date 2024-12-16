from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import cloudinary
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

# Cloudinary Setup
cloudinary.config(
    cloud_name="dgxzx0tpr",
    api_key="929353541146446",
    api_secret="3YxlBA1B_fcd8LVMnv5VeJJioWY"
)

# MongoDB Setup
try:
    client = MongoClient("mongodb+srv://Asahu:Asahu123@testimonial.axqlc.mongodb.net/?retryWrites=true&w=majority&appName=testimonial")
    db = client["testimonials"]  # Database
    collection = db["user_testimonials"]  # Collection
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/', methods=['GET', 'POST'])
def create_testimonial():
    try:
        if request.method == 'POST':
            client_name = request.form['client_name']
            description = request.form['description']
            linkedin_url = request.form['linkedin_url']
            position = request.form['position']

            # Upload images to Cloudinary
            profile_image = request.files['profile_image']
            company_image = request.files['company_image']

            # Secure upload to Cloudinary and get the URLs
            profile_image_result = upload(profile_image, folder="testimonials/profile_images")
            company_image_result = upload(company_image, folder="testimonials/company_images")

            profile_image_url = profile_image_result['secure_url']
            company_image_url = company_image_result['secure_url']

            # Store testimonial data in MongoDB
            testimonial_data = {
                "client_name": client_name,
                "description": description,
                "linkedin_url": linkedin_url,
                "position": position,
                "profile_image": profile_image_url,
                "company_image": company_image_url
            }

            collection.insert_one(testimonial_data)
            return redirect(url_for('thank_you', name=client_name))
    except Exception as e:
        print(f"Error: {e}")
        flash("Something went wrong. Please contact us at xyz@gmail.com for help.", "error")
        return redirect(url_for('error_page'))

    return render_template('create_testimonial.html')


@app.route('/thank-you/<name>')
def thank_you(name):
    return render_template('thank_you.html', name=name)

@app.route('/error')
def error_page():
    return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True)
