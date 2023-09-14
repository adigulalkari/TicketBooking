from flask import request,flash
from flask_restful import Resource, fields,marshal_with,reqparse
from .database import db
from .models import Venue, Show, Show_Venue

# serializing the data into json format to use it as a print statement on the terminal
resource_fields_venue = {
    "venue_id": fields.Integer,
    "venue_name": fields.String,
    "venue_place": fields.String,
    "venue_capacity": fields.Integer
}

resource_fields_show ={
    "show_id": fields.Integer,
    "show_name": fields.String,
    "show_rating": fields.Float,
    "show_tags": fields.String,
    "show_price": fields.Integer
}

# This data is coming from the request_payload. Which is the extra data we need to send
# with the url request. In the below lines we are describing the nature of the payload.
venue_put_args = reqparse.RequestParser()
venue_put_args.add_argument("venue_name", type=str, help='Name needed!')
venue_put_args.add_argument("venue_place", type=str, help='Place needed!')
venue_put_args.add_argument("venue_capacity", type=int, help='Capacity needed!')


# VenueAPI works perfectly when tested against a python
# file test.py in the AppDev1 folder.
# the post method is wroking and data is being posted into the database
class VenueAPI(Resource):
    # get venues
    # def get(self):
    #     return render_template("venue_form.html"), 200, {'Content-Type': 'text/html'}

    # Post to the database
    @marshal_with(resource_fields_venue)
    def post(self):
        data = request.get_json()
        new_venue = Venue(venue_name=data['venue_name'], venue_place=data['venue_place'],
                        venue_capacity=data['venue_capacity'])
        db.session.add(new_venue)
        db.session.commit()
        flash('Successfully added!')
        return new_venue,201

    # update the venue
    @marshal_with(resource_fields_venue)
    def put(self):
        data = request.get_json()
        venue_to_update = db.session.query(Venue).filter(Venue.venue_id == data['venue_id']).first()
        venue_to_update.venue_name = data['venue_name']
        venue_to_update.venue_place = data['venue_place']
        venue_to_update.venue_capacity = data['venue_capacity']
        db.session.commit()
        return venue_to_update




# Only post and put work through the api.

class ShowAPI(Resource):
    # def get(self):
    #     pass

    @marshal_with(resource_fields_show)
    def post(self):
        data = request.get_json()
        ven_size = len(data['venue_name'])
        new_show = Show(show_name=data['show_name'], show_rating=data['show_rating'],
                        show_tags=data['show_tags'],show_price=data['show_price'])
        db.session.add(new_show)
        db.session.commit()
        flash('Successfully added!')
        last_entry = Show.query.order_by(Show.show_id.desc()).first()
        for i in range(ven_size):
            ven_to_create_relation = db.session.query(Venue).filter(Venue.venue_name==data['venue_name'][i]).first()
            new_relationship = Show_Venue(show_id = last_entry.show_id, venue_id= ven_to_create_relation.venue_id)
            db.session.add(new_relationship)
            db.session.commit()
        return new_show,201

    @marshal_with(resource_fields_show)
    def put(self):
        data = request.get_json()
        show_to_update = db.session.query(Show).filter(Show.show_id == data['show_id']).first()
        # Updating the show table
        show_to_update.show_name = data['show_name']
        show_to_update.show_rating = data['show_rating']
        show_to_update.show_tags = data['show_tags']
        show_to_update.show_price = data['show_price']
        db.session.commit()
        
        # Deleting the already existing records and then posting the updated ones
        show_to_del_in_rel_table = db.session.query(Show_Venue).filter(Show_Venue.show_id == data['show_id']).all()
        for instance in show_to_del_in_rel_table:
            db.session.delete(instance)
        db.session.commit()
        # Updating the association table
        for vp in data['venue_name']:
            ven_to_update_relation = db.session.query(Venue).filter(Venue.venue_name==vp).first()
            new_rel = Show_Venue(show_id=data['show_id'], venue_id=ven_to_update_relation.venue_id )
            db.session.add(new_rel)
            db.session.commit()
        
        return show_to_update