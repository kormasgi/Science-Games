from flask import Flask, request, send_file
import requests
from io import BytesIO
from PIL import Image
import os
from selenium import webdriver

app = Flask(__name__)
driver = webdriver.Chrome()

#classes = ["judaic studies", "social studies", "hebrew", "dinim", "biology", "earth science", "physics", "spanish", "language arts", "math", "chumash"]

@app.route("/")
def get_tests():
    password = request.form["future"].lower()
    driver.get("put in the url of the google classroom home page here")
    #get to the home page then sign in
    driver.find_element("judaic studies").click()
    driver.find_element("test").click()