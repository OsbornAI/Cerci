import matrix

# When we abstract a tensor here we mean a multi dimensional object which can be fed into the others
# We should think about these in terms of layers rather than tensors, where they are layers stacked on top of each other
class Tensor:
    def validTensor(self):
        try:
            self.__tensor[0]
        except:
            self.__tensor = [self.__tensor]
        mSize = self.__tensor[0].size()
        for mat in self.__tensor:
            if (mat.size() != mSize): raise Exception("Matrices must all be of same size!")

    def __init__(self, matrices, dup=False):
        self.__tensor = matrices 
        self.validTensor()
        if (dup != False):
            for _ in range(dup-1):
                self.__tensor.append(matrices)

    def print(self):
        for mat in self.__tensor:
            mat.print()
            print()

    def pad(self, pad_up=0, pad_down=0, pad_right=0, pad_left=0, pad_val=lambda: 0):
        retArray = []
        for mat in self.__tensor:
            pd = mat.pad(pad_up=pad_up, pad_down=pad_down, pad_right=pad_right, pad_left=pad_left, pad_val=pad_val)
            retArray.append(pd)
        
        return Tensor(retArray)

    def applyFunc(self, func):
        retArray = []
        for mat in self.__tensor:
            fn = mat.applyFunc(func)
            retArray.append(fn)
        
        return Tensor(retArray)

    def returnTensor(self):
        return self.__tensor

    def size(self):
        matSize = self.__tensor[0].size()
        return matSize[0], matSize[1], len(self.__tensor)

    def cut(self, startRow, endRow, startCol, endCol):
        retArray = []
        for mat in self.__tensor:
            ct = mat.cut(startRow, endRow, startCol, endCol)
            retArray.append(ct)
        
        return Tensor(retArray)