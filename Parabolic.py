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

    def Scheme_Printer(self):
        if self.scheme == 'Explicit':
            print("Solve Explicit")
            self.Scheme_name = "Explicit"
        elif self.scheme == 'Implicit':
            print("Solve Implicit")
            self.Scheme_name = "Implicit"
        else:
            print("Wrong scheme input, solve Explicit")
            self.scheme = 'Explicit'
            self.Scheme_name = "Explicit"

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
        dirname = "Parabolic, {0}, d={1}".format(self.Scheme_name, self.diffusion)
        path = os.getcwd()
        dirname = os.path.join(path, dirname)
        if os.path.isdir(dirname):
            shutil.rmtree(dirname) # 디렉토리가 존재하면 삭제하고 다시 계산
        os.mkdir(dirname)
        self.dirname = dirname

    def Para_Write(self):
        filename = "{0}/{1}, d={2}.csv.".format(self.dirname, self.Scheme_name, self.diffusion)
        filename = "%s%.6f"%(filename, self.time)
        file = open(filename,'w')
        file.write("X,Y,Z,Velocity\n")
        for i in range(len(self.U)):
            data = "%3.3f,%3.3f,%3.3f,%3.3f\n"%(float(i*self.dx),0.0,0.0,self.U[i])
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

    def Lassonen(self):
        return
    def Implicit_Solver(self):
        for i in range(self.iter+1):
            self.Para_Write()
            self.Lassonen()
            self.Time_Marching()
            self.time += self.dt
            print("\rtime = %.6f"%self.time, end="")
        print()

    def Compute(self, scheme):
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
    ID = Parabolic()
    return ID

def help():
    prompt = """Compute function
    0: 'Explicit'
    1: 'Implicit'"""
    print(prompt)