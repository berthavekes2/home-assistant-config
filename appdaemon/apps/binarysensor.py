import appdaemon.plugins.hass.hassapi as hass

class setvalueback(hass.Hass):

  def initialize(self):
    self.listen_state(self.set_back,self.args["entity"])

  def set_back(self, entity, attribute, old, new, kwargs):
    if new == self.args["listen_for"]:
      self.set_state(self.args["entity"],state = self.args["set_back_state"])