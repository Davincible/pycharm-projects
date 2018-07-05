"""
*  Created by David Brouwer
*  david.brouwer.99@gmail.com
*  GitHub: https://github.com/Davincible
*
*  seatingplans module, defining interactive airplane layouts which can be used for the seat selection in a plane.
*
"""

import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import *
from seats import BusinessClass_Seat, EconomyClass_Seat, ExtraLegRoom_Seat
from kivy.clock import mainthread, Clock


class PlaneLayoutBasis(ScrollView):
    plane_layout_source = StringProperty('')
    plane_layout = Image().texture
    seat_layout = ListProperty([{"seat-type": 'BusinessClass', 'columns': 7},
                                {"seat-type": 'EconomyClass', 'columns': 7},
                                {"seat-type": 'ExtraLegRoom', 'columns': 2},
                                {"seat-type": 'EconomyClass', 'columns': 16}])
    orientation = OptionProperty('vertical', options=['horizontal', 'vertical'])
    padding_amounts = ListProperty([0, 0, 0, 0])
    padding_ = ListProperty([0, 0, 0, 0])
    tex_coords_ = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])
    seat_layout_size = ListProperty([0, 0])
    seat_layout_size_hint = ListProperty([1, 1])
    parent_grid = ObjectProperty(None)
    seat_layout_one_pos = ListProperty([0, 0])
    seat_layout_two_pos = ListProperty([0, 0])
    layout_width = NumericProperty(0)
    layout_height = NumericProperty(0)

    def __init__(self, **kwargs):
        super(PlaneLayoutBasis, self).__init__(**kwargs)
        self.register_event_type('on_plane_layout_source')
        self.dispatch('on_plane_layout_source')
        self.bind(padding_amounts=self.calculate_paddings)
        self.bind(orientation=self.orient)
        self.bind(size=self.set_pos, orientation=self.set_pos)
        self.bind(size=self.orient)
        self.orient()
        self.calculate_paddings()
        # self.frames_ahead(self.calculate_paddings, 1)
        self.frames_ahead(self.place_seats, 1)
        # Clock.schedule_once(self.place_seats, 1)

    @mainthread
    def calculate_paddings(self, *args):
        if not self.padding_amounts.count(0):
            if self.orientation == 'horizontal':
                original_width, original_height = self.parent_grid.width, self.parent_grid.height
            else:
                original_width, original_height = self.parent_grid.height, self.parent_grid.width

            left = (self.padding_amounts[0] / self.plane_layout.width) * original_width
            top = (self.padding_amounts[1] / self.plane_layout.height) * original_height
            right = (self.padding_amounts[2] / self.plane_layout.width) * original_width
            bottom = (self.padding_amounts[3] / self.plane_layout.height) * original_height
            self.padding_ = [left, top, right, bottom] if self.orientation == 'horizontal' else [top, left, bottom, right]
            self.place_seats()


    @mainthread
    def set_pos(self, *args):
        self.seat_layout_one_pos = self.ids.center_layout.pos
        if self.orientation == 'horizontal':
            self.seat_layout_two_pos = [self.ids.center_layout.x,
                                        self.ids.center_layout.y + 0.578 * self.ids.center_layout.height]
        else:
            self.seat_layout_two_pos = [self.ids.center_layout.x + 0.578 * self.ids.center_layout.width,
                                        self.ids.center_layout.y]

    @mainthread
    def orient(self, *args):
        self.tex_coords_ = [0, 1, 1, 1, 1, 0, 0, 0] if self.orientation == 'horizontal' else [1, 1, 1, 0, 0, 0, 0, 1]
        self.calculate_paddings()
        if self.orientation == 'horizontal':
            if self.ids.parent_grid.width < self.ids.parent_grid.height:
                self.ids.parent_grid.width, self.ids.parent_grid.height = self.ids.parent_grid.height, self.ids.parent_grid.width
            self.seat_layout_size = [100, 0.422 * self.ids.center_layout.height]
            self.seat_layout_size_hint = [1, None]
        elif self.orientation == 'vertical':
            if self.ids.parent_grid.width > self.ids.parent_grid.height:
                self.ids.parent_grid.width, self.ids.parent_grid.height = self.ids.parent_grid.height, self.ids.parent_grid.width
            self.seat_layout_size = [0.422 * self.ids.center_layout.width, 100]
            self.seat_layout_size_hint = [None, 1]

    def on_plane_layout_source(self, *args):
        self.plane_layout = Image(source=self.plane_layout_source).texture

    @mainthread
    def frames_ahead(self, func, frames, *args, **kwargs):
        if frames > 1:
            frames -= 1
            self.frames_ahead(func, frames)
        else:
            func(*args, **kwargs)

    def create_seat_widget(self, seat_data):
        if seat_data['seat-type'] == 'BusinessClass':
            seat = BusinessClass_Seat()
            seat_length = (45 / self.plane_layout.width) * self.layout_width
            seat_width = (33 / self.plane_layout.height) * self.layout_height
        elif seat_data['seat-type'] == 'EconomyClass':
            seat = EconomyClass_Seat()
            seat_length = (45 / self.plane_layout.width) * self.layout_width
            seat_width = (33 / self.plane_layout.height) * self.layout_height
        elif seat_data['seat-type'] == 'ExtraLegRoom':
            seat = ExtraLegRoom_Seat()
            seat_length = (60 / self.plane_layout.width) * self.layout_width
            print("length of long seat", seat_length)
            seat_width = (33 / self.plane_layout.height) * self.layout_height
        return seat, seat_width, seat_length

    @mainthread
    def place_seats(self, *args):
        top = self.ids.top_seats
        bottom = self.ids.bottom_seats
        column_number = 1
        top.clear_widgets()
        bottom.clear_widgets()
        x_offset = 0

        self.layout_width = self.parent_grid.width if self.orientation == 'horizontal' else self.parent_grid.height
        self.layout_height = self.parent_grid.height if self.orientation == 'horizontal' else self.parent_grid.width
        first_seat_length = 0

        for seat_data in self.seat_layout:
            for column in range(column_number, seat_data['columns'] + column_number):
                for row in "ABC":
                    seat, seat_width, seat_length = self.create_seat_widget(seat_data)

                    if column_number is 1:
                        first_seat_length = seat_length

                    seat.seat_number = "{}{}".format(column, row)
                    seat.orientation = self.orientation
                    if row == 'A':
                        seat_width = (31 / self.plane_layout.height) * self.layout_height
                        seat.small = True
                        if self.orientation == 'horizontal':
                            seat.pos = [bottom.x + x_offset, bottom.y]
                        else:
                            seat.pos = [bottom.x, bottom.top - x_offset - seat_length]
                    if row == 'B':
                        seat_width = (33 / self.plane_layout.height) * self.layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [bottom.x + x_offset, bottom.y + (0.311 * bottom.height)]
                        else:
                            seat.pos = [bottom.x + (0.311 * bottom.width), bottom.top - x_offset - seat_length]
                    elif row == 'C':
                        seat_width = (33 / self.plane_layout.height) * self.layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [bottom.x + x_offset, bottom.y + (0.311 * bottom.height) + (0.322 * bottom.height)]
                        else:
                            seat.pos = [bottom.x + (0.311 * bottom.width) + (0.322 * bottom.width), bottom.top - x_offset - seat_length]
                    size = [seat_length, seat_width]

                    seat.size = size
                    bottom.add_widget(seat)

                for row in "DEF":
                    seat, seat_width, seat_length = self.create_seat_widget(seat_data)

                    if column_number is 1:
                        first_seat_length = seat_length

                    seat.seat_number = "{}{}".format(column, row)
                    seat.orientation = self.orientation
                    if row == 'D':
                        seat_width = (33 / self.plane_layout.height) * self.layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [top.x + x_offset, top.y]
                        else:
                            seat.pos = [top.x, top.top - x_offset - seat_length]
                    if row == 'E':
                        seat_width = (33 / self.plane_layout.height) * self.layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [top.x + x_offset, top.y + (0.311 * top.height)]
                        else:
                            seat.pos = [top.x + (0.311 * top.width), top.top - x_offset - seat_length]
                    elif row == 'F':
                        seat_width = (31 / self.plane_layout.height) * self.layout_height
                        seat.small = True
                        if self.orientation == 'horizontal':
                            seat.pos = [top.x + x_offset, top.y + (0.311 * top.height) + (0.322 * top.height)]
                        else:
                            seat.pos = [top.x + (0.311 * top.width) + (0.322 * top.width), top.top - x_offset - seat_length]

                    seat.size = [seat_length, seat_width]
                    top.add_widget(seat)

                x_offset += seat_length
            column_number += seat_data['columns']


class KL73B(PlaneLayoutBasis):
    plane_layout_source = StringProperty('resources/kl73b.jpg')


class KL739(PlaneLayoutBasis):
    plane_layout_source = StringProperty('resources/kl739.jpg')
    padding_amounts = ListProperty([540, 65, 478, 65])


class SeatingPlansMainLayout(FloatLayout):
    pass


class seatingplansApp(App):
    def build(self):
        return SeatingPlansMainLayout()


if __name__ == '__main__':
    seatingplansApp().run()
