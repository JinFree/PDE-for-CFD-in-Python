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
        self.T = np.random.randn(self.Gy, self.Gx)
        self.Tnew = np.random.randn(self.Gy, self.Gx)
        self.scheme = 'Jacobi'
        self.Scheme_name = "Error"
        self.Dirname = "Error"
        self.iter = 0

    def Scheme_Printer(self):
        if self.scheme == 'Jacobi':
            print("Solve Jacobi")
            self.Scheme_name = "Jacobi"
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
        self.dirname = dirname
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)  # 디렉토리가 존재하면 삭제하고 다시 계산# return # 디렉토리가 존재하면 덮어쓰기 #
        os.mkdir(dirname)

    def Para_Write(self):
        if self.Scheme_name == "PSOR":
            filename = "{0}/{1}, w = {2}, iter = {3}.csv".format(self.dirname, self.Scheme_name, self.w, self.iter)
        else:
            filename = "{0}/{1}, iter = {2}.csv".format(self.dirname, self.Scheme_name, self.iter)
        file = open(filename,'w')
        file.write("X,Y,Z,Temperature\n")
        for i in range(self.Gy):
            for j in range(self.Gx):
                data = "%3.3f,%3.3f,%3.3f,%3.3f\n"%(float(j*self.GridSize),float(i*self.GridSize),0.0,self.T[i][j])
                file.write(data)
        file.close()

    def get_w(self):
        prompt = """Input w, 1.0 ~ 1.9
Enter w: """
        print(prompt)
        self.w = float(input())
        if 1.0 < self.w < 1.9:
            return
        else:
            print("Wrong Input")
            self.get_w()

    def Initial_Condition(self):
        self.T = np.zeros((self.Gy, self.Gx))
        self.Tnew = np.zeros((self.Gy, self.Gx))

    def Boundary_Condition(self):
        for i in range(self.Gy):
            self.T[i][0] = 0
            self.Tnew[i][0] = 0
            self.T[i][self.Gx-1] = 0
            self.Tnew[i][self.Gx-1] = 0
        for i in range(self.Gx):
            self.T[self.Gy-1][i] = 0
            self.Tnew[self.Gy-1][i] = 0
            self.T[0][i] = self.T0
            self.Tnew[0][i] = self.T0

    def CalErr(self):
        error = 0
        for i in range(1, self.Gy-1):
            for j in range(1, self.Gx-1):
                error += abs(self.Tnew[i][j] - self.T[i][j])
        return error

    def Memcpy(self):
        self.T = self.Tnew.copy()

    def Jacobi(self):
        for i in range(1, self.Gy-1):
            for j in range(1, self.Gx-1):
                self.Tnew[i][j] = (self.T[i+1][j]+self.T[i-1][j]+self.T[i][j+1]+self.T[i][j-1])/4.0

    def Jacobi_Solver(self):
        self.iter = 0
        error = 1.0
        while error > self.Ermax:
            self.Jacobi()
            error = self.CalErr()
            self.Memcpy()
            self.iter += 1
            print("\rIteration = %d"%self.iter, end="")

    def PGS(self):
        for i in range(1, self.Gy-1):
            for j in range(1, self.Gx-1):
                self.Tnew[i][j] = (self.T[i+1][j]+self.Tnew[i-1][j]+self.T[i][j+1]+self.Tnew[i][j-1])/4.0

    def PGS_Solver(self):
        self.iter = 0
        error = 1.0
        while error > self.Ermax:
            self.PGS()
            error = self.CalErr()
            self.Memcpy()
            self.iter += 1
            print("\rIteration = %d"%self.iter, end="")

    def PSOR(self):
        for i in range(1, self.Gy-1):
            for j in range(1, self.Gx-1):
                self.Tnew[i][j] = (1.0 - self.w)*(self.T[i][j]) + self.w*(self.T[i+1][j]+self.Tnew[i-1][j]+self.T[i][j+1]+self.Tnew[i][j-1])/4.0

    def PSOR_Solver(self):
        self.iter = 0
        error = 1.0
        while error > self.Ermax:
            self.PSOR()
            error = self.CalErr()
            self.Memcpy()
            self.iter += 1
            print("\rIteration = %d"%self.iter, end="")

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
        self.Para_Write()
        print()

def main():
    ID = Elliptic()
    return ID

def help():
    prompt = """Compute function
    'Jacobi'
    'PGS'
    'PSOR'"""
    print(prompt)

PyCompute = Elliptic()
print("What Will you Compute?")
prompt = """
1: Jacobi
2: PGS
3: PSOR

Enter Number(1~3): """
ID = 5
I = 1
while I:
    if 0 < ID < 4:
        I = 0
    else:
        print(prompt)
        ID = int(input())
if ID == 1:
    PyCompute.Main('Jacobi')
if ID == 2:
    PyCompute.Main('PGS')
if ID == 3:
    PyCompute.Main('PSOR')