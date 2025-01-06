import datetime
from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..RoomPlanModal import RoomPlanModal

  
class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    today = datetime.date.today()
    self.next_sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )
    self.active_date = self.next_sunday
    self.refresh_bookings()
    self.repeating_panel_1.set_event_handler('x-clear-booking', self.clear_booking)

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
    if self.active_date == self.next_sunday:
      self.button_date_back.visible = False
    else:
      self.button_date_back.visible = True
    self.repeating_panel_1.items = anvil.server.call('get_bookings', self.active_date)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    link_clicked = alert(
      content=RoomPlanModal(),
      title="Room Plan showing seating positions",
      large=True,
      buttons=[("Back", True)],
    )

  def clear_booking(self, booking, **event_args):
    # clear the booking
    anvil.server.call('clear_booking', booking)
    self.refresh_bookings()
