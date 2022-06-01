import numpy as np
import matplotlib.pyplot as plt
from transistor import Transistor
plt.rc('font', size=30)

class Baseplate:
    def __init__(self,thermal_conductivity,thickness,Ta):
        self.k = thermal_conductivity        # thermal conductivity W/(m K)
        self.thickness = thickness           # substrate thickness in mm
        self.nump = 0.001                    # points pr mm
        self.view_x = 50                     # view area in mm
        self.view_z = 50
        self.max_estimation = True
        self.Ta = Ta

        self.transistor_array = []           # array of transistors placed on baseplate


    def change_view_range(self,view_x,view_z,nump):
        self.nump = nump
        self.view_x = view_x
        self.view_z = view_z


    def add_transistor(self,power,x0,z0):
        self.transistor_array.append(Transistor(power,x0,z0))

    def calculate_temperature_matrix(self,num_mirror_sources):

        T = []

        for transistor in self.transistor_array:
            print("Calculate surface temperature contribution for transistor with power " + str(transistor.power) + " and position (" + str(transistor.x0) + "," + str(transistor.z0) + ")" )
            Tmp = transistor.calc_contribution(self.nump, self.view_x, self.view_z, self.k,self.thickness,num_mirror_sources)
            if T == []:
                T = Tmp
            else:
                T += Tmp

        return T

    def plot_contour(self,T):
        np_x = int(self.view_x * self.nump)
        np_z = int(self.view_z * self.nump)

        xlist = np.linspace(0, self.view_x, np_x)
        zlist = np.linspace(0, self.view_z, np_z)
        X, Z = np.meshgrid(xlist, zlist)

        fig,ax = plt.subplots(1,1)

        for transistor in self.transistor_array:
            transistor.plot_base_xy(ax)

        cp = ax.contour(X,Z,T,40,cmap="inferno")
        ax.clabel(cp, inline=True, fontsize=10)
        #ax.set_ylim(30,80)
        ax.set_xlabel("z [mm]")
        ax.set_ylabel("x [mm]")
        plt.show()

    def plot_contourf(self,T):
        np_x = int(self.view_x * self.nump)
        np_z = int(self.view_z * self.nump)

        xlist = np.linspace(0, self.view_x, np_x)
        zlist = np.linspace(0, self.view_z, np_z)
        X, Z = np.meshgrid(xlist, zlist)

        fig, ax = plt.subplots(1, 1)

        for transistor in self.transistor_array:
            transistor.plot_base_xy(ax)

        ax.contourf(X, Z, T, 50,cmap="inferno")        #https://matplotlib.org/stable/tutorials/colors/colormaps.html
        plt.show()

    def print_junction_temp(self):

        T = self.calculate_temperature_matrix(1)
        result = []
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("Estimate junction temperature for transistor on baseplate")
        for transistor in self.transistor_array:
            temp = transistor.estimate_case_temperature(T,self.nump,self.max_estimation)
            result.append(temp)
            print("\t" + str(transistor.power) + "W transistor at (" + str(transistor.x0) + "," + str(transistor.z0) + "):\t\t" '%.4f' % temp)
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        return result

    def update_position(self,transistor_num,new_x0,new_z0):
        pos = transistor_num-1
        self.transistor_array[pos].set_position(new_x0,new_z0)

    def print_transistor_stat(self,T):
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        print("|Position\t|Power\t|Temperature increase (average / max)\t|Case temperature (average / max)" )
        for transistor in self.transistor_array:
            position = '%.1f' % transistor.x0 + "," + '%.1f' % transistor.z0

            tmp_max = transistor.estimate_case_temperature(T,self.nump,False)
            tmp_avg = transistor.estimate_case_temperature(T,self.nump,True)

            print(position + "\t|" + str(transistor.power) + "\t|" + '%.2f' % tmp_max + " / " + '%.2f' % tmp_avg + "\t\t\t\t\t\t\t|" + '%.2f' % (tmp_max + self.Ta) + " / " + '%.2f' % (tmp_avg + self.Ta))
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
