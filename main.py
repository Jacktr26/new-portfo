from flask import Flask, render_template, url_for, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def my_home():
    today = datetime.today().strftime('%B %d, %Y')  # e.g., June 18, 2025
    return render_template('index.html', today=today)

@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(f"{page_name}.html")

@app.route('/generic')
def generic_page():
    success = request.args.get('success')
    return render_template('generic.html', success=success)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        name = data.get("name", "")
        email = data.get("email", "")
        message = data.get("message", "")
        file = database.write(f'\n{name},{email},{message}')

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        name = data.get("name", "")
        email = data.get("email", "")
        message = data.get("message", "")
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])


@app.route('/next')
def next_page():
    return "You've been redirected to the next page!"

@app.route('/redirect', methods=['POST'])
def redirect_user():
    return redirect(url_for('next_page'))

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/generic?success=1')  # redirect back to the form with a flag
    except Exception as e:
        return f'An error occurred: {e}'

@app.route("/privacy")
def privacy_policy():
    return render_template("privacy.html")

@app.route("/gigs")
def gigs():
    return render_template("gigs.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")


if __name__ == '__main__':
    app.run(debug=True)