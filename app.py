from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, send_file
import json
import markdown
import markdown.extensions.fenced_code
from brain_module import run_pipeline

# Add api_key in config.json to enable running the pipeline
# Install requirements from requirements.txt



from modules.config import get_config

CONFIG = get_config()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message = request.form['message']
        responses = run_pipeline(message)
        responses[0]="```python\n"+responses[0]+"\n```"
        responses[0] = markdown.markdown(responses[0], extensions=['fenced_code', 'codehilite'])
        responses[1] = markdown.markdown(json.loads(responses[1])["explanation"], extensions=['fenced_code', 'codehilite'])
        return render_template('output.html', responses=responses)
    return render_template('index.html')


def run_flask():
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

if __name__ == '__main__':
    run_flask()
