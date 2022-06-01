import matplotlib.pyplot as plt
import numpy as np

from baseplate import Baseplate

class Simulation:

    def __init__(self,k,h,nump,ms,Ta):
        self.k = k
        self.h = h
        self.nump = nump
        self.ms = ms
        self.Ta = Ta

    def plot_2transistors_distanse(self,pwr,start_distance,end_distance,num_points):
        baseplate = Baseplate(self.k,self.h,self.Ta)
        view_length = end_distance + 20
        baseplate.change_view_range(view_length,view_length,self.nump)

        init_x1 = view_length*0.5 - start_distance*0.5
        init_x2 = view_length * 0.5 + start_distance * 0.5
        z_pos   = view_length*0.5

        baseplate.add_transistor(pwr,init_x1,z_pos)
        baseplate.add_transistor(pwr,init_x2,z_pos)

        distances = np.linspace(start_distance,end_distance,num_points)

        junction_temp = []
        plt.rc('font', size=30)

        for d in distances:

            print("=========================================================================================")
            print("Distance: " + '%.3f' % d)
            print("=========================================================================================")

            x1_pos = view_length * 0.5 - d * 0.5
            x2_pos = view_length * 0.5 + d * 0.5

            baseplate.update_position(1, x1_pos, z_pos)
            baseplate.update_position(2, x2_pos, z_pos)

            T = baseplate.calculate_temperature_matrix(self.ms)

            tmp = baseplate.transistor_array[1].estimate_junction_temperature(T,self.nump,True,self.Ta)

            junction_temp.append(tmp)

        print(junction_temp)

        plt.plot(distances,junction_temp, lw=4, c="black")
        plt.grid()
        plt.xlabel("Distance [mm]")
        plt.ylabel("Tj [°C]")
        plt.show()

    def plot_2transistors_thickness(self,pwr,distance,start_t,end_t,num_points):
        baseplate = Baseplate(self.k,self.h,self.Ta)
        view_length = distance + 20
        baseplate.change_view_range(view_length,view_length,self.nump)

        x1 = view_length*0.5 - distance*0.5
        x2 = view_length * 0.5 + distance * 0.5
        z_pos = view_length*0.5

        baseplate.add_transistor(pwr,x1,z_pos)
        baseplate.add_transistor(pwr,x2,z_pos)

        thicknesses = np.linspace(start_t,end_t,num_points)

        junction_temp = []
        plt.rc('font', size=30)

        for t in thicknesses:

            print("=========================================================================================")
            print("Thickness: " + '%.3f' % t)
            print("=========================================================================================")

            baseplate.thickness = t

            T = baseplate.calculate_temperature_matrix(self.ms)

            tmp = baseplate.transistor_array[1].estimate_junction_temperature(T,self.nump,True,self.Ta)

            junction_temp.append(tmp)

        print(junction_temp)

        plt.plot(thicknesses,junction_temp, lw=4, c="black")
        plt.grid()
        plt.xlabel("Thickness [mm]")
        plt.ylabel("Tj [°C]")
        plt.show()

    def plot_2transistors_k(self,pwr,distance,start_k,end_k,num_points):
        baseplate = Baseplate(self.k,self.h,self.Ta)
        view_length = distance + 20
        baseplate.change_view_range(view_length,view_length,self.nump)

        x1 = view_length*0.5 - distance*0.5
        x2 = view_length * 0.5 + distance * 0.5
        z_pos = view_length*0.5

        baseplate.add_transistor(pwr,x1,z_pos)
        baseplate.add_transistor(pwr,x2,z_pos)

        cond = np.linspace(start_k,end_k,num_points)

        junction_temp = []
        plt.rc('font', size=30)

        for k in cond:

            print("=========================================================================================")
            print("Thermal conductivity: " + '%.3f' % k)
            print("=========================================================================================")

            baseplate.k = k

            T = baseplate.calculate_temperature_matrix(self.ms)

            tmp = baseplate.transistor_array[0].estimate_junction_temperature(T,self.nump,True,self.Ta)

            junction_temp.append(tmp)

        print(junction_temp)

        plt.plot(cond,junction_temp, lw=4, c="black")
        plt.grid()
        plt.xlabel("Thermal Conductivity [W/°C]")
        plt.ylabel("Tj [°C]")
        plt.show()

    def plot_2transistors_tmp_diff(self, pwr, distance, start_k, end_k, num_points):
            baseplate = Baseplate(self.k, self.h, self.Ta)
            view_length = distance * (3 - 1) + 20
            baseplate.change_view_range(view_length, view_length, self.nump)
            z_coordinates = np.linspace(10, view_length - 10, 3)
            x_pos = view_length * 0.5

            for z_pos in z_coordinates:
                baseplate.add_transistor(pwr, x_pos, z_pos)

            cond = np.linspace(start_k, end_k, num_points)

            junction_temp = []
            plt.rc('font', size=30)

            for k in cond:
                print("=========================================================================================")
                print("Thermal conductivity: " + '%.3f' % k)
                print("=========================================================================================")

                baseplate.k = k

                T = baseplate.calculate_temperature_matrix(self.ms)

                tmp_1 = baseplate.transistor_array[0].estimate_junction_temperature(T, self.nump, True, self.Ta)
                tmp_2 = baseplate.transistor_array[1].estimate_junction_temperature(T, self.nump, True, self.Ta)

                tmp_diff = tmp_2-tmp_1

                junction_temp.append(tmp_diff)

            print(junction_temp)

            plt.plot(cond, junction_temp, lw=4, c="black")
            plt.grid()
            plt.xlabel("Thermal Conductivity [W/°C]")
            plt.ylabel("Tj [°C]")
            plt.show()

    def case_vertical_line(self,distance,num_transistors,pwr):
        baseplate = Baseplate(self.k,self.h,self.Ta)
        view_length = distance*(num_transistors-1) + 20
        baseplate.change_view_range(view_length,view_length,self.nump)
        x_coordinates = np.linspace(10,view_length-10,num_transistors)
        z_pos = view_length*0.5

        for x_pos in x_coordinates:
            baseplate.add_transistor(pwr,x_pos,z_pos)

        T = baseplate.calculate_temperature_matrix(self.ms)
        baseplate.print_transistor_stat(T)
        baseplate.plot_contour(T)

    def case_horisontal_line(self,distance,num_transistors,pwr):
        baseplate = Baseplate(self.k,self.h,self.Ta)
        view_length = distance*(num_transistors-1) + 20
        baseplate.change_view_range(view_length,view_length,self.nump)
        z_coordinates = np.linspace(10,view_length-10,num_transistors)
        x_pos = view_length*0.5

        for z_pos in z_coordinates:
            baseplate.add_transistor(pwr,x_pos,z_pos)

        T = baseplate.calculate_temperature_matrix(self.ms)
        baseplate.print_transistor_stat(T)
        baseplate.plot_contour(T)

    def case_diagonal_line(self,distance,num_transistors,pwr):
        baseplate = Baseplate(self.k, self.h,self.Ta)
        distance_axis = distance/np.sqrt(2)
        view_length = distance_axis * (num_transistors - 1) + 20
        baseplate.change_view_range(view_length, view_length, self.nump)
        coordinates = np.linspace(10, view_length - 10, num_transistors)

        for pos in coordinates:
            baseplate.add_transistor(pwr, pos, pos)

        T = baseplate.calculate_temperature_matrix(self.ms)
        baseplate.print_transistor_stat(T)
        baseplate.plot_contour(T)

    def case_zshape(self,distance,num_transistors,pwr):
        baseplate = Baseplate(self.k,self.h,self.Ta)
        distance_axis = distance*np.sqrt(3)*0.5
        view_length = distance*(num_transistors-1)*0.5+20
        baseplate.change_view_range(view_length,view_length,self.nump)
        coordinates_z = np.linspace(10,view_length-10,num_transistors)

        for index in range(len(coordinates_z)):
            pos_x = view_length*0.5 + ((-1)**index)*distance_axis*0.5
            pos_z = coordinates_z[index]
            baseplate.add_transistor(pwr, pos_x, pos_z)

        T = baseplate.calculate_temperature_matrix(self.ms)
        baseplate.print_transistor_stat(T)
        baseplate.plot_contour(T)

    def case_diamond(self,distance,pwr):        # Only for 4 transistors
        baseplate = Baseplate(self.k,self.h,self.Ta)
        offset = distance/np.sqrt(2)
        view_length = 2*offset + 20
        center = view_length * 0.5
        baseplate.change_view_range(view_length,view_length,self.nump)

        baseplate.add_transistor(pwr, center, center + offset)
        baseplate.add_transistor(pwr, center, center - offset)
        baseplate.add_transistor(pwr, center + offset, center)
        baseplate.add_transistor(pwr, center - offset, center)

        T = baseplate.calculate_temperature_matrix(self.ms)
        baseplate.print_transistor_stat(T)
        baseplate.plot_contour(T)

    def case_square(self,distance,pwr):        # Only for 4 transistors
        baseplate = Baseplate(self.k,self.h,self.Ta)
        offset = distance/np.sqrt(2)
        view_length = 2*offset + 40
        center = view_length * 0.5
        baseplate.change_view_range(view_length,view_length,self.nump)

        baseplate.add_transistor(pwr, center + offset, center + offset)
        baseplate.add_transistor(pwr, center - offset, center + offset)
        baseplate.add_transistor(pwr, center + offset, center - offset)
        baseplate.add_transistor(pwr, center - offset, center - offset)

        T = baseplate.calculate_temperature_matrix(self.ms)
        baseplate.print_transistor_stat(T)
        baseplate.plot_contour(T)

    def symetric_angle_sweep(self,radius,pwr,num_points):
        baseplate = Baseplate(self.k,self.h,self.Ta)

        angle = np.linspace(0,np.pi,num_points)

        view_length = 2 * radius + 20
        center = radius + 10

        baseplate.change_view_range(view_length,view_length,self.nump)
        baseplate.add_transistor(pwr,10,10)
        baseplate.add_transistor(pwr,center,center)

        tmp_array = []

        for a in angle:

            print("=========================================================================================")
            print("Angle: " + '%.3f' % a)
            print("=========================================================================================")

            z_pos = center + radius * np.sin(a)
            x_pos = center + radius * np.cos(a)

            baseplate.update_position(1,z_pos,x_pos)

            T = baseplate.calculate_temperature_matrix(self.ms)

            tmp = baseplate.transistor_array[1].estimate_junction_temperature(T,self.nump,True,self.Ta)

            tmp_array.append(tmp)

        print(tmp_array)

        plt.grid()
        plt.xlabel("Angle [rad]")
        plt.ylabel("Tj [°C]")
        plt.ticklabel_format(useOffset=False, style='plain')
        plt.plot(angle, tmp_array, lw=4, c="black")
        plt.show()


    def case_zshape_with_offset(self,distance,num_transistors,pwr,offset):
        baseplate = Baseplate(self.k,self.h,self.Ta)
        distance_axis = np.sqrt(distance**2 - 0.25*(distance+offset)**2)
        view_length = distance*(num_transistors-1)*0.5+20+(num_transistors-1)*offset
        baseplate.change_view_range(view_length,view_length,self.nump)
        coordinates_z = np.linspace(10,view_length-10,num_transistors)

        for index in range(len(coordinates_z)):
            pos_x = view_length*0.5 + ((-1)**index)*distance_axis*0.5
            pos_z = coordinates_z[index]
            baseplate.add_transistor(pwr, pos_x, pos_z)

        T = baseplate.calculate_temperature_matrix(self.ms)
        baseplate.print_transistor_stat(T)
        baseplate.plot_contour(T)

    def plot_npmm_depencence(self):
        baseplate = Baseplate(self.k, self.h, self.Ta)
        view_length = 20
        baseplate.change_view_range(view_length, view_length, self.nump)

        x_pos = view_length * 0.5
        z_pos = view_length * 0.5

        baseplate.add_transistor(25, x_pos, z_pos)

        npmms = np.linspace(1, 15, 15)

        junction_temp_max = []
        junction_temp_avg = []
        plt.rc('font', size=30)

        for npmm in npmms:
            print("=========================================================================================")
            print("npmm: " + '%.3f' % npmm)
            print("=========================================================================================")

            baseplate.change_view_range(view_length, view_length, npmm)

            T = baseplate.calculate_temperature_matrix(self.ms)

            #tmp_max = baseplate.transistor_array[0].estimate_case_temperature(T, npmm, True) + self.Ta
            tmp_avg = baseplate.transistor_array[0].estimate_case_temperature(T, npmm, False) + self.Ta

            #junction_temp_max.append(tmp_max)
            junction_temp_avg.append(tmp_avg)


        plt.plot(npmms, junction_temp_avg, lw=4, c="black")
        #plt.plot(npmms, junction_temp_max, lw=4, c="black",linestyle="dashed")
        plt.grid()
        plt.xlabel("Points per mm")
        plt.ylabel("Tj [°C]")
        plt.show()
