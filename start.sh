#!/usr/bin/env bash

# 1. PERINTAH BUILD (Instalasi Dependensi)
# Railpack akan menjalankan ini untuk menyiapkan lingkungan
pip install -r requirements.txt

# 2. PERINTAH START (Menjalankan Aplikasi)
# Perintah ini menggantikan "web: python app.py" dari Procfile Anda, 
# tetapi lebih baik menggunakan server produksi seperti Gunicorn

gunicorn app:app
# ATAU jika Anda ingin menjalankan dengan python app.py sesuai Procfile:
# python app.py