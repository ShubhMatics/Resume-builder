# resume-builderProject Overview

You're building a Flask web application that:

Lets users fill out a resume form

Previews the resume in HTML (resume_template.html)

Converts it to PDF using pdfkit (which internally calls wkhtmltopdf)

Lets the user download the generated PDF

You want to deploy this on Render, a popular cloud platform for deploying full-stack web applications.

✅ 2. Dependencies (requirements.txt)

You'll need a requirements.txt file so Render knows which Python packages to install. Below is a minimal and complete list:

Flask==3.0.3             # Web framework
Jinja2==3.1.4            # Templating engine used by Flask
Werkzeug==3.0.3          # WSGI server library used internally by Flask
pdfkit==1.0.0            # Python wrapper for wkhtmltopdf
gunicorn==21.2.0         # Production WSGI HTTP server


⚠️ pdfkit requires wkhtmltopdf to be installed in the system (more on that in the next step).

✅ 3. Installing System Dependency (wkhtmltopdf)

pdfkit depends on a binary system utility called wkhtmltopdf, which is not a Python package. You must install it separately during the build phase.

✅ Solution: build.sh

Create a file named build.sh in the root directory:

#!/usr/bin/env bash
apt-get update
apt-get install -y wkhtmltopdf


Make it executable:

chmod +x build.sh


This script will install wkhtmltopdf during your Render build.

✅ 4. Specify Build & Start Commands (render.yaml)

Create a render.yaml file in the root of your project. This tells Render what to do during deployment.

services:
  - type: web
    name: resume-builder
    runtime: python
    buildCommand: ./build.sh
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.13


buildCommand: Runs the script to install wkhtmltopdf

startCommand: Starts your app with Gunicorn

app:app: means app.py contains app = Flask(__name__)

envVars: Optional, for setting Python version

✅ 5. Application File Structure

Here’s a recommended structure for your project:

resume-app/
│
├── app.py                # Your main Flask app
├── requirements.txt      # Python dependencies
├── build.sh              # Install wkhtmltopdf during Render build
├── render.yaml           # Render deployment configuration
├── templates/
│   ├── index.html
│   └── resume_template.html
├── output/               # Folder to store generated PDFs


📝 templates/ is required by Flask to find Jinja2 templates like index.html.

✅ 6. Flask App (app.py)

Your existing app.py already looks correct:

from flask import Flask, render_template, request, send_file, session, redirect, url_for
import pdfkit, os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
options = {'enable-local-file-access': ''}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    data = request.form.to_dict()
    session['resume_data'] = data
    return render_template('resume_template.html', data=data, mode='preview')

@app.route('/download')
def download():
    data = session.get('resume_data')
    if not data:
        return redirect(url_for('index'))

    rendered = render_template('resume_template.html', data=data, mode='pdf')
    output_path = os.path.join('output', 'resume.pdf')
    pdfkit.from_string(rendered, output_path, configuration=config, options=options)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

✅ 7. Troubleshooting Common Issues
❌ Error: TemplateNotFound: index.html

🔧 Solution:
Make sure you have a templates/ folder and that index.html is inside it:

resume-app/
└── templates/
    └── index.html


Flask looks inside the templates/ folder by default.

✅ 8. Final Deployment Steps on Render

Push your code to a GitHub repo

Go to Render

Click "New Web Service"

Connect your GitHub repo

Use the following settings:

Runtime: Python
