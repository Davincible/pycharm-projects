"""
*  Created by David Brouwer
*  david.brouwer.99@gmail.com
*  GitHub: https://github.com/Davincible
*
*  seats module, defining the widgets of airplane seats.
*
"""

import kivy
kivy.require('1.10.0')
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import get_color_from_hex
from kivy.clock import mainthread, Clock
from kivy.lang import Builder
from kivy.properties import *
from kivy.app import App

Builder.load_string("""
#:import utils kivy.utils

<SeatsLayout>:
    BoxLayout:
        orientation: 'vertical'
        # size_hint: None, None
        # size: 500, 500
        pos_hint: {'center_x': .5, 'center_y': .5}

        EconomyClass_Seat:

        BusinessClass_Seat:
        
        ExtraLegRoom_Seat:


<BusinessClass_Seat>:
    seat_source: 'resources/KL_BUSINESS--EBC.png'
    seat_color_hex: '#001825'

    
<EconomyClass_Seat>
    seat_source: 'resources/seatmap-seat.png'
    seat_color_hex: '#00a1de'


<EmtpySpace>:
    size: [15, 33]


<ExtraLegRoom_Seat>:
    size_hint: None, None
    size: [60, 33]
       
    SeatBase:
        id: seating
        pos_hint: {'center_y': .5, 'right': 1}
        seat_number: root.seat_number
        seat_color_hex: '#d6b400'
        orientation: root.orientation
        small: root.small
        disabled: root.disabled
        on_size: print("seat:", args[1])


<SeatBase>:
    size_hint: None, None
    size: [45, 33]
    on_release: print(self.seat_number, self.size)

    canvas:
        Color:
            rgba: root.seat_color
        Rectangle:
            size: self.size
            pos: self.pos

        Color:
            rgba: [1, 1, 1, 1] if not root.disabled else [1, 1, 1, .5]
        Rectangle:
            size: self.size
            pos: self.pos
            texture: root.texture_
            tex_coords: root.texture_coords

    Label:
        text: root.seat_number
        pos_hint: root.label_orientation
        font_name: root.font
""")


class SeatBase(ButtonBehavior, FloatLayout):
    """the base class for any plane seat"""
    seat_source = StringProperty('')  # path to the source of the seat image
    texture_ = Image(source='resources/seatmap-seat.png').texture  # the background texture of the seat containing the image
    seat_size = ListProperty([45, 33])  # the size of the seat on the source image in pixels, this says nothing about the actual widget size
    small = BooleanProperty(False)  # if True; the width of the seat on the source image will be less
    seat_color = ListProperty([])  # seat color in rgba format
    seat_color_hex = StringProperty('#00a1de')  # opional, seat color in hex. Although the default color is set as hex.
    seat_number = StringProperty('2B')  # the seat number displayed on the seat
    font = StringProperty('resources/FRANKGO.ttf')  # font used for the seat label
    orientation = OptionProperty('horizontal', options=['horizontal', 'vertical'])  # the orientation the seat should be placed in
    texture_coords = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])  # the texture coordinates of the source image, defining which part of the source image should be used.
    label_orientation = DictProperty({'center_x': .45, 'center_y': .52})  # the position of the label relative to the seat
    disabled = BooleanProperty(False)  # if True; the seat will be disabled. E.g. if already booked.
    sched_text = None  # will call the clock to schedule the :meth: set_texture_size

    def __init__(self, **kwargs):
        super(SeatBase, self).__init__(**kwargs)
        self.sched_text = Clock.schedule_once(lambda dt: self.set_texture_size())
        self.bind(size=self.sched_text)
        self.bind(orientation=self.sched_text)
        self.bind(small=self.sched_text)
        self.register_event_type('on_seat_color_hex')
        self.register_event_type('on_seat_source')
        self.on_seat_color_hex()

    def on_seat_source(self, *args):
        self.texture_ = Image(source=self.seat_source).texture

    def on_seat_color_hex(self, obj=None, hex_color=None):
        # if a hex color is set, convert it to the rgba space
        self.seat_color = get_color_from_hex(hex_color if hex_color else self.seat_color_hex)

    def set_texture_size(self, *args):
        # set the texture coordinates
        if self.small:
            self.seat_size = [45, 31]
        else:
            self.seat_size = [45, 33]

        nx = (self.texture_.width - float(self.seat_size[0])) / self.texture_.width
        ny = (self.texture_.height - float(self.seat_size[1])) / (2 * self.texture_.height)
        nr = 1
        nt = 1 - ny
        if self.orientation == 'horizontal':
            self.texture_coords = [nx, ny, nr, ny, nr, nt, nx, nt]
            self.label_orientation = {'center_x': .45, 'center_y': .52}
            if self.width < self.height:
                self.width, self.height = self.height, self.width
        elif self.orientation == 'vertical':
            self.texture_coords = [nr, ny, nr, nt, nx, nt, nx, ny]
            self.label_orientation = {'center_x': .5, 'center_y': .52}
            if self.width > self.height:
                self.width, self.height = self.height, self.width


class EconomyClass_Seat(SeatBase):
    """the economy class seat"""
    pass


class BusinessClass_Seat(SeatBase):
    """the business class seat"""
    pass

class ExtraLegRoom_Seat(FloatLayout):
    """the seat with extra legroom"""
    default_size = ListProperty([60, 33])
    default_seat_size = ListProperty([45, 33])
    seat_number = StringProperty('2B')
    orientation = OptionProperty('horizontal', options=['horizontal', 'vertical'])
    small = BooleanProperty(False)
    disabled = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ExtraLegRoom_Seat, self).__init__(**kwargs)
        self.bind(size=self.update_seating_size)
        self.register_event_type('on_orientation')
        self.bind(size=self.on_orientation)
        self.bind(size=lambda x, y: print(y))

    @mainthread
    def on_orientation(self, *args):
        if (self.orientation == 'horizontal' and self.width < self.height) or \
                (self.orientation == 'vertical' and self.width > self.height):
            self.width, self.height = self.height, self.width

    # def on_small(self, *args):
    #     if self.orientation == 'horizontal';
    #         self.height =

    def update_seating_size(self, *args):
        if self.orientation == 'horizontal':
            x = (self.default_seat_size[0] / self.default_size[0]) * self.size[0]
            y = (self.default_seat_size[1] / self.default_size[1] * self.size[1])
        else:
            x = (self.default_seat_size[0] / self.default_size[0]) * self.size[1]
            y = (self.default_seat_size[1] / self.default_size[1] * self.size[0])

        print("x", x, "y", y)
        self.ids.seating.size = [x, y]


class SeatsLayout(FloatLayout):
    """the main layout used for testing purposed, not meant to be used in other modules"""
    def __init__(self, **kwargs):
        super(SeatsLayout, self).__init__(**kwargs)
        # Clock.schedule_once(self.second_init, 1)
        # self.add_widget(Economy_Seat(orientation='vertical', disabled=True))

    @mainthread
    def second_init(self, *args):
        self.add_widget(EconomyClass_Seat(orientation='vertical'))


class SeatsApp(App):
    def build(self):
        return SeatsLayout()


if __name__ == '__main__':
    SeatsApp().run()
