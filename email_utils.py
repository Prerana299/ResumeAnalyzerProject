import streamlit as st
import sqlite3
import pandas as pd
import re
import spacy
import pdfplumber
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def send_email(receiver_email, candidate_name):
    sender_email = 'shrutiashinde26@gmail.com'
    sender_password = 'uenm qhvh nllw odwj'

    subject = "Congratulations on Your Shortlisting!"
    body = f"""
    Dear {candidate_name},

    Congratulations! 🎉

    We are pleased to inform you that your resume has been shortlisted.

    Best regards,  
    Recruitment Team
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(e)
        return False