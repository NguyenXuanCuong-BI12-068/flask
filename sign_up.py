from flask import Flask, render_template, redirect, url_for, request
from flask.connect_database import initialize_database


def Sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            conn = initialize_database()
            if conn is not None:
                try:
                    print("Connected to the database successfully.")
                    c = conn.cursor()
                    # Check if the username already exists in the database
                    duplicate = "select * from User where username = %s"
                    c.execute(duplicate, (username,))
                    user_exists = c.fetchone()
                    if user_exists:
                        return render_template('error.html', message="Username already exists. Please choose a different username.")
                    else:
                        # Insert the new user into the database
                        
                        insert_user = "INSERT INTO User (username, password) VALUES (%s, %s)"
                        values = (username, password)
                        c.execute(insert_user, values)
                        conn.commit()
                        return redirect(url_for('login'))  # Redirect to the login page after successful sign-up
                except Exception as e:
                    print("Error executing SQL statement:", e)
                    return render_template('error.html', message="Error while signing up.")
                finally:
                    c.close()
                    conn.close()
            else:
                print("Failed to connect to the database.")
                return render_template('error.html', message="Database connection failed.")
        else:
            return redirect(url_for('sign_up'))  # Redirect back to the sign-up page if the input is invalid
    else:
        return render_template('sign_up.html')