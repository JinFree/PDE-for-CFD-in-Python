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
        return

    def Initialize(self):
        self.dx = 1.0 / float(self.Grid-1)
        self.StreamError = 1.0
        self.VorticityError = 1.0
        self.iter = 0
        return

    def Scheme_Printer(self):
        print("Solve Caviry ReN is {0} and Grid is {1}".format(self.ReN, self.Grid))
        self.Scheme_name = "ReN = %4d, Grid = %3d"%(self.ReN,self.Grid)
        return

    def Dir_Write(self):
        self.dirname = "Cavity, {0}".format(self.Scheme_name)
        path = os.getcwd()
        self.dirname = os.path.join(path, self.dirname)
        if os.path.isdir(self.dirname):
            shutil.rmtree(self.dirname)  # 디렉토리가 존재하면 삭제하고 다시 계산# return # 디렉토리가 존재하면 덮어쓰기 #
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
            self.W[][]
        return

    def Velocity(self):
        return

    def Time_Marching(self):
        return

    def Check_Error(self):
        return

    def Vorticity_FTCS(self):
        return

    def Stream_PGS(self):
        return

    def Main(self, ren, grid):
        self.ReN = ren
        self.Grid = grid
        self.Scheme_Printer()
        self.Initialize()

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