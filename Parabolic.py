import math
import os
import shutil
import numpy as np
class Parabolic:
    enumerate(['Explicit', 'Implicit'])

    def __init__(self):
        self.U0 = 40
        self.N = 41
        self.h = 0.04
        self.dx = self.h/(self.N-1)
        self.dt = float(0.000001)
        self.t_end = float(0.0007)
        self.nu = 0.5
        self.diffusion = 0.5
        self.U = np.random.randn(self.N)
        self.Unew = np.random.randn(self.N)
        self.Scheme_name = "Error"
        self.scheme = 'Explicit'
        self.iter = int(self.t_end/self.dt)
        self.time = float(0.0)
        self.dirname = "Error"
        return

    def Scheme_Printer(self):
        print("Solve {0}".format(self.scheme))
        self.Scheme_name = "%s"%self.scheme
        return

    def diffusion_number(self):
        self.diffusion = self.nu * self.dt / (math.pow(self.dx, 2))
        print("Diffusion number is %.3f"%self.diffusion)

    def dinamic_viscosity(self):
        self.nu = float(input("Input Dynamic viscosity: "))
        self.diffusion_number()
        if (self.diffusion > 0.5 )and (self.scheme == 'Explicit'):
            print("You cannot get proper solution in explicit scheme when diffusion number is larger than 0.5")

    def Initial_Condition(self):
        self.U = np.zeros(self.N)
        self.Unew = np.zeros(self.N)

    def Boundary_Condition(self):
        self.U[0] = self.Unew[0] = self.U0

    def Time_Marching(self):
        self.U = self.Unew.copy()

    def Dir_Write(self):
        self.dirname = "Parabolic, {0}, d={1}".format(self.Scheme_name, self.diffusion)
        path = os.getcwd()
        self.dirname = os.path.join(path, self.dirname)
        if os.path.isdir(self.dirname):
            shutil.rmtree(self.dirname)  # 디렉토리가 존재하면 삭제하고 다시 계산# return # 디렉토리가 존재하면 덮어쓰기 #
        os.mkdir(self.dirname)
        return

    def Para_Write(self):
        filename = "{0}/{1}, d={2}.csv.".format(self.dirname, self.Scheme_name, self.diffusion)
        filename = "%s%.6f"%(filename, self.time)
        file = open(filename, 'w')
        file.write("X,Y,Z,Velocity\n")
        for i in range(len(self.U)):
            data = "%3.3f,%3.3f,%3.3f,%3.3f\n" % (float(i*self.dx), 0.0, 0.0, self.U[i])
            file.write(data)
        file.close()

    def FTCS(self):
        for i in range(1, len(self.U)-1):
            self.Unew[i] = self.diffusion * (self.U[i-1]+self.U[i+1])+(1.0-2.0*self.diffusion)*self.U[i]

    def Explicit_Solver(self):
        for i in range(self.iter+1):
            self.Para_Write()
            self.FTCS()
            self.Time_Marching()
            self.time += self.dt
            print("\rtime = %.6f"%self.time, end="")
        print()

    def Lassonen_A_Mat(self):
        self.A = np.zeros(3)
        self.A[0] = -self.diffusion
        self.A[1] = 1.0+2.0*self.diffusion
        self.A[2] = -self.diffusion

    def Lassonen(self):
        P = np.zeros(self.N)
        Q = np.zeros(self.N)
        Q[0] = self.U[0]
        for i in range(1, self.N-1):
            P[i] = -self.A[2] / ((self.A[0] * P[i-1]) + self.A[1])
            Q[i] = (self.U[i] - (self.A[0] * Q[i-1])) / ((self.A[0] * P[i-1]) + self.A[1])
        self.Unew[self.N-1] = Q[self.N-1]
        for j in range(0, self.N-1):
            i = self.N-2 - j
            self.Unew[i] = P[i] * self.Unew[i+1] + Q[i]

    def Implicit_Solver(self):
        self.Lassonen_A_Mat()
        for i in range(self.iter+1):
            self.Para_Write()
            self.Lassonen()
            self.Time_Marching()
            self.time += self.dt
            print("\rtime = %.6f"%self.time, end="")
        print()

    def Main(self, scheme):
        self.time = 0.0
        self.scheme = scheme
        self.Scheme_Printer()
        self.dinamic_viscosity()
        self.Initial_Condition()
        self.Boundary_Condition()
        self.Dir_Write()
        if scheme == 'Explicit':
            self.Explicit_Solver()
        else:
            self.Implicit_Solver()


def main():
    func = Parabolic()
    return func

PyCompute = Parabolic()
print("What Will you Compute?")
prompt = """
1: Explicit FTCS
2: Implicit Lassonen

Enter Number(1~2): """
ID = 5
I = 1
while I:
    if 0 < ID < 3:
        I = 0
    else:
        print(prompt)
        ID = int(input())
if ID == 1:
    PyCompute.Main('Explicit')
elif ID == 2:
    PyCompute.Main('Implicit')