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
        
        flash('Sacrifice attempted! Check to see if it worked.', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_movie.html')
    
# Function generated with help from VSCode's copilot
@app.route('/update-movie', methods=['GET', 'POST'])
def update_movie():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        
        # Collect all optional fields that were provided
        updates = {}
        if request.form.get('overview'):
            updates['overview'] = request.form['overview']
        if request.form.get('popularity'):
            updates['popularity'] = request.form['popularity']
        if request.form.get('release_date'):
            updates['release_date'] = request.form['release_date']
        if request.form.get('revenue'):
            updates['revenue'] = request.form['revenue']
        if request.form.get('runtime'):
            updates['runtime'] = request.form['runtime']
        if request.form.get('budget'):
            updates['budget'] = request.form['budget']
        if request.form.get('vote_average'):
            updates['vote_average'] = request.form['vote_average']
        if request.form.get('vote_count'):
            updates['vote_count'] = request.form['vote_count']
        if request.form.get('movie_status'):
            updates['movie_status'] = request.form['movie_status']
        
        # Only update if at least one field was provided
        if updates:
            # Build dynamic UPDATE query
            set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
            query = f"UPDATE movie SET {set_clause} WHERE title = %s"
            args = list(updates.values()) + [title]
            
            dbCode.execute_update(query, tuple(args))
            flash('Movie updated successfully!', 'info')
        else:
            flash('Please provide at least one field to update.', 'warning')
        
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
