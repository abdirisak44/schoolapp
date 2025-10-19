from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from supabase import create_client, client
url="https://zbtdbfajfvgzdmkbobsa.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpidGRiZmFqZnZnemRta2JvYnNhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA3MTk3ODcsImV4cCI6MjA3NjI5NTc4N30.I0sZOQ6zCu9uUkKCICML6DHzbwmXHkextmwuXzaMDMI"
supabase:client=create_client(url,key)
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:/// school2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)

class studentstbl(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    faculty=db.Column(db.String(100), nullable=False)
    semester=db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)


class teacherstbl(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    faculty=db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(100), nullable=False)

class staffstbl(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    position=db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
        students=studentstbl.query.all()
        return render_template("index.html",students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
        name=request.form['name']
        faculty=request.form['faculty']
        semester=request.form['semester']
        phone = request.form['phone']

        student=studentstbl(name=name,faculty=faculty,semester=semester,phone=phone)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/add_teacher')
def show_teachers():
        teachers=teacherstbl.query.all()
        return render_template("teachers.html",teachers=teachers)
    
@app.route('/add_teacher', methods=['POST'])
def add_teacher():
        name=request.form['name']
        faculty=request.form['faculty']
        semester=request.form['semester']
        teacher=teacherstbl(name=name,faculty=faculty,semester=semester)
        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for('add_teacher'))
    
@app.route('/add_staff')
def show_staff():
        staffs=staffstbl.query.all()
        return render_template("staffs.html",staffs=staffs)
    
@app.route('/add_staff', methods=['POST'])
def add_staff():
        name=request.form['name']
        position=request.form['position']
        salary=request.form['salary']
        staff=staffstbl(name=name,position=position,salary=salary)
        db.session.add(staff)
        db.session.commit()
        return redirect(url_for('show_staff'))
#delete student
@app.route('/delete_student/<int:student_id>',methods=['POST'])
def delete_student(student_id):
      student=studentstbl.query.get_or_404(student_id)
      db.session.delete(student)
      db.session.commit()
      return redirect(url_for('index'))

@app.route('/delete_teacher/<int:teacher_id>',methods=['POST'])
def delete_teacher(teacher_id):
      teacher=teacherstbl.query.get_or_404(teacher_id)
      db.session.delete(teacher)
      db.session.commit()
      return redirect(url_for('add_teacher'))

@app.route('/delete_staff/<int:staff_id>',methods=['POST'])
def delete_staff(staff_id):
      staff=staffstbl.query.get_or_404(staff_id)
      db.session.delete(staff)
      db.session.commit()
      return redirect(url_for('show_staff'))
#update
@app.route('/edit_student/<int:student_id>',methods=['POST','GET'])
def edit_student(student_id):
      student=studentstbl.query.get_or_404(student_id)
      if request.method=='POST':
            student.name=request.form['name']
            student.faculty=request.form['faculty']
            student.semester=request.form['semester']
            student.phone=request.form['phone']
            db.session.commit()
            return redirect(url_for('index'))
      return render_template('edit_student.html',student=student)
           
@app.route('/edit_teacher/<int:teacher_id>',methods=['POST','GET'])
def edit_teacher(teacher_id):
      teacher=teacherstbl.query.get_or_404(teacher_id)
      if request.method=='POST':
            teacher.name=request.form['name']
            teacher.faculty=request.form['faculty']
            teacher.semester=request.form['semester']
            db.session.commit()
            return redirect(url_for('add_teacher'))
      return render_template('edit_teacher.html',teacher=teacher)
           
  
if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


