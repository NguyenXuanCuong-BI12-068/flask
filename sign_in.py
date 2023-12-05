from flask import Flask, render_template,redirect, url_for, request
from flask.connect_database import initialize_database

def Sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            #  Connect to the database
            conn = initialize_database()
            if conn is None:
                return "Error to connect database"
            try:
                # Check whether username and password are match!
                c = conn.cursor()
                check = "select * from User where username = %s and password = %s"
                values = (username,password)
                c.execute(check, values)
                # fetch the result
                result = c.fetchone()
                if result:
                    
                    return redirect(url_for('dashboard', username=username))
                else:
                    error = "Username or Password are incorrect! Try again!"
                    return render_template('error.html', message = error)
            except Exception as e:
                print("Error executing SQL query:", e)
                return "An error occurred"
            finally:
                c.close()
                conn.close()

        else:
            return redirect(url_for('login'))
    else:
        return render_template('index.html')