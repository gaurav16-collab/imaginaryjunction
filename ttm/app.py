import os
import requests
from flask import Flask, render_template, request
from monsterapi import client

app = Flask(__name__, template_folder="templates")  # 👈 Ensure this line is present


# Set API Key directly (Not recommended for production)
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImRjZjZlNWQ5MTY5MmJiNjFiM2M0MGNhYzAyYzgwMzJjIiwiY3JlYXRlZF9hdCI6IjIwMjUtMDMtMThUMTk6MDA6NDQuMzUwMzIxIn0.Yto9cURq6OX83FN7lC6_Xrv05I-dmuUlHGqJK41hC6k"

if not API_KEY:
    raise ValueError("API Key not found. Set the MONSTER_API_KEY environment variable.")

# Initialize Monster API client
monster_client = client(api_key=API_KEY)

@app.route('/', methods=['GET', 'POST'])
def generate_image():
    if request.method == 'POST':
        prompt = request.form.get('prompt')

        if not prompt:
            return "Please enter a prompt.", 400

        try:
            response = monster_client.generate(model='txt2img', data={"prompt": prompt})

            if response and 'output' in response and response['output']:
                image_url = response['output'][0]
                return render_template('index.html', image_url=image_url, prompt=prompt)

            return "Failed to generate image.", 500
        except Exception as e:
            return f"Error: {str(e)}", 500

    return render_template('index.html', image_url=None)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
