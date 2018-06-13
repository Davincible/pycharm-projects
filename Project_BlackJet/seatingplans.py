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
from seats import BusinessClass_Seat, EconomyClass_Seat
from kivy.clock import mainthread, Clock


class PlaneLayoutBasis(ScrollView):
    plane_layout_source = StringProperty('')
    plane_layout = Image().texture
    seat_layout = ListProperty([{"seat-type": 'BusinessClass', 'columns': 7}, {"seat-type": 'EconomyClass', 'columns': 7}])
    orientation = OptionProperty('vertical', options=['horizontal', 'vertical'])
    padding_amounts = ListProperty([0, 0, 0, 0])
    padding_ = ListProperty([0, 0, 0, 0])
    tex_coords_ = ListProperty([0, 0, 0, 0, 0, 0, 0, 0])
    seat_layout_size = ListProperty([0, 0])
    seat_layout_size_hint = ListProperty([1, 1])
    parent_grid = ObjectProperty(None)
    seat_layout_one_pos = ListProperty([0, 0])
    seat_layout_two_pos = ListProperty([0, 0])

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

    @mainthread
    def place_seats(self, *args):
        top = self.ids.top_seats
        bottom = self.ids.bottom_seats
        column_number = 1
        top.clear_widgets()
        bottom.clear_widgets()

        for seat_data in self.seat_layout:
            for column in range(column_number, seat_data['columns'] + column_number):
                layout_width = self.parent_grid.width if self.orientation == 'horizontal' else self.parent_grid.height
                layout_height = self.parent_grid.height if self.orientation == 'horizontal' else self.parent_grid.width
                seat_length = (45 / self.plane_layout.width) * layout_width
                seat_width = (33 / self.plane_layout.height) * layout_height
                x_offset = seat_length * (column - 1)

                for row in "ABC":
                    if seat_data['seat-type'] == 'BusinessClass':
                        seat = BusinessClass_Seat()
                    elif seat_data['seat-type'] == 'EconomyClass':
                        seat = EconomyClass_Seat()

                    seat.seat_number = "{}{}".format(column, row)
                    seat.orientation = self.orientation
                    size = [seat_length, seat_width]
                    if row == 'A':
                        seat_width = (31 / self.plane_layout.height) * layout_height
                        size = [seat_length, seat_width]
                        seat.small = True
                        if self.orientation == 'horizontal':
                            seat.pos = [bottom.x + x_offset, bottom.y]
                        else:
                            seat.pos = [bottom.x, bottom.top - (seat_length * column)]
                    if row == 'B':
                        seat_width = (33 / self.plane_layout.height) * layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [bottom.x + x_offset, bottom.y + (0.311 * bottom.height)]
                        else:
                            seat.pos = [bottom.x + (0.311 * bottom.width), bottom.top - (seat_length * column)]
                    elif row == 'C':
                        seat_width = (33 / self.plane_layout.height) * layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [bottom.x + x_offset, bottom.y + (0.311 * bottom.height) + (0.322 * bottom.height)]
                        else:
                            seat.pos = [bottom.x + (0.311 * bottom.width) + (0.322 * bottom.width), bottom.top - (seat_length * column)]

                    seat.size = size
                    bottom.add_widget(seat)

                for row in "DEF":
                    if seat_data['seat-type'] == 'BusinessClass':
                        seat = BusinessClass_Seat()
                    elif seat_data['seat-type'] == 'EconomyClass':
                        seat = EconomyClass_Seat()

                    seat.seat_number = "{}{}".format(column, row)
                    seat.orientation = self.orientation
                    if row == 'D':
                        seat_width = (33 / self.plane_layout.height) * layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [top.x + x_offset, top.y]
                        else:
                            seat.pos = [top.x, top.top - (seat_length * column)]
                    if row == 'E':
                        seat_width = (33 / self.plane_layout.height) * layout_height
                        if self.orientation == 'horizontal':
                            seat.pos = [top.x + x_offset, top.y + (0.311 * top.height)]
                        else:
                            seat.pos = [top.x + (0.311 * top.width), top.top - (seat_length * column)]
                    elif row == 'F':
                        seat_width = (31 / self.plane_layout.height) * layout_height
                        seat.small = True
                        if self.orientation == 'horizontal':
                            seat.pos = [top.x + x_offset, top.y + (0.311 * top.height) + (0.322 * top.height)]
                        else:
                            seat.pos = [top.x + (0.311 * top.width) + (0.322 * top.width), top.top - (seat_length * column)]

                    seat.size = [seat_length, seat_width]
                    top.add_widget(seat)
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
