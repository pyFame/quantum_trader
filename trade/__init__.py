from postion import  Position

def position(hedge=True):
  client.futures_change_position_mode(dualSidePosition = hedge)
  return client.futures_get_position_mode()

