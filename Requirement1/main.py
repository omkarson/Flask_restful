from flask import Flask, render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
mydb = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sunbeam:sunbeam@localhost/optum_test'
app.register_blueprint


##Swagger specific code
swagger_url = '/swagger'
api_url = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    swagger_url,
    api_url,
    config={
        'app_name': "Employee - management dashboard api"
    }
)
app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)




@app.before_first_request
def create_table():
    mydb.create_all()


class Employee(mydb.Model):

    __tablename__= "employee"

    id = mydb.Column(mydb.Integer, primary_key=True)
    first_name = mydb.Column(mydb.String(50))
    middle_name = mydb.Column(mydb.String(50))
    last_name = mydb.Column(mydb.String(50))
    age = mydb.Column(mydb.Integer())

    position = mydb.Column(mydb.String(80))
    phone = mydb.Column(mydb.String(80))
    city = mydb.Column(mydb.String(80))
    state = mydb.Column(mydb.String(80))



    def __init__(self,first_name,middle_name,last_name,age,position, phone, city, state):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age
        self.position = position
        self.phone = phone
        self.city = city
        self.state = state


# employees = []

@app.route('/', methods=['GET'])
def home():


            return render_template('home.html')






@app.route('/create_employee', methods=['GET', 'POST'])
def create_employee():

    if request.method == "POST":

       # employees['first name'] = request.form.get('first_name')
       # employees['middle name'] = request.form.get('middle_name')
       emp = Employee(request.form.get('first_name'),request.form.get('middle_name'),request.form.get('last_name'),request.form.get('age'), request.form.get('position'),request.form.get('phone'),request.form.get('city'),request.form.get('state'))
       # employees.append(emp)
       mydb.session.add(emp)
       mydb.session.commit()

       return redirect('/list_employees')
    return render_template("create_employee.html")
@app.route('/list_employees')
def list_employees():
    employees = Employee.query.all()
    return render_template('list_employee.html', emp=employees)

@app.route('/list_employees/<int:eid>/delete', methods=['POST','GET'])
def delete_employee(eid):
    try:
        emp1 = Employee.query.filter_by(id=eid).first()
        if emp1:
            mydb.session.delete(emp1)
            mydb.session.commit()
            return redirect('/list_employees')
    except Exception :
        print("Problem with deleting the employee")

@app.route('/view_employee/<int:eid>', methods=['GET'])
def view_employee(eid):
    employee = Employee.query.filter_by(id=eid).first()
    if employee:
        return render_template('view_data.html', employee=employee)

@app.route('/update/<int:eid>', methods=['GET',"POST"])
def update_employee(eid):
    try:
        employee = Employee.query.filter_by(id=eid).first()
        if request.method == 'POST':
            if employee:
                # first_name = request.form.get('first_name')
                # middle_name =  request.form.get('middle_name')
                # last_name = request.form.get('last_name')
                # age = int(request.form.get('age'))
                # position = request.form.get('position')
                # phone = request.form.get('phone')
                # city = request.form.get('city')
                # state = request.form.get('state')
                # emp = Employee(first_name, middle_name, last_name, age,position,phone,city,state)
                mydb.session.query(Employee).filter_by(id=eid).update({
                    "first_name": request.form.get('first_name'),
                    "middle_name": request.form.get("middle_name"),
                    "last_name": request.form.get("last_name"),
                    "age": request.form.get("age"),
                    "position": request.form.get('position'),
                    "phone": request.form.get('phone'),
                    "city": request.form.get('city'),
                    "state": request.form.get('state')

                })
                # mydb.session.add(emp)
                mydb.session.commit()
                return redirect("/list_employees")
        return render_template("update_employee.html", employee=employee)
    except:
        print("Bad request")

if __name__ == '__main__':
    app.run(debug=True, port=10000)


# create table employee(id int Primary key, name varchar(50), age int, position varchar(50));