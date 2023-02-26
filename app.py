from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #orm for sqlite
from datetime import datetime

app = Flask(__name__)
# add extra configurations to the app object for flask to locate the database - uniform resource identifier - file that'll be identified
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #we just want it to reside in our folder
# app.config - dictionary that'll accept new key values
db = SQLAlchemy(app) #database is being initialized with settings from our app

app.app_context().push() #push to application context stack

# create model
class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # function that'll return string everytime we create a new element
    def __repr__(self):
        return '<Task %r>' % self.id # returns task and id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': 
        #create new task from input
        task_content = request.form['content'] #pass in id of input we wanted
        new_task = Todo(content=task_content)

        try: 
            db.session.add(new_task) #add to database
            db.session.commit() #commit to database
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all() #.first() for most recent by date
        return render_template('index.html', tasks=tasks) 


@app.route('/delete/<int:id>')    
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #get task by id, 404 if no exist
    
    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try: 
            db.session.commit() #just have to commit to update
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)