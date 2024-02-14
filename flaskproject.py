from flask import Flask, request, jsonify, json, abort, Blueprint
import sqlite3

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
sqlite3.connect('my_database.db')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join(__file__, '..', '..', 'employees.db'))
 
def init_db():
        conn = sqlite3.connect('my_database.db')
        conn.execute("CREATE TABLE IF NOT EXISTS employees "
                     "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "name TEXT NOT NULL,"
                     "position TEXT NOT NULL,"
                     "salary REAL);")
    
        conn.close()

init_db()
 
# getting the deatils of employeee from the db
@app.route('/employees_details',methods=['Get'])
def get_employees():
     conn = sqlite3.connect('my_database.db')
     cursor = conn.cursor()
     query='SELECT * FROM employees'
     cursor.execute(query)
     employes=cursor.fetchall()
     conn.commit()
     conn.close()
     return employes

@app.route('/employees/<id>',methods=['Delete'])
def delete_employees(id:int):
     conn = sqlite3.connect('my_database.db')
     cursor = conn.cursor()
     query = "DELETE FROM employees WHERE id = ?"
     cursor.execute(query,(id,))
     conn.commit()
     conn.close()
     return {"delete":"employee deleted"}
     

@app.route('/employees/<name>/<id>',methods=['Put'])
def update_employees(name:str,id:int):
     conn = sqlite3.connect('my_database.db')
     cursor = conn.cursor()
     query="UPDATE employees SET name = ? WHERE id = ?"
     cursor.execute(query,(name,id))
      
     conn.commit()
     conn.close()
     return {"update":"employee details is updated"}

# adding the employeee details to db
@app.route('/employee', methods=['POST'])
def add_employee():
    try:
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        name = request.json.get('name', None)
        position = request.json.get('position', None)
        salary = request.json.get('salary', None)

        if not name or not position or not salary:
            response = {"error": "Missing required fields"}
            return jsonify(response), 400

        query = "INSERT INTO employees(name, position, salary) VALUES(?, ?, ?)"
        cursor.execute(query, (name, position, salary))
         
        conn.commit()
        conn.close()
        response = {"message": "Employee added successfully!"}
        return jsonify(response), 201
    except sqlite3.Error as error:
        response = {"error": f"Error adding employee: {error}"}
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(debug=True)