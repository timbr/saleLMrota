import datetime
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

today = datetime.date.today()
next_sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )
active_date = next_sunday

@anvil.server.http_endpoint("/add_record", enable_cors=True, methods=["POST"])
def add_record(**q):
    """Add a record to the database."""
    given_date = datetime.datetime.strptime(anvil.server.request.body_json['meeting_date'], "%d-%m-%Y").date()
    flowers_person = anvil.server.request.body_json['flowers_person']
    drinks_person = anvil.server.request.body_json['drinks_person']
    door_person = anvil.server.request.body_json['door_person']
    bookings = app_tables.rota_bookings_table.search(meeting_date=given_date)
    if len(bookings) == 0:
        app_tables.rota_bookings_table.add_row(meeting_date=given_date, flowers_person=flowers_person, drinks_person=drinks_person, door_person=door_person)
    else:
        bookings[0]['flowers_person'] = flowers_person
        bookings[0]['drinks_person'] = drinks_person
        bookings[0]['door_person'] = door_person
    r = anvil.server.HttpResponse()
    r.headers['access-control-allow-headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    r.status = 200
    r.body = {"success": True}
    return r

@anvil.server.http_endpoint("/get_records", enable_cors=True, methods=["GET"])
def get_records():
    """Retrieve all records from the database."""
    bookings = app_tables.rota_bookings_table.search(tables.order_by('meeting_date'), q.all_of(meeting_date=q.greater_than_or_equal_to(active_date)))[:4]
    return [{"meetingDate": row['meeting_date'].strftime("%d-%m-%Y"), "flowersPerson": row['flowers_person'], "drinksPerson": row['drinks_person'], "doorPerson": row['door_person']} for row in bookings]

@anvil.server.http_endpoint("/get_records/:start_date", enable_cors=True, methods=["GET"])
def get_records_from_start_date(start_date, **params):
    """Retrieve all records from the database."""
    first_date = datetime.datetime.strptime(start_date, "%d-%m-%Y").date()
    bookings = app_tables.rota_bookings_table.search(tables.order_by('meeting_date'), q.all_of(meeting_date=q.greater_than_or_equal_to(first_date)))[:4]
    return [{"meetingDate": row['meeting_date'].strftime("%d-%m-%Y"), "flowersPerson": row['flowers_person'], "drinksPerson": row['drinks_person'], "doorPerson": row['door_person']} for row in bookings]