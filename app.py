from flask import Flask, render_template
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS']=False

from models import db, Entry
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    today = datetime.now().strftime("%d-%b-%Y,%A")
    return render_template("index.html", date=today)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect all form data
    date = datetime.now().strftime("%d-%b-%Y, %A")
    journal_notes = request.form.get('journal_notes', '')
    
    # Habits data (radio buttons)
    habits = {
        'water': request.form.get('habit_water'),
        'read': request.form.get('habit_read'),
        'learn': request.form.get('habit_learn'),
        'walk': request.form.get('habit_walk'),
        'meditate': request.form.get('habit_meditate'),
        'nojunk': request.form.get('habit_nojunk')
    }
    
    # Tracker data (text inputs)
    tracker = {
        'screentime': request.form.get('tracker_screentime', ''),
        'steps': request.form.get('tracker_steps', ''),
        'learned': request.form.get('tracker_learned', ''),
        'sleep': request.form.get('tracker_sleep', ''),
        'water': request.form.get('tracker_water', '')
    }
    
    # Reflection data
    reflection_good = request.form.get('reflection_good', '')
    reflection_bad = request.form.get('reflection_bad', '')
    reflection_improve = request.form.get('reflection_improve', '')
    
    # Create new Entry object
    from models import Entry
    entry = Entry(
        date=date,
        journal_notes=journal_notes,
        habits=habits,
        tracker=tracker,
        reflection_good=reflection_good,
        reflection_bad=reflection_bad,
        reflection_improve=reflection_improve
    )
    
    # Save to database
    db.session.add(entry)
    db.session.commit()
    
    # Redirect to entries list
    return redirect(url_for('entries'))

@app.route('/entries')
def entries():
    from models import Entry
    all_entries = Entry.query.order_by(Entry.created_at.desc()).all()
    
    # Simple HTML output for testing
    output = "<h1>Past Entries</h1>"
    if all_entries:
        output += "<ul>"
        for entry in all_entries:
            output += f"<li><strong>{entry.date}</strong> – {entry.journal_notes[:100]}...</li>"
        output += "</ul>"
    else:
        output += "<p>No entries yet.</p>"
    output += "<p><a href='/'>Back to journal</a></p>"
    return output

if __name__ == "__main__":
    app.run(debug=True)