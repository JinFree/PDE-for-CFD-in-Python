from __future__ import print_function
import math
import os
import shutil
import numpy as np
class Cavity:
    def __init__(self):
        self.ReN = 100
        self.Grid = 129
        self.Scheme_name = "Error"
        self.dx = 1.0 / float(self.Grid-1)
        self.dt = 0.0005
        self.U0 = 1.0
        self.Ermax = 0.000001
        self.U = np.random.randn(self.Grid, self.Grid)
        self.V = np.random.randn(self.Grid, self.Grid)
        self.W = np.random.randn(self.Grid, self.Grid)
        self.Wnew = np.random.randn(self.Grid, self.Grid)
        self.Psi = np.random.randn(self.Grid, self.Grid)
        self.Psinew = np.random.randn(self.Grid, self.Grid)
        self.StreamError = 1.0
        self.VorticityError = 1.0
        self.iter = 0
        self.dirname = "Error"
        self.c = 0.5 * self.dt / self.dx
        self.d = self.dt / (float(self.ReN)*math.pow(self.dx, 2.0))
        self.time = 0.0
        return

    def Initialize(self):
        self.dx = 1.0 / float(self.Grid-1)
        self.StreamError = 1.0
        self.VorticityError = 1.0
        self.iter = 0
        self.c = 0.5 * self.dt / self.dx
        self.d = self.dt / (float(self.ReN)*math.pow(self.dx, 2.0))
        return

    def Scheme_Printer(self):
        print("Solve Cavity ReN is {0} and Grid is {1}".format(self.ReN, self.Grid))
        self.Scheme_name = "ReN = %4d, Grid = %3d"%(self.ReN,self.Grid)
        return

    def Dir_Write(self):
        self.dirname = "Cavity, {0}".format(self.Scheme_name)
        path = os.getcwd()
        self.dirname = os.path.join(path, self.dirname)
        if os.path.isdir(self.dirname):
            shutil.rmtree(self.dirname)
        os.mkdir(self.dirname)
        return

    def Para_Write(self):
        filename = "{0}/{1}, iter = {2}.csv".format(self.dirname, self.Scheme_name, self.iter)
        file = open(filename, 'w')
        file.write("X,Y,Z,U,V,W,Psi\n")
        for i in range(self.Grid):
            for j in range(self.Grid):
                data = "%6.6f,%6.6f,%6.6f,%6.6f,%6.6f,%6.6f,%6.6f\n" % \
                       (float(j)*self.dx, float(i)*self.dx, 0.0, self.U[i][j],
                        self.V[i][j], self.W[i][j], self.Psi[i][j])
                file.write(data)
        file.close()
        return

    def Initial_Condition(self):
        self.U = np.zeros(self.Grid, self.Grid)
        self.V = np.zeros(self.Grid, self.Grid)
        self.W = np.zeros(self.Grid, self.Grid)
        self.Wnew = np.zeros(self.Grid, self.Grid)
        self.Psi = np.zeros(self.Grid, self.Grid)
        self.Psinew = np.zeros(self.Grid, self.Grid)
        for i in range(self.Grid):
            self.U[self.Grid-1][i] = self.U0
        return

    def Boundary_Condition(self):
        for i in range(self.Grid):
            self.W[i][self.Grid-1] = 2.0 * (self.Psi[i][self.Grid-1] - self.Psi[i][self.Grid-2]) / math.pow(self.dx, 2.0)
            self.W[i][0] = 2.0 * (self.Psi[i][0] - self.Psi[i][2]) / math.pow(self.dx, 2.0)
            self.W[self.Grid-1][i] = 2.0 * (self.Psi[self.Grid-1][i] - self.Psi[self.Grid-2][i]) / math.pow(self.dx, 2.0) - 2.0 * self.U0 / self.dx
            self.W[0][i] = 2.0 * (self.Psi[0][i] - self.Psi[1][i]) / math.pow(self.dx, 2.0)
        return

    def Velocity(self):
        for i in range(1, self.Grid-1):
            for j in range(1, self.Grid-1):
                self.U[i][j] = (self.Psi[i+1][j] - self.Psi[i-1][j])/(2.0*self.dx)
                self.V[i][j] = (self.Psi[i][j+1] - self.Psi[i][j-1])/(2.0*self.dx)
        return

    def Time_Marching(self):
        self.W = self.Wnew.copy()
        return

    def Check_W_Error(self):
        for i in range(1, self.Grid-1):
            for j in range(1, self.Grid-1):
                error = abs(self.W[i][j] - self.Wnew[i][j])
                self.VorticityError += math.pow(error, 2.0)
        self.VorticityError = math.sqrt(self.VorticityError / math.pow(float(self.Grid-2), 2.0))
        return

    def Check_Psi_Error(self):
        for i in range(1, self.Grid-1):
            for j in range(1, self.Grid-1):
                error = abs(self.Psi[i][j] - self.Psinew[i][j])
                self.StreamError += math.pow(error, 2.0)
        self.StreamError = math.sqrt(self.StreamError / math.pow(float(self.Grid-2), 2.0))
        return

    def Vorticity_FTCS(self):
        for i in range(1, self.Grid-1):
            for j in range(1, self.Grid-1):
                self.Wnew[i][j] = (1.0 - 4.0 * self.d) * self.W[i][j]\
                                  + (self.d - self.c * self.U[i][j+1]) * self.W[i][j+1]\
                                  + (self.d + self.c * self.U[i][j-1]) * self.W[i][j-1]\
                                  + (self.d - self.c * self.V[i+1][j]) * self.W[i+1][j]\
                                  + (self.d + self.c * self.V[i-1][j]) * self.W[i-1][j]

        return
    def PGS(self):
        for i in range(1, self.Grid-1):
            for j in range(1, self.Grid-1):
                self.Psinew[i][j] = 0.25 * (self.Psi[i+1][j] + self.Psi[i-1][j] + self.Psi[i][j+1] + self.Psi[i][j-1]
                                            + math.pow(self.dx, 2.0) * self.W[i][j])
    def Stream_PGS(self):
        while self.StreamError > self.Ermax:
            self.PGS()
            self.Check_Psi_Error()
            self.Psi = self.Psinew.copy()
            print("\rStream Error = %.6f" % self.StreamError, end="")
        return

    def Main(self, ren, grid):
        self.ReN = ren
        self.Grid = grid
        self.Scheme_Printer()
        self.Initialize()
        self.Dir_Write()
        while self.VorticityError > self.Ermax:
            self.Boundary_Condition()
            self.Vorticity_FTCS()
            self.Stream_PGS()
            self.Velocity()
            self.Check_W_Error()
            self.Time_Marching()
            self.time += self.dt
            print("\rtime = %.6r" % self.time, end="")
        print()
        self.Para_Write()
        return


def main():
    ID = Cavity()
    return ID
PyCompute = Cavity()
print("What ReN will you compute?")
prompt = """
1: ReN = 100  Grid = 129
2: ReN = 400  Grid = 129
3: ReN = 400  Grid = 257
4: ReN = 1000 Grid = 129
5: ReN = 3200 Grid = 129
6: ReN = 5000 Grid = 257

Enter Number(1~6): """
ID = 0
I = 1
while I:
    if 0 < ID < 7:
        I = 0
    else:
        print(prompt)
        ID = int(input())
if ID == 1:
    PyCompute.Main(100, 129)
elif ID == 2:
    PyCompute.Main(400, 129)
elif ID == 3:
    PyCompute.Main(400, 257)
elif ID == 4:
    PyCompute.Main(1000, 129)
elif ID == 5:
    PyCompute.Main(3200, 129)
elif ID == 6:
    PyCompute.Main(5000, 257)