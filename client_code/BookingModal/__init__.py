from ._anvil_designer import BookingModalTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class BookingModal(BookingModalTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #print(properties)

    # Any code you write here will run when the form opens.
    #items = []
    #capacity = int(properties['capacity'])
    #print(capacity)
    #for i in range(1, capacity):
    #  entry = {'label_bubbleperson': f'Bubble person {i}'}
    #  items.append(entry)
    #self.bubblepeople_panel.items = items
    
    if properties['capacity'] == 1:
      self.bubblepeople_panel.visible = False
    else:
      self.bubblepeople_panel.items = anvil.server.call('get_bubblepeople',
                                                        capacity=properties['capacity'],
                                                        meeting_date=properties['meeting_date'],
                                                        slot_name=properties['slot_name'])
    
      
    