# 🖊️ Automatic Signature Verification System

A web-based application to verify the authenticity of handwritten signatures using image processing and structural similarity techniques.

## Overview
This system validates user-submitted signatures by comparing them to stored originals using image preprocessing and SSIM (Structural Similarity Index Measure) — without any machine learning or neural networks.

It is built with Python (Django) for the backend, MySQL for data storage, and a clean, responsive frontend using HTML, CSS, JS, and Bootstrap.

## Features
- User registration and login
- Admin dashboard to manage data
- Upload & verify signatures
- Image comparison using SSIM
- Stores verification results in a database

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Backend**: Python, Django
- **Database**: MySQL
- **Image Processing**: OpenCV, PIL
- **Similarity Check**: SSIM (Structural Similarity Index)

##  How to Run

```bash
git clone https://github.com/suhani-kharode/Automatic-Signature-Verification-System.git
cd Automatic-Signature-Verification-System
pip install -r requirements.txt
python manage.py runserver
