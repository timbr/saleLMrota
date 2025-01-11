import datetime
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_bookings(meeting_date):
  # Get a list of bookings from the Data Table
  slots = app_tables.slots.search()
  num_slots = len(slots)
  bookings = app_tables.bookings.search(meeting_date=meeting_date)
  if len(bookings) == 0:
    for slot in slots:
      app_tables.bookings.add_row(meeting_date=meeting_date, slot_name=slot, created_timestamp=datetime.datetime.now())
    bookings = app_tables.bookings.search(meeting_date=meeting_date)
  return bookings

@anvil.server.callable
def get_bubblepeople(meeting_date, slot_name, capacity):
  # Get a list of bookings from the Data Table
  bubblepeople = app_tables.bubblepeople.search(meeting_date=meeting_date, slot_name=slot_name)
  if len(bubblepeople) == 0:
    for i in range(1, capacity):
      app_tables.bubblepeople.add_row(index=i, meeting_date=meeting_date, slot_name=slot_name, created_timestamp=datetime.datetime.now())
    bubblepeople = app_tables.bubblepeople.search(meeting_date=meeting_date, slot_name=slot_name)
  return bubblepeople

@anvil.server.callable
def add_booking(booking, booking_dict):
  # check that the booking given is really a row in the ‘bookings’ table
  if app_tables.bookings.has_row(booking):
    booking_dict['booked_timestamp'] = datetime.datetime.now()
    booking.update(**booking_dict)
  else:
    raise Exception("Booking does not exist")

@anvil.server.callable
def add_bubbleperson(meeting_date, slot_name, index, name):
  bubbleperson = app_tables.bubblepeople.search(meeting_date=meeting_date, slot_name=slot_name, index=index)[0]
  bubbleperson.update(name=name)

@anvil.server.callable
def clear_booking(booking):
  # check that the booking being deleted exists in the Data Table
  if app_tables.bookings.has_row(booking):
    # find the bubblepeople and delete them
    bubblepeople = app_tables.bubblepeople.search(meeting_date=booking['meeting_date'], slot_name=booking['slot_name']['slot_name'])
    for person in bubblepeople:
      person['name'] = None
    booking['booker_name'] = None
    booking['booker_phone'] = None
    booking['booker_email'] = None
  else:
    raise Exception("Booking does not exist")

@anvil.server.http_endpoint("/add_record", methods=["POST"])
def add_record(data):
    """Add a record to the database."""
    bookings = app_tables.rota_bookings_table.search(meeting_date=data['meeting_date'])
    if len(bookings) == 0:
        app_tables.rota_bookings_table.add_row(meeting_date=data['meeting_date'], door_person=data['door_person'])
    else:
        bookings[0]['door_person'] = data['door_person']
    app_tables.rota_bookings_table.add_row(meeting_date=data['meeting_date'], door_person=data['door_person'])
    return {"success": True}

@anvil.server.http_endpoint("/get_records", methods=["GET"])
def get_records():
    """Retrieve all records from the database."""
    bookings = app_tables.rota_bookings_table.search()
    return [{"meetingDate": row['meeting_date'], "doorPerson": row['door_person']} for row in bookings]