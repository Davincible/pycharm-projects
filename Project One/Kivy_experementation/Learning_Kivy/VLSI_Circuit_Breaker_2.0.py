"""
    Made by: David Brouwer
    Author email address: david.brouwer.99@gmail.com
    Author GitHub: https://github.com/Davincible

    This is basis of a component for a bigger project I'm creating.

    Data of comment: 28th November, 2017
"""

import kivy
kivy.require('1.10.0')

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty, ReferenceListProperty, BooleanProperty
from kivy.vector import Vector
from kivy.utils import platform, get_color_from_hex
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.app import App
from kivy.base import Builder

from colorsys import rgb_to_hsv
from time import time


class BaseLayoutClass(FloatLayout):
    pass


class CircuitBreakerBaseClass(Image):
    standard_vel = 2  # the standard velocity
    collided = BooleanProperty(False)  # another way to check if collision has occured besides the return value of the collision function
    wirehead = ObjectProperty(None)
    levels = 6  # the number of levels the game has
    current_level = 1
    current_level_source = StringProperty('')
    game_size = ListProperty([0, 0])

    #  background source for each level
    base_levels = ['VLSI-Circuit-Breaker-2.0-Level_{}.png'.format(level) for level in range(1, levels + 1)]

    #  properties for each game level
    level_properties = {1: {'x_start': 70, 'y_start': 168, 'direction': 'right', 'speed_divider': 570},
                        2: {'x_start': 65, 'y_start': 120, 'direction': 'right', 'speed_divider': 535},
                        3: {'x_start': 65, 'y_start': 75, 'direction': 'right', 'speed_divider': 500},
                        4: {'x_start': 120, 'y_start': 70, 'direction': 'up', 'speed_divider': 450},
                        5: {'x_start': 95, 'y_start': 765, 'direction': 'down', 'speed_divider': 400},
                        6: {'x_start': 75, 'y_start': 765, 'direction': 'down', 'speed_divider': 380}}

    border_threshold = .265  # threshold for the border detection, done on the V value of the HSV color
    highest = 0  # highest value (HSV color)
    dt_update = []

    def __init__(self, **kwargs):
        super(CircuitBreakerBaseClass, self).__init__(**kwargs)
        self.current_level_source = self.base_levels[self.current_level - 1]
        Clock.schedule_once(lambda dt: self.parent.bind(size=self.update_game_size))
        Clock.schedule_once(self.update_game_size)
        Clock.schedule_once(self.start_game, 5)


    def start_game(self, dt, level=None):
        """Start the Game"""
        #  clear reset line
        self.wirehead.line_points = []
        self.wirehead.index = 0

        #  set level source and velocity
        self.current_level = level if level else self.current_level
        self.standard_vel = self.width / self.level_properties[self.current_level]['speed_divider']
        self.current_level_source = self.base_levels[self.current_level - 1]

        #  set moving direction
        if self.level_properties[self.current_level]['direction'] == 'right':
            velocity = (self.standard_vel, 0)
        elif self.level_properties[self.current_level]['direction'] == 'up':
            velocity = (0, self.standard_vel)
        elif self.level_properties[self.current_level]['direction'] == 'down':
            velocity = (0, -self.standard_vel)
        elif self.level_properties[self.current_level]['direction'] == 'left':
            velocity = (-self.standard_vel, 0)

        #  serve the wirehead
        self.serve_wirehead(vel=velocity)

        #  start the game - schedule the updates
        Clock.schedule_interval(self.update_wirehead, 1 / 60)

    def update_wirehead(self, dt=None, *args):
        """Move the wire with a set interval and velocity"""
        #  for timing purposes
        self.dt_update.append(dt)

        #  move the wirehead with the set velocity
        self.wirehead.move()

        #  check if the new position of the wire collides with the circuit board boundaries.
        if self.hit_border(*self.wirehead.center):
            if self.hit_border(*self.wirehead.center) == 2:
                self.current_level = self.current_level + 1 if self.current_level + 1 in self.level_properties.keys() else self.current_level
            Clock.schedule_once(self.start_game, .5)
            return False

    def serve_wirehead(self, vel=(2, 0)):
        """Initiate the wire"""
        #  update the starting point of the wire depending on the current level
        self.update_starting_point()

        #  assign the passed velocity parameter to the wire velocity
        self.wirehead.velocity = vel

        #  make the wire visible, this triggers the bound color attribute of the wire - as seen in the kv file
        App.get_running_app().wire_visible = True

    def update_game_size(self, *args):
        """Update the size of the circuit board according to the size of the parent widget"""
        try:
            #  update the gameboard size according to the screen size
            width = min(self.parent.width, self.texture_size[0])
            height = min(self.parent.height, self.texture_size[1])
            x = width if ((self.texture_size[1] * width) / self.texture_size[0]) <= height else (self.texture_size[0] * height) / self.texture_size[1]
            y = (self.texture_size[1] * x) / self.texture_size[0] if ((self.texture_size[1] * x) / self.texture_size[0]) <= height else height
            self.size = [x, y]

            #  update the wirehead according to the gameboard size
            self.wirehead.size = (self.width / 60, self.width / 60)

            #  update the velocity according to the gameboard size
            velocity = self.width / self.level_properties[self.current_level]['speed_divider']
            self.standard_vel = velocity
            new_velocity = [0, 0]
            if self.wirehead.velocity[0] < 0:
                new_velocity[0] = -velocity
            elif self.wirehead.velocity[0] > 0:
                new_velocity[0] = velocity

            if self.wirehead.velocity[1] < 0:
                new_velocity[1] = -velocity
            elif self.wirehead.velocity[1] > 0:
                new_velocity[1] = velocity

            self.wirehead.velocity = new_velocity
        except:
            pass

    def hit_border(self, x, y):
        """Collision detection"""
        collided_with_wire = False  # flag to check if the wire collided with itself
        line_points = self.wirehead.line_points

        #  check if the wire collided with itself, not working as of now
        if x in line_points and y == line_points[line_points.index(x) + 1]:
            collided_with_wire = True
            # print(self.wirehead.)

        #  get the pixel value for the passed coordinate in the parameters
        try:
            x_ = ((x - self.x) / self.width) * self.texture_size[0]
            y_ = ((self.height - (y - self.y)) / self.height) * self.texture_size[1]
            pixel_color = self._coreimage.read_pixel(x_, y_)
        #  if the coordinate is not inside the background image, set pixel color values to zero
        except:
            pixel_color = [0, 0, 0, 0]

        #  convert the color value to HSV
        pixel_hsv = rgb_to_hsv(*pixel_color[:-1])

        #  if the V (value) is higher than the set threshold, collision occurred
        if pixel_hsv[-1] > self.border_threshold or collided_with_wire or pixel_hsv == (0, 0, 0):
            self.collided = True
            #  check for collision with gray finish block
            if pixel_hsv[1] < .2 and pixel_hsv[1] > 0:
                return 2  # return 2 if collided with finish block, return 1 if collided with border
            return 1
        else:
            #  track highest value for debug purposes
            if pixel_hsv[-1] > self.highest:
                self.highest = pixel_hsv[-1]
            self.collided = False
            return 0

    def update_starting_point(self, *args):
        """Calculate the starting point of the wire for the current level"""
        x = self.x + self.level_properties[self.current_level]['x_start'] * (self.width / self.texture_size[0]) - 0.5 * self.wirehead.width
        y = self.y + self.level_properties[self.current_level]['y_start'] * (self.height / self.texture_size[1]) - 0.5 * self.wirehead.width
        self.wirehead.pos = [x, y]


