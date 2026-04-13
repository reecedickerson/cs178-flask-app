# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *
import dbCode


app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        genre = request.form['genre']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name:", name, ":", "Favorite Genre:", genre)
        
        flash('User added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to delete:", name)
        
        flash('User deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-movies', methods=['GET', 'POST'])
def display_movies():
    search_term = request.args.get('search', '')
    display_field = request.args.get('field', 'title')
    
    # Base query
    query = "SELECT * FROM movie"
    args = ()
    
    # Add search filter if search term provided
    if search_term:
        query += " WHERE title LIKE %s"
        args = ('%' + search_term + '%',)
    
    # Add ordering based on selected field
    if display_field == 'overview':
        query += " ORDER BY overview"
    elif display_field == 'popularity':
        query += " ORDER BY popularity DESC"
    elif display_field == 'release_date':
        query += " ORDER BY release_date DESC"
    elif display_field == 'revenue':
        query += " ORDER BY revenue DESC"
    elif display_field == 'runtime':
        query += " ORDER BY runtime DESC"
    else:  # default to title
        query += " ORDER BY title"
    
    movie_list = dbCode.execute_query(query, args)
    return render_template('display_movies.html', movies=movie_list, search_term=search_term, display_field=display_field)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
