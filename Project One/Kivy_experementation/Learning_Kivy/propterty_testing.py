import kivy
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget


class testClass(Widget): # every widget class has the eventdispatcher methods
    a = NumericProperty(0)
    number1 = NumericProperty(None)
    number2 = NumericProperty(None)


def callback(obj, value):  ## two arguments must be given.
    print("The call back has been activated")


ins = testClass()
ins.bind(a=callback)  # no brackets are used, bind a property to a function
ins.bind(number1=ins.setter('number2'))  # bind two properties together, number two will change if number one changes

ins.a = 5
print("number one before:", ins.number1)
print("number two before:", ins.number2)
ins.number1 = 666
print("number one after:", ins.number1)
print("number two after:", ins.number2)
ins.number2 = 444
print("number one after change 2:", ins.number1)  # number one does not change if number two changes
print("number two after change 2:", ins.number2)

ins.bind(number2=ins.setter('number1')) # binding number2 to number1, so that #1 changes when #2 changes
ins.number2 = 123
print("number one after binding 2 to 1:", ins.number1)
print("number two after binding 2 to 1:", ins.number2)

ins.number1 = 666
print("number one after:", ins.number1) # now number1 & number2 are bound int both directions
print("number two after:", ins.number2)

