from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path
import os

app = Flask(__name__)

def get_db_connection():

    db = Path(__file__).parent / "musicAL.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/albums")
def albums():
    conn = get_db_connection()     
    albums = conn.execute("SELECT * FROM albums").fetchall()            
    conn.close()                            
    return render_template("products.html", albums=albums)    


@app.route('/albums/<int:album_id>')
def album_detail(album_id):
    conn = sqlite3.connect('musicAL.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get the album details
    cur.execute("SELECT * FROM albums WHERE id = ?", (album_id,))
    album = cur.fetchone()

    # Get the additional album info from the 'details' table
    cur.execute("SELECT album_info FROM details WHERE album_id = ?", (album_id,))
    album_info = cur.fetchone()

    # Get all songs linked to this album
    cur.execute("SELECT * FROM allsongs WHERE album_id = ?", (album_id,))
    songs = cur.fetchall()

    conn.close()

    # Pass album_info along with album and songs to the template
    return render_template('album_detail.html', album=album, album_info=album_info, album_songs=songs)

@app.route("/singles")
def singles():
    conn = get_db_connection()     
    singles = conn.execute("SELECT * FROM singles").fetchall()            
    conn.close()                            
    return render_template("singlesh.html", singles=singles)  

@app.route("/singles/<int:single_id>")
def singles_detail(single_id):
    conn = get_db_connection()
    
    # Get the single details from the singles table
    single = conn.execute("SELECT * FROM singles WHERE id = ?", (single_id,)).fetchone()

    # Optionally, get additional info about the single from another table (if needed)
    # Assuming you have a table like 'single_details' or 'details' for single-related info
    single_info = conn.execute("SELECT single_info FROM sdetails WHERE single_id = ?", (single_id,)).fetchone()

    conn.close()
    
    # Pass both the single and single_info to the template
    return render_template("singles_detail.html", single=single, single_info=single_info)

@app.route("/create", methods=["GET", "POST"])
def createnew():
    if request.method == "POST":
        # Get the form data
        name = request.form["name"]
        releaseyear = request.form["releaseyear"]
        album_type = request.form["type"]
        songnum = request.form["songnum"] if album_type == "album" else 0  # For singles, set songnum to 0

        # Handle file upload for cover image
        coverimg = request.files["coverimg"]
        coverimg_filename = coverimg.filename
        coverimg.save(os.path.join("static/images", coverimg_filename))  # Save the image in static/images folder

        # Insert the new album or single into the database
        conn = get_db_connection()
        if album_type == "album":
            conn.execute("INSERT INTO albums (name, releaseyear, coverimg, songnum) VALUES (?, ?, ?, ?)",
                         (name, releaseyear, coverimg_filename, songnum))
        else:
            conn.execute("INSERT INTO singles (name, releaseyear, coverimg) VALUES (?, ?, ?)",
                         (name, releaseyear, coverimg_filename))

        conn.commit()
        conn.close()

        # Redirect to a page where you can view the new album or single (could be the list view)
        return redirect(url_for("singles"))  # Or 'albums' depending on what you want to show

    return render_template("createnew.html")

@app.route('/albums/delete/<int:album_id>', methods=['POST'])
def delete_album(album_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM albums WHERE id = ?", (album_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('albums'))


@app.route('/singles/delete/<int:single_id>', methods=['POST'])
def delete_single(single_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM singles WHERE id = ?", (single_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('singles'))

if __name__ == "__main__":
    app.run(debug=True)

