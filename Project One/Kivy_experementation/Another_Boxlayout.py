import kivy
kivy.require('1.9.1')

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock, ClockBaseBehavior
from kivy.properties import ObjectProperty


class Box_widget(BoxLayout):
    text_one = ObjectProperty(None)
    button_one = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Box_widget, self).__init__(**kwargs)
        self.ids['text_one'].bind(text=self.something_happened)

    def get_idss(self, value):
        for item in self.ids:
            print('Item number: %s' % (str(item)))

        print(self.ids)

    def something_happened(self, *args):
        print('OHJOO SOMETHING HAPPENED')

    def on_touch_down(self, touch):
        print('touch down profile', touch.is_touch)
        if self.ids['button_one'].collide_point(*touch.pos):
                print("COLIDED WITH BUTTON ONE")

        if touch.is_double_tap and not touch.is_triple_tap:
            print('DOUBLE TAP')

        if touch.is_triple_tap:
            print('TRIPPLE TAP')
        return super(Box_widget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        print('touch move profile', touch.profile)
        return super(Box_widget, self).on_touch_move(touch)

    def print_istouch(self, *args):
        print(self.touch.is_touch)


def get_timestuff(*args):
    print("Avergae fps:", ClockBaseBehavior.get_fps(Clock))
    print("Time passed since boot:", ClockBaseBehavior.get_boottime(Clock))
    print('THE CURRENT TIME IS:', ClockBaseBehavior.get_time(Clock))


class AnotherBoxlayoutApp(App):

    def build(self):
        instance = Box_widget()
        # event1 = Clock.schedule_once(instance.get_idss, 4)
        # event2 = Clock.schedule_interval(get_timestuff, 1.5)
        # event3 = Clock.schedule_interval(instance.print_istouch, 4)
        return instance


if __name__ == '__main__':
    AnotherBoxlayoutApp().run()