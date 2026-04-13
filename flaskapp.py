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
        
        # lines added with help of VSCode's GitHub copilot
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
        
        # Get movie_id first
        movie_id = dbCode.get_movie_id_by_title(title)
        if not movie_id:
            flash('Movie not found with that title.', 'danger')
            return redirect(url_for('home'))
        
        # Delete related records first (due to foreign key constraints)
        dbCode.execute_delete("DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))
        dbCode.execute_delete("DELETE FROM movie_languages WHERE movie_id = %s", (movie_id,))
        
        # Now delete the movie
        dbCode.execute_delete("DELETE FROM movie WHERE movie_id = %s", (movie_id,))
        
        flash('Erasure attempted. Check to see if it is still there!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_movie.html')
    
# Function generated with help from VSCode's GitHubcopilot
@app.route('/update-movie', methods=['GET', 'POST'])
def update_movie():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        
        # Get movie_id first
        movie_id = dbCode.get_movie_id_by_title(title)
        if not movie_id:
            flash('Movie not found with that title.', 'danger')
            return redirect(url_for('home'))
        
        # Collect all optional fields that were provided (excluding genres and languages)
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
        if request.form.get('movie_status'):
            updates['movie_status'] = request.form['movie_status']
        
        # Handle genres separately
        if request.form.get('genres'):
            genre_names = [g.strip() for g in request.form['genres'].split(',') if g.strip()]
            dbCode.update_movie_genres(movie_id, genre_names)
        
        # Handle languages separately
        if request.form.get('languages'):
            language_names = [l.strip() for l in request.form['languages'].split(',') if l.strip()]
            dbCode.update_movie_languages(movie_id, language_names)
        
        # Only update movie table if at least one field was provided
        if updates:
            # Build dynamic UPDATE query
            set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
            query = f"UPDATE movie SET {set_clause} WHERE movie_id = %s"
            args = list(updates.values()) + [movie_id]
            
            dbCode.execute_update(query, tuple(args))
        
        flash('Movie updated successfully!', 'success')
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
        # Base query with joins for genres and languages
        # Display generated with help from VSCode's GitHub copilot
        query = """
        SELECT m.*,
               GROUP_CONCAT(DISTINCT g.genre_name ORDER BY g.genre_name) as genres,
               GROUP_CONCAT(DISTINCT l.language_name ORDER BY l.language_name) as languages
        FROM movie m
        LEFT JOIN movie_genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN genre g ON mg.genre_id = g.genre_id
        LEFT JOIN movie_languages ml ON m.movie_id = ml.movie_id
        LEFT JOIN language l ON ml.language_id = l.language_id
        """
        args = ()
        
        # Add search filter if search term provided
        if search_term:
            query += " WHERE m.title LIKE %s"
            args = ('%' + search_term + '%',)
        
        # Add GROUP BY
        query += " GROUP BY m.movie_id"
        
        # Add ordering based on selected field
        if display_field == 'overview':
            query += " ORDER BY m.overview"
        elif display_field == 'popularity':
            query += " ORDER BY m.popularity DESC"
        elif display_field == 'release_date':
            query += " ORDER BY m.release_date DESC"
        elif display_field == 'revenue':
            query += " ORDER BY m.revenue DESC"
        elif display_field == 'runtime':
            query += " ORDER BY m.runtime DESC"
        elif display_field == 'budget':
            query += " ORDER BY m.budget DESC"
        else:  # default to title
            query += " ORDER BY m.title"
        
        movie_list = dbCode.execute_query(query, args)
    
    return render_template('display_movies.html', movies=movie_list, search_term=search_term, display_field=display_field)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
