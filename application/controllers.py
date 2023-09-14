from flask import request, flash
from flask import render_template, redirect, url_for
from flask import current_app as app
from .models import *

# Return the landing page
@app.route("/")
def index():
    return render_template("index.html")

# Returns the page where you need to choose how are you loggining in.
@app.route("/auth")
def auth():
    return render_template("auth.html")

# --------------------------------ADMINS SECTION-----------------------------------

# Login Route for Admins
@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method=='GET':
        return render_template("login.html", title="admin")
    if request.method=='POST':
        username = request.form['username']
        password = request.form['pass']
    exists_check = db.session.query(Admin).filter_by(admin_username=username).first()
    if exists_check:
        flash('Welcome back to Bookify! You have been logged in successfully!')
        return redirect(url_for('admin_home', username=username))
    else:
        new_admin = Admin(admin_username=username, admin_password=password)
        db.session.add(new_admin)
        db.session.commit()
        flash('Welcome to Bookify! Your account has been created!')
        return redirect(url_for('admin_home', username=username))


# Home page for admins
@app.route("/admin-home", methods=['GET'])
def admin_home():
    return render_template('admin_home.html')



# ---------------------------USERS SECTION --------------------------------------

# Login Route for Users
@app.route("/login-user", methods=['GET', 'POST'])
def login_user():
    if request.method=='GET':
        return render_template("login.html", title="user")
    if request.method=='POST':
        username = request.form['username']
        password = request.form['pass']
    
    exist_check = db.session.query(User).filter_by(user_username=username).first()

    if exist_check:
        flash('Logged in successfully!')
        return redirect(url_for('user_home', username=username))
    else:
        new_user = User(user_username=username, user_password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Welcome to Bookify!')
        return redirect(url_for('user_home', username=username))


# Home page for user
@app.route("/user-home", methods=['GET'])
def user_home():
    venue = db.session.query(Venue).all()
    show = db.session.query(Show).all()
    return render_template("user_home.html", venue=venue, show=show)


# ---------------------------BOOKING SECTION --------------------------------------
@app.route('/book-show/<int:venue_id>')
def book_show(venue_id):
    vfs=db.session.query(Show_Venue).filter_by(venue_id=venue_id).all()
    shows = []
    for vf in vfs:
        show = db.session.query(Show).filter_by(show_id=vf.show_id).first()
        shows.append(show)
    return render_template('book_show.html', shows=shows, venue_id=venue_id)


@app.route('/book-tag/<show_tags>', methods=['GET'])
def book_tag(show_tags):
    show = db.session.query(Show).all()
    return render_template("book_based_on_tags.html", show=show, show_tags=show_tags)


@app.route('/book-venue/<int:show_id>')
def book_venue(show_id):
    vfs=db.session.query(Show_Venue).filter_by(show_id=show_id).all()
    venues = []
    for vf in vfs:
        venue = db.session.query(Venue).filter_by(venue_id=vf.venue_id).first()
        venues.append(venue)
    return render_template('book_venue.html', show_id=show_id, venues=venues)


@app.route('/book/<int:show_id>/<int:venue_id>', methods=['GET', 'POST'])
def book_show_venue(show_id, venue_id):
    venue =db.session.query(Venue).filter_by(venue_id=venue_id).first()
    show=db.session.query(Show).filter_by(show_id=show_id).first()
    if request.method == 'GET':
        return render_template("book_form.html", show=show, venue=venue)
    else:
        tickets = request.form['tickets']
        if int(tickets) <= int(venue.venue_capacity):
            venue.venue_capacity = int(venue.venue_capacity)-int(tickets)
            db.session.commit()
            return redirect(url_for('successful', show_id=show.show_id, venue_id=venue_id,tickets=tickets))
        else:
            flash('Oops there are not enough seats available!')
            return redirect(url_for('book_show_venue',show_id=show.show_id, venue_id=venue_id ))


@app.route('/success/<int:show_id>/<int:venue_id>/<int:tickets>')
def successful(show_id,venue_id,tickets):
    show=db.session.query(Show).filter_by(show_id=show_id).first()
    venue =db.session.query(Venue).filter_by(venue_id=venue_id).first()
    total_price = tickets*show.show_price
    return render_template('successful.html', show=show, venue=venue, tickets=tickets, total_price=total_price) 


# -------------------------------venue management--------------------

@app.route('/venue-dashboard', methods=['GET'])
def venue_dashboard():
    venue = db.session.query(Venue).all() 
    return render_template("venue_dashboard.html", venue=venue)

@app.route('/venue', methods=['GET'])
@app.route('/venue/<venue_id>', methods=['GET'])
def venue(venue_id=None):
    if not venue_id:
        return render_template('venue_form.html')
    else:
        venue_to_update = db.session.query(Venue).filter_by(venue_id=venue_id).first()
        return render_template('venue_form_to_update.html',venue_to_update=venue_to_update)
    
@app.route('/venue/<venue_id>/del')
def venue_del(venue_id):
    return render_template("confirm_venue_del.html",venue_id=venue_id)

@app.route('/venue/<venue_id>/confirm')
def venue_del_confirm(venue_id):
    venue_to_del = db.session.query(Venue).filter_by(venue_id = venue_id).first()
    db.session.delete(venue_to_del)
    association_to_del = db.session.query(Show_Venue).filter_by(venue_id = venue_id).all()
    for atd in association_to_del:
        db.session.delete(atd)
    db.session.commit()
    flash("Deleted Successfully!")
    return redirect(url_for('venue_dashboard'))



# -------------------------------shows management--------------------

@app.route('/show-dashboard')
def show_dashboard():
    show = db.session.query(Show).all()
    venue_list={}
    for s in show:
        vfs=db.session.query(Show_Venue).filter_by(show_id=s.show_id).all()
        for vf in vfs:
            v = db.session.query(Venue).filter_by(venue_id = vf.venue_id).first()
            venue_list.setdefault(vf.show_id, []).append(v.venue_name)    
    return render_template("show_dashboard.html", show=show, venue_list=venue_list)

@app.route('/show', methods=['GET'])
@app.route('/show/<show_id>', methods=['GET'])
def show(show_id=None):
    all_venue = db.session.query(Venue).all() 
    if not show_id:
        return render_template('show_form.html', all_venue=all_venue)
    else:
        show_to_update = db.session.query(Show).filter_by(show_id=show_id).first()
        return render_template('show_form_to_update.html',show_to_update=show_to_update, all_venue=all_venue)
    

@app.route('/show/<show_id>/del')
def show_del(show_id):
    return render_template("confirm_show_del.html",show_id=show_id)

@app.route('/show/<show_id>/confirm')
def show_del_confirm(show_id):
    show_to_del = db.session.query(Show).filter_by(show_id = show_id).first()
    db.session.delete(show_to_del)
    association_to_del = db.session.query(Show_Venue).filter_by(show_id = show_id).all()
    for atd in association_to_del:
        db.session.delete(atd)
    db.session.commit()
    flash("Deleted Successfully!")
    return redirect(url_for('show_dashboard'))
