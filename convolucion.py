import numpy as np

class Convolucion1D:
    def __init__(self, f, kernel):
        self.f = f
        self.kernel = kernel

    def step(self):
        """
            Invertimos el vector para hacer la convolución, de lo contrario
            sería correlación
        """
        kernel_aux = np.flip(self.kernel)
        res = np.zeros(self.f.shape[0] + kernel_aux.shape[0]-1, dtype=np.float64)

        """
            Redimensionamos la función para tener en cuenta los momentos iniciales
            y finales de la convolución
        """
        aux = np.pad(self.f, (kernel_aux.shape[0]-1, kernel_aux.shape[0]-1), 'constant')

        for i in range(res.shape[0]):
            res[i] = np.sum(aux[i:i+kernel_aux.shape[0]] * kernel_aux)

        return res

if __name__ == '__main__':

    f1 = np.zeros(8, dtype=np.float64)
    f1[7] = 1
    f2 = np.array([1.,2.,3.,2.,8.])

    """ 
    f1 = np.array([0,0,2,1,2,0,1,0,1,2])
    f2 = np.zeros(5, dtype=np.float64)
    f2[0] = 1
    """

    conv = Convolucion1D(f1, f2)
    print(conv.step())