class WireHead(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    line_points = ListProperty([])  # list with all the coordinates for the wire
    dt_move = []
    index = 0

    def __init__(self, **kwargs):
        super(WireHead, self).__init__(**kwargs)

    def move(self):
        """Move the wirehead with the set velocity, and grow the wire"""
        start = time()
        #  move the wirehead
        self.pos = Vector(*self.velocity) + self.pos

        #  add the current position of the wirehead to the wire
        if self.pos != (0, 0) and self.index % 3 == 0:
            try:
                self.line_points += [self.x + self.width/2, self.y + self.height/2 + 0.01]
            except TypeError:
                pass

        self.index += 1
        end = time()
        self.dt_move.append(end - start)  # time tracking for debug purposes


Builder.load_file('VLSI_Circuit_Breaker_2.0.kv')


class VLSI_Circuit_Breaker_2App(App):
    title = 'VLSI_Circuit_Breaker_2.0'
    wirehead = ObjectProperty(None)
    wire_color = get_color_from_hex('47f597')[:-1] + [.8]
    wire_visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(VLSI_Circuit_Breaker_2App, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_keyboard)
        Clock.schedule_once(self.get_wirehead)

    def get_wirehead(self, *args):
        """Create reference to the wirehead object"""
        self.wirehead = self.root.ids.WireHead_

    def on_keyboard(self, window, key, *args):
        """Keyboard handler, capture arrow keys"""
        standard_vel = self.root.ids.CircuitBreakerBase.standard_vel
        if key == 273:
            self.wirehead.velocity = 0, standard_vel
        elif key == 274:
            self.wirehead.velocity = 0, -standard_vel
        elif key == 275:
            self.wirehead.velocity = standard_vel, 0
        elif key == 276:
            self.wirehead.velocity = -standard_vel, 0
        else:
            #  print key if not captured
            print(key)

    def on_stop(self):
        """print out debug information on closure of program"""
        dt_move = self.root.ids.WireHead_.dt_move
        dt_update = self.root.ids.CircuitBreakerBase.dt_update

        print("dt_update:", min(dt_update), max(dt_update))
        print("dt_move:", min(dt_move), max(dt_move))

    def build(self):
        if platform != 'android':
            Window.size = (394, 700)

        return BaseLayoutClass()


if __name__ == '__main__':
    VLSI_Circuit_Breaker_2App().run()
