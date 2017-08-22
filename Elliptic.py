import math
import os
import shutil
import numpy as np
class Elliptic:
    enumerate(['Jacobi', 'PGS', 'PSOR'])
    def __init__(self):
        return

    def Initialize(self):
        self.Gx = 21
        self.Gy = 41
        self.GridSize = 0.05
        self.T0 = 100
        self.Ermax = 0.000001
        self.T = np.random.randn(self.Gx * self.Gy)
        self.Tnew = np.random.randn(self.Gx * self.Gy)
        self.scheme = 'Jacobi'
        self.Scheme_name = "Error"
        self.Dirname = "Error"
        self.iter = 0

    def Scheme_Printer(self):
        if self.scheme == 'Jacobi':
            print("Solve Jacobi")
            self.Scheme_name = "Explicit"
        elif self.scheme == 'PGS':
            print("Solve PGS")
            self.Scheme_name = "PGS"
        elif self.scheme == 'PSOR':
            print("Solve PSOR")
            self.Scheme_name = "PSOR"
            self.get_w()
        else:
            print("Wrong scheme input, solve Jacobi")
            self.scheme = 'Jacobi'
            self.Scheme_name = "Jacobi"

    def Dir_Write(self):
        if self.Scheme_name == "PSOR":
            dirname = "Elliptic, {0}, w={1}".format(self.Scheme_name, self.w)
        else:
            dirname = "Elliptic, {0}".format(self.Scheme_name)
        path = os.getcwd()
        dirname = os.path.join(path, dirname)
        if os.path.isdir(dirname):
            shutil.rmtree(dirname) # 디렉토리가 존재하면 삭제하고 다시 계산
        os.mkdir(dirname)
        self.dirname = dirname

    def get_w(self):
        prompt = """Input w, 1.0 ~ 1.9
        Enter w: """
        print(prompt)
        self.w = float(input())
        if 1.0 < self.w < 1.9:
            print("Wrong Input")
            self.get_w()

    def Initial_Condition(self):
        self.T = np.zeros(self.Gx * self.Gy)
        self.Tnew = np.zeros(self.Gx * self.Gy)

    def Boundary_Condition(self):
        for i in range(self.Gy):
            self.T[i*self.Gx] = 0
            self.Tnew[i * self.Gx] = 0
            self.T[(i+1)*self.Gx - 1] = 0
            self.Tnew[(i+1)*self.Gx - 1] = 0
        for i in range(self.Gx):
            self.T[self.Gx * (self.Gy - 1) + i] = 0
            self.Tnew[self.Gx * (self.Gy - 1) + i] = 0
            self.T[i] = self.T0
            self.Tnew[i] = self.T0

    def CalErr(self):
        error = 0
        for i in range(1, self.Gy-1):
            for j in range(1, self.Gx-1):
                error += abs(self.Tnew[i + j * self.Gx] - self.T[i + j * self.Gx])
        return error

    def Time_Marching(self):
        self.T = self.Tnew.copy()

    def Jacobi_Solver(self):
        return

    def PGS_Solver(self):
        return

    def PSOR_Solver(self):
        return

    def Main(self, scheme):
        self.Initialize()
        self.scheme = scheme
        self.Scheme_Printer()
        self.Initial_Condition()
        self.Boundary_Condition()
        self.Dir_Write()
        if scheme == 'Jacobi':
            self.Jacobi_Solver()
        elif scheme == 'PGS':
            self.PGS_Solver()
        elif scheme == 'PSOR':
            self.PSOR_Solver()



def main():
    ID = Elliptic()
    return ID

def help():
    prompt = """Compute function
    'Jacobi'
    'PGS'
    'PSOR'"""
    print(prompt)

a = main()
a.Initial_Condition()
a.Boundary_Condition()
print(a.T)
#a.Compute('Jacobi')