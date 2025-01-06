from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...BookingModal import BookingModal

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def form_refreshing_data_bindings(self, **event_args):
    """This method is called when refreshing_data_bindings is called"""
    self.label_slot_name.text = self.item['slot_name']['slot_name']
    
    capacity = self.item['slot_name']['slot_capacity']
    if int(capacity) > 1:
      self.label_slot_capacity.text = f"Max occupancy {capacity} people"
    else:
      self.label_slot_capacity.text = ''
      
    booked_by = self.item['booker_name']
    if booked_by is None:
      self.label_booked_by.text = "Free Slot"
      self.label_booked_by.foreground = "#4fe817"
      self.button_book.enabled = True
      self.button_edit.enabled = False
    else:
      self.label_booked_by.text = booked_by
      self.label_booked_by.foreground = "#8a19e6"
      self.button_book.enabled = False
      self.button_edit.enabled = True

  def button_book_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Initialise an empty dictionary to store the user inputs
    capacity=int(self.item['slot_name']['slot_capacity'])
    slot_name = self.item['slot_name']['slot_name']
    meeting_date = self.item['meeting_date']
    new_booking = {}
    # Open an alert displaying the 'Add_Booking' Form
    save_clicked = alert(
      content=BookingModal(item=new_booking, capacity=capacity, slot_name=slot_name, meeting_date=meeting_date),
      title=f"Add Booking for {self.item['slot_name']['slot_name']} on {self.item['meeting_date'].strftime('%-d %B %Y')}",
      large=True,
      buttons=[("Save", True), ("Cancel", False)],
    )
    if save_clicked:
      anvil.server.call('add_booking', self.item, new_booking)
    
    # Now refresh the page
      self.refresh_data_bindings()

  def button_edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Get the user to confirm if they wish to delete the booking
    # If they confirm, raise the 'x-delete-booking' event on the parent (which is the repeating_panel_1 on our Homepage)
    if confirm("This slot has been booked by {}. Would you like to cancel this booking?".format(self.item['booker_name'])):
      self.parent.raise_event('x-clear-booking', booking=self.item)


