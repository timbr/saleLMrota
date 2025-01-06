import datetime
from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

  
class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    today = datetime.date.today()
    self.next_sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )
    self.active_date = self.next_sunday
    self.refresh_bookings()

  def button_date_forward_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.active_date += datetime.timedelta(7)
    self.refresh_bookings()

  def button_date_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.active_date -= datetime.timedelta(7)
    self.refresh_bookings()

  def refresh_bookings(self):
    self.label_meeting_date.text = self.active_date.strftime("%A %-d %B %Y")
    bookings = app_tables.rota_bookings_table.search(meeting_date=self.active_date)
    if len(bookings) == 0:
      self.Flower_Person.text = ''
      self.TeaCoffee_Person.text = ''
      self.Door_Person.text = ''
    else:
      self.Flower_Person.text = bookings[0]['flowers_person']
      self.TeaCoffee_Person.text = bookings[0]['drinks_person']
      self.Door_Person.text = bookings[0]['door_person']

  def clear_booking(self, booking, **event_args):
    # clear the booking
    anvil.server.call('clear_booking', booking)
    self.refresh_bookings()

  def Flower_Person_change(self, **event_args):
    """This method is called when focus is lost from this text box"""
    bookings = app_tables.rota_bookings_table.search(meeting_date=self.active_date)
    if len(bookings) == 0:
        app_tables.rota_bookings_table.add_row(meeting_date=self.active_date, flowers_person=self.Flower_Person.text)
    else:
        bookings[0]['flowers_person'] = self.Flower_Person.text

  def TeaCoffee_Person_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    bookings = app_tables.rota_bookings_table.search(meeting_date=self.active_date)
    if len(bookings) == 0:
        app_tables.rota_bookings_table.add_row(meeting_date=self.active_date, drinks_person=self.TeaCoffee_Person.text)
    else:
        bookings[0]['drinks_person'] = self.TeaCoffee_Person.text

  def Door_Person_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    bookings = app_tables.rota_bookings_table.search(meeting_date=self.active_date)
    if len(bookings) == 0:
        app_tables.rota_bookings_table.add_row(meeting_date=self.active_date, door_person=self.Door_Person.text)
    else:
        bookings[0]['door_person'] = self.Door_Person.text

  def button_save_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.refresh_bookings()
