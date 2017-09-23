import numpy as np


class neuron():

    def __init__(self):
        self.input_var = np.array([])
        self.output_var = np.array([[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]])

    def print_input(self):
        print(self.input_var)

    def print_output(self):
        print(self.output_var)

    def return_input(self):
        return self.input_var

    def return_output(self):
        return self.output_var

    def set_input(self, new_input):
        self.input_var = new_input

    def set_output(self, new_output):
        self.output_var = new_output

neuron_one = neuron()
neuron_two = neuron()

neuron_one.set_output(np.random.rand(3, 5))

# neuron_two.input_var = neuron_one.output_var
neuron_two.set_input(neuron_one.return_output())


print("the output of neuron one is:\n", neuron_one.output_var)
print("the input of neuron two is:\n", neuron_two.input_var)
print('\n')

neuron_one.output_var[0, 0] = 5
neuron_one.output_var[0, 2] = 3

print("the output of neuron one is:\n", neuron_one.output_var)
print("the input of neuron two is:\n", neuron_two.input_var)
print('\n')
