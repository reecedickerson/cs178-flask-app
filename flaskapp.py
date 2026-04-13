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

@app.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        overview = request.form['overview']
        
        # lines added with help of VSCode's copilot
        query = "INSERT INTO movie (title, overview) VALUES (%s, %s)"
        dbCode.execute_insert(query, (title, overview))
        
        flash('Movie added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_movie.html')

@app.route('/delete-movie',methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        
        query = "DELETE FROM movie WHERE title = %s"
        dbCode.execute_delete(query, (title))
        
        flash('Movie deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_movie.html')
    
@app.route('/update-movie', methods=['GET', 'POST'])
def update_movie():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        new_overview = request.form['new_overview']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Title to update:", title, "New Overview:", new_overview)
        
        flash('Movie updated successfully!', 'info') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('update_movie.html')

@app.route('/display-movies', methods=['GET', 'POST'])
def display_movies():
    search_term = request.args.get('search', '')
    display_field = request.args.get('field', 'title')
    
    # Only show movies if there's a search term
    if not search_term:
        movie_list = []
    else:
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
        elif display_field == 'budget':
            query += " ORDER BY budget DESC"
        elif display_field == 'vote_average':
            query += " ORDER BY vote_average DESC"
        elif display_field == 'vote_count':
            query += " ORDER BY vote_count DESC"
        else:  # default to title
            query += " ORDER BY title"
        
        movie_list = dbCode.execute_query(query, args)
    
    return render_template('display_movies.html', movies=movie_list, search_term=search_term, display_field=display_field)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
