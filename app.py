from flask import Flask, render_template, request, send_file, session, redirect, url_for
import pdfkit, os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Path to wkhtmltopdf (adjust for your OS)
path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
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
