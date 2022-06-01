import numpy as np
from matplotlib.patches import Rectangle

class Transistor:
    def __init__(self,power,x0,z0):
        self.power  = power      # Dissipated power in W
        self.width  = 4.1        # Width in mm
        self.length = 9.5        # Length in mm
        self.Rth = 4.8

        self.accurate = True

        self.x0 = x0             # center coordinates
        self.z0 = z0

    def set_position(self,x0,z0):
        self.x0 = x0
        self.z0 = z0

    def plot_base_xy(self, ax):
        ax.add_patch(Rectangle((self.z0-self.length*0.5,self.x0-self.width*0.5),self.length,self.width,color="grey"))

    def calc_mirror_source_contribution(self,nump,view_x,view_z,k,thickness,ms_num):

        print("  - Adding contribution from mirror source " + str(ms_num))

        np_x = int(view_x*nump)            # nump = number of points pr um
        np_z = int(view_z*nump)

        T = np.zeros((np_x, np_z))
        yds = ((thickness*2*ms_num)*(10**-3))**2

        return self.add_mirror_plate_contribution(T,np_x,np_z,k,yds,nump,ms_num)

    def add_mirror_source_point_contribution(self,T,np_x,np_z,k,yds,pwr,nump):
        for x in range(np_x):
            xds = ((x/nump - self.x0)*(10**-3))**2
            for z in range(np_z):
                zds = ((z/nump-self.z0)*(10**-3))**2
                T[x][z] += pwr / (2*np.pi*k*np.sqrt(xds + zds + yds))
        return T

    def add_mirror_plate_contribution(self,T,np_x,np_z,k,yds,nump,ms_num):
        if self.accurate:
            return self.add_mirror_plate_contribution_accurate(T,np_x,np_z,k,yds,nump,ms_num)
        else:
            return self.add_mirror_plate_contribution_fast(T, np_x, np_z, k, yds, nump, ms_num)

    def add_mirror_plate_contribution_accurate(self,T,np_x,np_z,k,yds,nump,ms_num):
        Xln = int((self.x0 - self.width * 0.5)*nump)
        Xun = int((self.x0 + self.width * 0.5)*nump)
        Zln = int((self.z0 - self.length * 0.5)*nump)
        Zun = int((self.z0 + self.length * 0.5)*nump)

        pwr = self.power/(((Xun-Xln)*(Zun-Zln))*(-1)**ms_num)

        for xt in range(Xln,Xun,1):
            print("    * Row " + str(xt-Xln+1) + " of " + str(Xun-Xln))
            for zt in range(Zln,Zun,1):
                T = self.add_mirror_source_point_contribution(T,np_x,np_z,k,yds,pwr,nump)

        return T

    def add_mirror_plate_contribution_fast(self,T,np_x,np_z,k,yds,nump,ms_num):
        return self.add_mirror_source_point_contribution(T,np_x,np_z,k,yds,self.power,nump)

    def calc_plate_contribution(self,nump,view_x,view_z,k):

        print("  - Calculating contribution from transistor plate")

        np_x = int(view_x*nump)            # nump = number of points pr um
        np_z = int(view_z*nump)

        T = np.zeros((np_x, np_z))

        for x in range(np_x):
            for z in range(np_z):
                A1 = (x/nump - self.x0 - self.width*0.5)*(10**-3)
                A2 = (x/nump - self.x0 + self.width*0.5)*(10**-3)
                B1 = (z/nump - self.z0 - self.length*0.5)*(10**-3)
                B2 = (z/nump - self.z0 + self.length*0.5)*(10**-3)

                A1 = 0.000000001 if (A1 == 0) else A1
                A2 = 0.000000001 if (A2 == 0) else A2
                B1 = 0.000000001 if (B1 == 0) else B1
                B2 = 0.000000001 if (B2 == 0) else B2

                c1 = A2*(np.arcsinh(B2/np.abs(A2))-np.arcsinh(B1/np.abs(A2)))
                c2 = A1*(np.arcsinh(B2/np.abs(A1))-np.arcsinh(B1/np.abs(A1)))
                c3 = B2*(np.arcsinh(A2/np.abs(B2))-np.arcsinh(A1/np.abs(B2)))
                c4 = B1*(np.arcsinh(A2/np.abs(B1))-np.arcsinh(A1/np.abs(B1)))

                T[x][z] = (self.power/(2*np.pi*k*self.length*self.width*k*(10**-9)))*(c1-c2+c3-c4)

        return T

    def calc_contribution(self, nump,view_x,view_z,k,thickness,num_mirror_sources):
        T = self.calc_plate_contribution(nump,view_x,view_z,k)
        if num_mirror_sources > 0:
            for ms in range(1,num_mirror_sources+1):
                T += self.calc_mirror_source_contribution(nump,view_x,view_z,k,thickness,ms)

        return T

    def estimate_case_temperature(self,T,nump,max_point):

        # find edges of transistor
        x_low   = int((self.x0 - self.width*0.5)*nump)
        x_up    = int((self.x0 + self.width*0.5)*nump)
        z_low   = int((self.z0 - self.length*0.5)*nump)
        z_up    = int((self.z0 + self.length*0.5)*nump)
        T_local = T[x_low:x_up, z_low:z_up]

        if (max_point):
            return np.max(T_local)
        else:
            return np.average(T_local)

    def estimate_junction_temperature(self,T,nump,max_point,Ta):
        return self.estimate_case_temperature(T,nump,max_point) + Ta + self.Rth*self.power

    def change_direction(self):
        w = self.width
        self.width = self.length
        self.length = w
