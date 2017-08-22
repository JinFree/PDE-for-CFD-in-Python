import math
import os
import shutil
import numpy as np
class Hyperbolic:
    enumerate(['Ex_Upwind', 'Lax_method', 'Lax_Wendroff',
               'Non_Ex_Upwind', 'Non_Lax_Method', 'Non_Lax_Wendroff'])
    PI = math.pi
    def __init__(self):
        self.scheme = 'Ex_Upwind'

    def Initialize(self):
        if self.scheme == 'Ex_Upwind' or self.scheme == 'Lax_method' or self.scheme == 'Lax_Wendroff':
            self.dx = 5.0
            self.dt = 0.02
            self.end_t = 1.0
            self.L = 400
            self.alpha = 250.0
        elif self.scheme == 'Non_Ex_Upwind' or self.scheme == 'Non_Lax_Method' or self.scheme == 'Non_Lax_Wendroff':
            self.dx = 0.1
            self.dt = 0.1
            self.end_t = 1.0
            self.L = 4
            self.alpha = 1.0


    def Initialize_Time(self):
        self.time = 0.0

    def Scheme_Printer(self):
        if self.scheme == 'Ex_Upwind':
            print("Solve Explicit Upwind")
            self.Scheme_name = "Explicit Upwind"
        elif self.scheme == 'Lax_method':
            print("Solve Lax Method")
            self.Scheme_name = "Lax Method"
        elif self.scheme == 'Lax_Wendroff':
            print("Solve Lax Wendroff Method")
            self.Scheme_name = "Lax Wendroff Method"
        elif self.scheme == 'Non_Ex_Upwind':
            print("Solve Nonlinear Explicit Method")
            self.Scheme_name = "Nonlinear Explicit Method"
        elif self.scheme == 'Non_Lax_Method':
            print("Solve Nonlinear Lax Method")
            self.Scheme_name = "Nonlinear Lax Method"
        elif self.scheme == 'Non_Lax_Wendroff':
            print("Solve Nonlinear Lax Wendroff Method")
            self.Scheme_name = "Nonlinear Lax Wendroff Method"
        else:
            print("Wrong scheme input, ",end="")
            self.scheme = 'Ex_Upwind'
            self.Scheme_Printer()

    def CalDeltaT(self):
        self.dt = self.CFL * self.dx / self.alpha

    def Dir_Write(self):
        dirname = "Hyperbolic, {0}, c = {1}".format(self.Scheme_name, self.CFL)
        path = os.getcwd()
        dirname = os.path.join(path, dirname)
        self.dirname = dirname
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)  # 디렉토리가 존재하면 삭제하고 다시 계산# return # 디렉토리가 존재하면 덮어쓰기 #
        os.mkdir(dirname)

    def Para_Write(self):
        filename = "{0}/{1}, c = {2}.csv.".format(self.dirname, self.Scheme_name, self.CFL)
        filename = "%s%.6f"%(filename, self.time)
        file = open(filename, 'w')
        file.write("X,Y,Z,Velocity\n")
        for i in range(self.N):
            data = "%3.3f,%3.3f,%3.3f,%3.3f\n"%(float(i*self.dx),0.0,0.0,self.U[i])
            file.write(data)
        file.close()

    def Initial_Condition(self):
        if self.scheme == 'Ex_Upwind' or self.scheme == 'Lax_method' or self.scheme == 'Lax_Wendroff':
            for i in range(int(50.0/self.dx) , int(110.0/self.dx+1)):
                self.U[i] = abs(100.0 * (math.sin(self.PI*(i*self.dx - 50.0)/60.0)))
                self.Unew[i] = abs(100.0 * (math.sin(self.PI*(i*self.dx - 50.0)/60.0)))
        elif self.scheme == 'Non_Ex_Upwind' or self.scheme == 'Non_Lax_Method' or self.scheme == 'Non_Lax_Wendroff':
            for i in range(int(2.0/self.dx)):
                self.U[i] = 1.0
                self.Unew[i] = 1.0

    def Boundary_Condition(self):
        if self.scheme == 'Ex_Upwind' or self.scheme == 'Lax_method' or self.scheme == 'Lax_Wendroff':
            self.U[0] = 0.0
            self.Unew[0] = 0.0
            self.U[self.N-1] = 0.0
            self.Unew[self.N-1] = 0.0
        elif self.scheme == 'Non_Ex_Upwind' or self.scheme == 'Non_Lax_Method' or self.scheme == 'Non_Lax_Wendroff':
            self.U[0] = 1.0
            self.Unew[0] = 1.0
            self.U[self.N-1] = 0.0
            self.Unew[self.N-1] = 0.0

    def Time_Marching(self):
        self.U = self.Unew.copy()

    def Ex_Upwind(self):
        for i in range(1, self.N-1):
            self.Unew[i] = self.U[i] - self.CFL * (self.U[i]-self.U[i-1])

    def Lax_method(self):
        for i in range(1, self.N-1):
            self.Unew[i] = 0.5* ((self.U[i+1] + self.U[i-1])-self.CFL*(self.U[i+1]-self.U[i-1]))

    def Lax_Wendroff(self):
        for i in range(1, self.N-1):
            self.Unew[i] = self.U[i] - 0.5 * self.CFL *(self.U[i + 1] - self.U[i - 1]) + 0.5 * self.CFL* self.CFL * (self.U[i + 1] -2.0 * self.U[i]+ self.U[i - 1])

    def Non_Ex_Upwind(self):
        E = np.zeros(self.N)
        for i in range(self.N):
            E[i] = math.pow(self.U[i], 2)*0.5
        for i in range(1, self.N-1):
            self.Unew[i] = self.U[i] - self.CFL * (E[i] - E[i-1])

    def Non_Lax_Method(self):
        E = np.zeros(self.N)
        for i in range(self.N):
            E[i] = math.pow(self.U[i], 2)*0.5
        for i in range(1, self.N-1):
            self.Unew[i] = 0.5 * (self.U[i+1] + self.U[i-1] - self.CFL * (E[i+1] - E[i-1]))

    def Non_Lax_Wendroff(self):
        E = np.zeros(self.N)
        for i in range(self.N):
            E[i] = math.pow(self.U[i], 2)*0.5
        for i in range(1, self.N-1):
            self.Unew[i] = self.U[i] - 0.5 * self.CFL * (E[i+1] - E[i-1]) + 0.25 * self.CFL * self.CFL * ((self.U[i+1] + self.U[i])*(E[i+1]-E[i]) - (self.U[i] + self.U[i-1])*(E[i]-E[i-1]))

    def SCHEMEOPEN(self):
        if self.scheme == 'Ex_Upwind':
            self.Ex_Upwind()
        elif self.scheme == 'Lax_method':
            self.Lax_method()
        elif self.scheme == 'Lax_Wendroff':
            self.Lax_Wendroff()
        elif self.scheme == 'Non_Ex_Upwind':
            self.Non_Ex_Upwind()
        elif self.scheme == 'Non_Lax_Method':
            self.Non_Lax_Method()
        elif self.scheme == 'Non_Lax_Wendroff':
            self.Non_Lax_Wendroff()

    def Main(self, scheme):
        self.scheme = scheme
        self.Scheme_Printer()
        self.Initialize()
        CFL = [1.0, 0.5, 0.25]
        for i in CFL:
            self.Initialize_Time()
            self.CFL = i
            self.CalDeltaT()
            self.N = int(float(self.L)/self.dx)
            self.U = np.zeros(self.N)
            self.Unew = np.zeros(self.N)
            self.Initial_Condition()
            self.Boundary_Condition()
            self.iter = int(self.end_t/self.dt)
            self.Dir_Write()
            for j in range(self.iter+1):
                if float(j) % (1.0 / self.CFL) == 0:
                    self.Para_Write()
                self.SCHEMEOPEN()
                self.Time_Marching()
                self.Boundary_Condition()
                self.time += self.dt
                print("\rCFL = %3.3f, time = %.6f" % (self.CFL, self.time), end="")
            print()




def main():
    ID = Hyperbolic()
    return ID

PyCompute = Hyperbolic()
print("What Will you Compute?")
prompt = """
1: Explicit Upwind
2: Lax Method
3: Lax Wendroff Method
4: Nonlinear Explicit Upwind
5: Nonlinear Lax Method
6: Nonlinear Lax Wendroff Method

Enter Number(1~6): """
ID = 7
I = 1
while I:
    if 0 < ID < 7:
        I = 0
    else:
        print(prompt)
        ID = int(input())
if ID == 1:
    PyCompute.Main('Ex_Upwind')
if ID == 2:
    PyCompute.Main('Lax_method')
if ID == 3:
    PyCompute.Main('Lax_Wendroff')
if ID == 4:
    PyCompute.Main('Non_Ex_Upwind')
if ID == 5:
    PyCompute.Main('Non_Lax_Method')
if ID == 6:
    PyCompute.Main('Non_Lax_Wendroff')