import numpy as np


class Neuron:
    def __init__(self):
        self.w = np.array([])               # an array with all the weights
        self.b = 0                          # a single value b, used to compute z
        self.Z = np.array([])               # an array of all the z values
        self.dw = np.array([])              # an array of the derivatives of the loss of w
        self.db = 0                         # the derivative of the loss of b
        self.alpha = 0.001
        self.trainings_mode = False
        self.m = 0                          # the number of training examples in the data set
        # self.m_test = 0                     # the number of test examples in the test set
        self.nX = 0                         # the number of input features
        self.input_var = np.array([])       # the training data set input
        # self.input_test = np.array([])      # the test data set input
        self.output_train = np.array([])    # the corresponding output for the training data set
        self.A = np.array([])               # the output of the neuron, predicted value
        self.predicament = np.array([])     # the predicted output for the test data set
        self.loss = np.array([])            # an array of the loss with the current weights
        self.cost = 0                       # the total cost with the current weights

    def normalize_data(self):
        # normalize the input data
        pass

    def initialize(self, data, mode='test', trainings_output=None, copy=False, learning_rate=None, bb=None, w_zeros=True):
        """_initialize all the values_"""
        try:
            # if the data set is not a numpy array throw an error
            if not isinstance(data, type(np.array([]))):
                print("ERROR@initialize(): the data set is not a numpy array")
                exit(1)

            # if the data set is not 2D throw an error
            elif isinstance(data, type(np.array([]))) and len(data.shape) is not 2:
                print("ERROR@initialize(): the data is not two dimensional")
                exit(1)
            else:
                # set the data set as input
                if copy is True:
                    self.input_var = data.copy()
                if copy is False:
                    self.input_var = data
                assert(len(self.input_var.shape) == 2)

                # store the dimensions of the data set
                self.nX = int(self.input_var.shape[0])
                self.m = int(self.input_var.shape[1])

                # Create an array with zeros which will store all the weights and one for the derivatives
                if w_zeros:
                    self.w = np.zeros((self.nX, 1))
                else:
                    self.w = np.random.rand(self.nX, 1)
                self.dw = np.zeros((self.nX, 1))
                assert(len(self.w.shape) == 2)
                assert(len(self.dw.shape) == 2)

                # assign learning rate to alpha
                if bb and isinstance(bb, type(1.)):
                    self.b = bb
                elif bb and not isinstance(bb, type(1)):
                    print("WARNING@initialize: b must be an int, and is now a", type(bb))

                # assign learning rate to alpha
                if learning_rate and isinstance(learning_rate, type(1)):
                    self.alpha = learning_rate
                elif learning_rate and not isinstance(learning_rate, type(1)):
                    print("WARNING@initialize: learning rate must be an int, and is now a", type(learning_rate))

                # either assign an output or not, depending on the mode
                if mode.lower() == 'train':
                    self.trainings_mode = True
                    # throw an error if the trainings output is not a numpy array
                    if isinstance(trainings_output, type(np.array([]))):

                        # throw an error if the trainings output is not 2D not x by 1
                        if len(trainings_output.shape) is not 2 or trainings_output.shape != (1, self.m):
                            print("ERROR@initialize: make sure the dimensions of the trainings output are correct \n"
                                  "     The current shape is: %s, the required shape is: (1, %s)"
                                  % (str(trainings_output.shape), str(self.m)))
                            exit(1)
                        else:
                            self.output_train = trainings_output.copy()
                            assert(len(self.output_train.shape) == 2)
                    else:
                        print("ERROR@initialize: the trainings output is not a numpy array")
                        exit(1)

                # Throw a warning is the data set is not 10 times bigger than the number of features
                if self.m / self.nX < 10.0:
                    print('WARNING@update_input(): '
                          'the training set is only %.2f times bigger than the number of input features'
                          % (self.m / self.nX))

        except TypeError as error_one:
            print('ERROR@update_input(): make sure you have entered all parameters')
            raise

    @staticmethod
    def activation_function(af_z):
        """_return the sigmoid of the input_"""
        sigmoid = 1 / (1 + np.exp(-af_z))
        return sigmoid

    def forward_propagation(self):
        """_compute Z = w.T dot X + b & compute A = the sigmoid of Z_"""
        self.Z = np.dot(self.w.T, self.input_var) + self.b
        self.A = self.activation_function(self.Z)

    def backward_propagation(self):
        """_compute the loss & compute dw & compute db_"""
        self.loss = np.dot(self.output_train, np.log(self.A).T) + np.dot((1 - self.output_train), np.log(1 - self.A).T)
        self.cost = np.sum(self.loss) / -self.m
        self.dw = np.dot(self.input_var, (self.A - self.output_train).T) / self.m
        self.db = np.sum(self.A - self.output_train) / self.m

    def update_weights(self):
        """_update the weights_"""
        self.w = self.w - self.alpha * self.dw
        self.b = self.b - self.alpha * self.db

    def return_prediction(self):
        self.predicament = self.A
        self.predicament = self.predicament * 100

        print('The predicament is:', self.predicament)
        print('the shape is:', self.predicament.shape)
        print("dw = " + str(self.dw))
        print("db = " + str(self.db))
        print("cost = " + str(self.cost))

    def fire(self):
        """_bring everything together in one function_"""
        self.forward_propagation()

        if self.trainings_mode:
            self.backward_propagation()
            self.update_weights()

if __name__ == '__main__':
    """(self, data, mode='test', trainings_output=None, copy=False, learning_rate=None, bb=None)"""

    N_One = Neuron()
    N_Two = Neuron()
    N_Three = Neuron()
    X = np.array([[1.,2.,-1.], [3.,4.,-3.2]])
    Y = np.array([[1,0,1]])
    b = 2.
    N_One.initialize(data=X, mode='train', trainings_output=Y, bb=b, w_zeros=True)
    N_Two.initialize(data=X, mode='train', trainings_output=Y, bb=b, w_zeros=True)
    N_One.fire()
    N_Two.fire()
    N_Three.initialize(data=np.array([np.squeeze(N_One.A), np.squeeze(N_Two.A)]), mode='train', trainings_output=Y, bb=b, w_zeros=True)
    N_Three.fire()
    print('Neuron One: ------')
    N_One.return_prediction()
    print('Neuron Two: ------')
    N_Two.return_prediction()
    print('Neuron Three: ------')
    N_Three.return_prediction()


"""
EXCESSIVE CODE:
            if isinstance(data, type(np.array([]))) and len(data.shape) is not 2:
                self.input_var = data.reshape(data.shape[0], -1).T
                print('The data parameter with shape %s has been reshaped to %s, and then assigned to the input_var variable'
                      % (str(data.shape), str(self.input_var.shape)))

            # if the data is 2D directly assign it to the input_var variable
            elif isinstance(data, type(np.array([]))) and len(data.shape) is 2:
                self.input_var = data
                print('The data with shape %s parameter has been directly assigned to the input_var variable'
                      % str(data.shape))

"""