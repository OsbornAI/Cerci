import matrix
from misc import applyActivationGradient

class FullyConnected:
    def __init__(self, weight_set, bias_set, activation_func):
        self.weights = weight_set
        self.bias = bias_set
        self.activation_func = activation_func

        self.pWeights = matrix.Matrix(dims=weight_set.size(), init=lambda: 0)
        self.pBias = matrix.Matrix(dims=bias_set.size(), init=lambda: 0)
        self.rmsWeights = matrix.Matrix(dims=weight_set.size(), init=lambda: 0)
        self.rmsBias = matrix.Matrix(dims=bias_set.size(), init=lambda: 0)
        self.iteration = 0

    def predict(self, inputs):
        multiplied = matrix.multiplyMatrices(self.weights, inputs)
        out = matrix.add(multiplied, self.bias)

        outCpy = out.clone()
        out = out.applyFunc(lambda x: self.activation_func(x, vals=outCpy)) 

        return out

    def train(self, input_set, predicted, errors_raw, optimizer, learn_rate=0.1):
        self.iteration += 1

        errors = applyActivationGradient(self.activation_func, errors_raw, predicted)

        inputTransposed = input_set.transpose()

        w_AdjustmentsRaw = matrix.multiplyMatrices(errors, inputTransposed)

        self.pWeights, self.rmsWeights, w_Adjustments = optimizer(self.pWeights, self.rmsWeights, w_AdjustmentsRaw, self.iteration)
        w_Adjustments = matrix.multiplyScalar(w_Adjustments, learn_rate)
        self.weights = matrix.subtract(self.weights, w_Adjustments)

        self.pBias, self.rmsBias, b_Adjustments = optimizer(self.pBias, self.rmsBias, errors, self.iteration)
        b_Adjustments = matrix.multiplyScalar(errors, learn_rate)
        self.bias = matrix.subtract(self.bias, b_Adjustments)

        transposeWeights = self.weights.transpose()
        h_Error = matrix.multiplyMatrices(transposeWeights, errors)

        return h_Error

    def returnNetwork(self):
        return self.weights, self.pWeights, self.rmsWeights, self.bias, self.pBias, self.rmsBias