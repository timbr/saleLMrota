from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def text_box_bubbleperson_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    anvil.server.call('add_bubbleperson',
                       meeting_date=self.item['meeting_date'],
                       slot_name=self.item['slot_name'],
                       index=self.item['index'],
                       name=self.text_box_bubbleperson.text)
    



