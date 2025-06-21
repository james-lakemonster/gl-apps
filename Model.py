class Model:
   def __init__(self):
      self.states = {
         "angle": 0.0,
         "angle_dot": 90.0,
         "z": 5.0,
         "z_speed": 0.0,
         "z_motion_direction": 1.0,
         }

   def getStates(self):
      return self.states

   def setup(self):
      pass

   def update(self, dt, controls):
      states = self.states

      # integrate the states
      states['z'] += states['z_motion_direction'] * states['z_speed'] * dt;
      states['angle'] += states['angle_dot'] * dt
      states['z_speed'] += controls['force'] * 10.0 * dt
      states['angle_dot'] += controls['torque'] * 360.0 * dt

      # apply constraints (incase any states are out of bounds)

      # wrap the angle
      if states['angle'] > 360:
         states['angle'] -= 360
      if states['angle'] < 360:
         states['angle'] += 360

      # bounce off the near and far walls
      if states['z'] > 25.0:
         states['z'] = 25.0
         states['z_motion_direction'] = -1.0
      if states['z'] < 5.0:
         states['z'] = 5.0
         states['z_motion_direction'] = 1.0

      # do not admit backwards motion
      if states["z_speed"] < 0.0:
         states["z_speed"] = 0.0

      if states["angle_dot"] < 0.0:
         states["angle_dot"] = 0.0

