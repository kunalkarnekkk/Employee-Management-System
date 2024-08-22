from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='employee'
    )

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    # if 'username' in session:
    #     return redirect(url_for('add_employee'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate user
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('add_employee'))
        else:
            return 'Invalid username or password'

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_emp')
def add_emp():
    return render_template('login.html')

# # Add Button 
# @app.route('/add')
# def add():
#     return redirect(url_for('login'))

# # Remove button 
# @app.route('/remove')
# def remove():
    


# Add employee route
@app.route('/add_employee_page')
def add_empl():
    return render_template('add_emp.html')

# Remove employee route
@app.route('/remove_employee_page')
def remove_empl():
    return render_template('remv_emp.html')

# Promote Employee route
@app.route('/promote_employee_page')
def promote_empl():
    return render_template('promote_employee.html')

## Display Employee route
@app.route('/display_employee_page')
def display_emp1():
    return render_template('disp.html')

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']

        try:
            # Save employee details to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO employees (name, position, department) VALUES (%s, %s, %s)', (name, position, department))
            conn.commit()
            conn.close()
            return redirect(url_for('add_employee'))
        except Exception as e:
            return "An error occurred while adding employee" 
    return render_template('add_employee.html')

# # Remove employee route
# @app.route('/remove_employee', methods=['POST'])
# def remove_employee():
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     employee_id = request.form.get('employee_id', type=int)

#     if employee_id is None:
#         return "Invalid employee ID", 400  # Bad request response with status code 400

#     try:
#         # Get employee details before removing
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM employees WHERE id = %s', (employee_id,))
#         employee_data = cursor.fetchone()

#         # Insert employee details into another table (e.g., removed_employees)
#         cursor.execute('INSERT INTO removed_employees (id, name, position, department) VALUES (%s, %s, %s, %s)', employee_data)
        
#         # Remove employee from the main table
#         cursor.execute('DELETE FROM employees WHERE id = %s', (employee_id,))
#         conn.commit()
#         conn.close()
        
#         return redirect(url_for('add_employee')), 302  # Redirect response with status code 302 (Found)
#     except Exception as e:
#         return "An error occurred while removing employee", 500  # Internal Server Error response with status code 500

# Remove employee route
@app.route('/remove_employee', methods=['POST'])
def remove_employee():
    if 'username' not in session:
        return redirect(url_for('login'))

    employee_id = request.form.get('employee_id', type=int)

    if employee_id is None:
        return "Invalid employee ID"  # Bad request response

    try:
        # Get employee details before removing
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = %s', (employee_id,))
        employee_data = cursor.fetchone()

        # Insert employee details into another table (e.g., removed_employees)
        cursor.execute('INSERT INTO removed_employees (id, name, position, department) VALUES (%s, %s, %s, %s)', employee_data)
        
        # Remove employee from the main table
        cursor.execute('DELETE FROM employees WHERE id = %s', (employee_id,))
        conn.commit()
        conn.close()
        
        return redirect(url_for('add_employee'))
    except Exception as e:
        return "An error occurred while removing employee", 

# Promote employee route*
@app.route('/promote_employee', methods=['GET', 'POST'])
def promote_employee():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        new_position = request.form['new_position']
        new_department = request.form['new_department']

        try:
            # Update employee details in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE employees SET position = %s, department = %s WHERE id = %s', (new_position, new_department, employee_id))
            conn.commit()
            conn.close()
            return redirect(url_for('add_employee'))
        except Exception as e:
            return "An error occurred while promoting employee", 500  
    return render_template('add_employee.html')

# @app.route('/display_employee', methods=['GET'])
# def display_employee():
#     # Get employee ID from the request query parameters
#     employee_id = int(request.args.get('employee_id'))

#     try:
#         # Establish database connection
#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         # Fetch employee details from the database           
#         cursor.execute('SELECT * FROM employees WHERE id = %s', (employee_id,))
#         employee = cursor.fetchone()

#         conn.close()

#         if employee:
#             return render_template('display_employee.html', employee=employee)
#         else:
#             return "Employee not found", 404  # Return a not found response if employee is not found
#     except Exception as e:
#         return "An error occurred while fetching employee details", 500  # Return a server error response

@app.route('/display_employee', methods=['GET'])
def display_employee():
    # Get employee position from the request query parameters
    position = request.args.get('position')

    if not position:
        return "Position parameter is required", 400  

    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch employees with the specified position from the database
        cursor.execute('SELECT * FROM employees WHERE position = %s', (position,))
        employee = cursor.fetchall()

        conn.close()

        return render_template('display_employee.html', employee=employee,position=position)
    except Exception as e:
        return str(e)
if __name__ == '__main__':
    app.run(debug=True)

