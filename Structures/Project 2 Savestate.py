import numpy as np
import tkinter as tk
from tkinter.ttk import Notebook
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure as fig

class Struct_Frame():
    """Class to define the overall frame. Includes input for beam geometry"""
    def __init__(self, E:float, b:float, h:float):
        self.E = E
        self.b = b
        self.h = h

        self.A = b*h
        self.I = b*h**3/12

        self.joints = []
        self.members = []

    def solve(self):
        """Function to solve all of the different forces and displacements in the frame"""
        num_nodes = len(self.joints)*3 # 3 nodes per joint

        loads = np.zeros((num_nodes,1)) # applied loading
        free_nodes = [] # nodes with no displacement constraint
        fixed_nodes = [] # constrained nodes
        node_num = 0 # node index
        for joint in self.joints:
            # Defining whether each node is free or fixed based on its degrees of freedom. DoF is determined by the support: Fixed = 0, 
            # Pin = 1, Roller = 2.The current node index is appended to its respective list to sort them by free/fixed.
            if joint.DoF == 0:
                fixed_nodes.append(node_num)
                fixed_nodes.append(node_num+1)
                fixed_nodes.append(node_num+2)
            elif joint.DoF == 1:
                fixed_nodes.append(node_num)
                fixed_nodes.append(node_num+1)
                free_nodes.append(node_num+2)
            elif joint.DoF == 2:
                free_nodes.append(node_num)
                fixed_nodes.append(node_num+1)
                free_nodes.append(node_num+2)
            elif joint.DoF == 3:
                free_nodes.append(node_num)
                free_nodes.append(node_num+1)
                free_nodes.append(node_num+2)
            
            # Assigning any applied loads to the loading matrix. If the joint doesn't have any, it will send a 0 (handled in Joint class)
            loads[node_num] = joint.force_x
            loads[node_num+1] = joint.force_y
            loads[node_num+2] = joint.moment

            # the loop handles 1 joint (3 nodes) at a time so update node index to reflect
            node_num += 3

        S = np.zeros((num_nodes,num_nodes)) # global stiffness matrix of the entire frame
        for member in self.members:
            # Stiffness matrix creation handled inside Member class
            member.K = member.global_stiff_matrix(E=self.E, A=self.A, I=self.I)

            # Expanding K matrix to fit entire frame
            K_frame = np.zeros((num_nodes,num_nodes))
            K_frame[np.ix_(member.index,member.index)] = member.K

            # Adding each expanded K matrix to S
            S += K_frame

        # Removing fixed node indicies from S and P
        S = np.delete(np.delete(S, fixed_nodes, axis=0), fixed_nodes, axis=1)
        loads = np.delete(loads, fixed_nodes, axis=0)

        # some linear algebra to solve for d in P = Sd
        d = np.linalg.solve(S, loads)

        d_frame = np.zeros((num_nodes,1)) # displacement matrix for entire frame. fixed nodes = 0
        i = 0
        for free_node in free_nodes:
            # expanding displacement matrix to fit the entire frame
            d_frame[free_node] = d[i]
            i += 1

        for member in self.members:
            # indexing the indicies of the nodes in each member
            member.v = d_frame[member.index]
            member.k = member.local_stiff_matrix(E=self.E, A=self.A, I=self.I)
            T = member.transformation_matrix()

            member.u = T @ member.v # displacement of nodes in each member relative to frame axes
            member.Q = member.k @ member.u # local member forces

            member.F = T.T @ member.Q # forces relative to frame axes

            member.a_stress = member.Q[3,0]/self.A # axial stress in beam
            member.a_strain = member.a_stress/self.E # axial strain in the member
            x = np.linspace(0,member.length,len(member.stress_top))
            for i in range(len(member.stress_top)):
                member.stress_top[i] = -self.h/2*(member.Q[1,0]*x[i] - member.Q[2,0])/self.I + member.a_stress # bending stress along beam
                member.stress_bottom = -1*member.stress_top

                member.strain_top = member.stress_top/self.E
                member.strain_bottom = -1*member.strain_top
        
    def plot_stress_and_strain(self):
        """Function to display the stress and strain plots in a separate window. The program will automatically generate a new tab for each member."""

        class Beam_Plot(tk.Frame):
            """Class to define all of the things identical between the stress and strain plots"""
            def __init__(self, master:tk, frame:Struct_Frame, member_index:int):
                super().__init__()

                self.master = master
                self.member = frame.members[member_index]
                self.title_index = member_index + 1
                self.x = np.linspace(0, self.member.length, len(self.member.stress_top))

                self.fig = fig(figsize=(3,3))
                self.ax = self.fig.add_subplot(111)
                self.ax.set_xlabel('Location along member (in)')

            def place(self):
                canvas = FigureCanvasTkAgg(self.fig, self.master)
                canvas.draw()
                canvas.get_tk_widget().pack(side='left', fill='both', expand=True)

        class Stress_Plot(Beam_Plot):
            """Class to define the aspects unique to the stress plot"""
            def __init__(self, master:tk, frame:Struct_Frame, member_index:int):
                super().__init__(master, frame, member_index)

                self.ax.plot(self.x, self.member.stress_top, label='Top Stress')
                self.ax.plot(self.x, self.member.stress_bottom, label='Bottom Stress')
                self.ax.set_title(f'Maximum Normal Stress Distribution: Member {self.title_index}')
                self.ax.set_ylabel('Stress (ksi)')

        class Strain_Plot(Beam_Plot):
            """Class to define the aspects unique to the strain plot"""
            def __init__(self, master:tk, frame:Struct_Frame, member_index:int):
                super().__init__(master, frame, member_index)

                self.ax.plot(self.x, self.member.strain_top, label='Top Strain')
                self.ax.plot(self.x, self.member.strain_bottom, label='Bottom Strain')
                self.ax.set_title(f'Maximum Normal Strain Distribution: Member {self.title_index}')
                self.ax.set_ylabel('Strain (micron)')
                
                # forcing the y axis to display in scientific notation otherwise it gets cut off
                self.ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

        class Root(tk.Tk):
            """Class to define the main window information"""
            def __init__(self, frame:Struct_Frame):
                super().__init__()
                self.title("Stress and Strain Plots")

                # Size of the main window
                window_width = 1300
                window_height = 700

                # Configure to put the window in the center of the screen
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                x = (screen_width // 2) - (window_width // 2)
                y = (screen_height // 2) - (window_height // 2)
                self.geometry(f"{window_width}x{window_height}+{x}+{y}")

                # Escape key closes the window
                self.bind("<Escape>",lambda event=None: self.destroy())

                notebook = Notebook(self)
                notebook.pack(fill='both', expand=True)

                for i in range(len(frame.members)):
                    page = tk.Frame(notebook)
                    notebook.add(page, text=f"Member {i+1}")

                    stress = Stress_Plot(page, frame, i)
                    stress.place()
                    strain = Strain_Plot(page, frame, i)
                    strain.place()

        Root(self).mainloop()
    
    def plot_displacement(self):
        for member in self.members:
           member.member_disp(E=self.E,I=self.I)

        class Root(tk.Tk):
            """Class to define the main window information"""
            def __init__(self, frame:Struct_Frame):
                super().__init__()
                self.title("Stress and Strain Plots")

                # Size of the main window
                window_width = 600
                window_height = 600

                # Configure to put the window in the center of the screen
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                x = (screen_width // 2) - (window_width // 2)
                y = (screen_height // 2) - (window_height // 2)
                self.geometry(f"{window_width}x{window_height}+{x}+{y}")

                # Escape key closes the window
                self.bind("<Escape>",lambda event=None: self.destroy())

                Frame_Plot(self, frame)

        class Frame_Plot(tk.Frame):
            def __init__(self, master:tk, frame:Struct_Frame):
                super().__init__()

                self.fig = fig(figsize=(3,3))
                self.ax = self.fig.add_subplot(111)
                
                for member in frame.members:
                    self.ax.plot(member.x_pos, member.y_pos, color='blue')
                    self.ax.plot(member.x_pos + member.disp_x*100, member.y_pos + member.disp_y*100, color='red')
                
                canvas = FigureCanvasTkAgg(self.fig, master)
                canvas.draw()
                canvas.get_tk_widget().pack(fill='both', expand=True)

        Root(self).mainloop()

class Joint():
    """Class to input each joint in the frame. The number of joints is different for each frame, so instead of assinging to a variable, 
    each Joint appends itself to a list in its repsective Struct_Frame class as a part of the init funciton. Create joints in the order of 
    stiffness method convention."""
    nodes = np.arange(3) # each joint includes 3 nodes

    def __init__(self, frame:Struct_Frame, DoF:int, location_x:float, location_y:float, force_x:float=0, force_y:float=0, moment:float=0):
        self.location_x = location_x
        self.location_y = location_y
        self.force_x = force_x
        self.force_y = force_y
        self.moment = moment
        self.DoF = DoF

        frame.joints.append(self) # add joint to list of joints in frame
        self.index = self.nodes.copy()
        self.nodes += 3 

class Member():
    """Class to define each member in the frame. Input the joint number as defined by stiffness method convention."""
    def __init__(self, frame:Struct_Frame, left_joint:int, right_joint:int):
        jointL = frame.joints[left_joint-1]
        jointR = frame.joints[right_joint-1]

        self.index = np.concatenate((jointL.index,jointR.index)) # nodes included in each member

        self.x0 = jointL.location_x
        self.x1 = jointR.location_x
        self.y0 = jointL.location_y
        self.y1 = jointR.location_y

        x = self.x1 - self.x0
        y = self.y1 - self.y0
        l = np.sqrt(x**2 + y**2)
        
        self.length = l
        self.cos = x/l
        self.sin = y/l

        self.k = None # stiffness matrix relative to local axes
        self.K = None # stiffness matrix relative to frame axes
        self.v = None # displacement along member relative to member
        self.u = np.zeros((6,1)) # displacement along member relative to frame axes
        self.Q = np.zeros((6,1)) # local member forces
        self.F = np.zeros((6,1)) # member forces realtive to frame axes
        self.a_stress = None # axial stress in the member
        self.a_strain = None # axial strain in the member
        self.stress_top = np.zeros(100) # bending stress along the member - bottom and top are negative of each other in symmetric beam

        self.trans_disp = np.zeros(100)
        self.axial_disp = np.zeros(100)
        self.disp_x = 0
        self.disp_y = 0

        self.x_pos = np.linspace(self.x0,self.x1,100)
        self.y_pos = np.linspace(self.y0,self.y1,100)

        frame.members.append(self) # add member to list of members in frame

    def member_disp(self, E:float, I:float):
        def mac(x,a):
            if x <= a:
                return 0
            elif x > a:
                return x - a

        C1 = float(self.u[2])
        C2 = float(self.u[1])

        num_points = 100
        x = np.linspace(0,self.length,num_points)
        for i in range(num_points):
            self.trans_disp[i] += (self.Q[1]/6*mac(x[i],0)**3 - self.Q[2]/2*mac(x[i],0)**2 + self.Q[4]/6*mac(x[i],self.length)**3 - self.Q[5]/2*mac(x[i],self.length)**2)/I/E

            self.trans_disp[i] += C1*x[i] + C2

        self.axial_disp = x*self.a_stress/E + self.u[0]

        self.disp_x = -self.sin*self.trans_disp + self.cos*self.axial_disp
        self.disp_y = self.cos*self.trans_disp + self.sin*self.axial_disp

    def transformation_matrix(self):
        """Function to define the transformation matrix for the member"""
        C = self.cos
        S = self.sin

        T = np.array([[C , S , 0 , 0 , 0 , 0],
                      [-S, C , 0 , 0 , 0 , 0],
                      [0 , 0 , 1 , 0 , 0 , 0],
                      [0 , 0 , 0 , C , S , 0],
                      [0 , 0 , 0 ,-S , C , 0],
                      [0 , 0 , 0 , 0 , 0 , 1]])
        return T

    def local_stiff_matrix(self, E:float, A:float, I:float):
        """Function to define the stiffness matrix of the member relative to its own axes"""
        L = self.length

        m = E*I/L**3
        
        k = m*np.array([[A*L**2/I , 0 , 0 , -A*L**2/I , 0 , 0],
                        [0 , 12 , 6*L , 0 , -12 , 6*L],
                        [0 , 6*L , 4*L**2 , 0 , -6*L , 2*L**2],
                        [-A*L**2/I , 0 , 0 , A*L**2/I , 0 , 0],
                        [0 , -12 , -6*L , 0 , 12 , -6*L],
                        [0 , 6*L , 2*L**2 , 0 , -6*L , 4*L**2]])
        return k

    def global_stiff_matrix(self, E:float, A:float, I:float):
        """Function to define the stiffness matrix of the member relative to the global coordinate axes"""
        C = self.cos
        S = self.sin
        L = self.length

        m = E*I/L**3

        K = m*np.array([[A*L**2/I*C**2 + 12*S**2 , (A*L**2/I - 12)*C*S , -6*L*S , -(A*L**2/I*C**2 + 12*S**2) , -(A*L**2/I - 12)*C*S , -6*L*S],
                        [(A*L**2/I - 12)*C*S , A*L**2/I*S**2 + 12*C**2 , 6*L*C , -(A*L**2/I - 12)*C*S , -(A*L**2/I*S**2 + 12*C**2) , 6*L*C],
                        [-6*L*S       ,      6*L*C        ,       4*L**2       ,       6*L*S       ,       -6*L*C       ,       2*L**2],
                        [-(A*L**2/I*C**2 + 12*S**2) , -(A*L**2/I - 12)*C*S , 6*L*S , A*L**2/I*C**2 + 12*S**2 , (A*L**2/I - 12)*C*S , 6*L*S],
                        [-(A*L**2/I - 12)*C*S , -(A*L**2/I*S**2 + 12*C**2) , -6*L*C , (A*L**2/I - 12)*C*S , A*L**2/I*S**2 + 12*C**2 , -6*L*C],
                        [-6*L*S       ,       6*L*C       ,       2*L**2       ,       6*L*S       ,       -6*L*C       ,       4*L**2]])
        return K

"""
Program Input - This is the only section that changes for different frames. Define each joint and member in order according to numbering system
"""
ex2 = Struct_Frame(E=10200, b=1, h=.25)
Joint(ex2, DoF=0, location_x=0, location_y=0)
Joint(ex2, DoF=3, location_x=0, location_y=8, moment=100/1000)
Joint(ex2, DoF=3, location_x=0, location_y=16)
Joint(ex2, DoF=0, location_x=16.25, location_y=0)
Joint(ex2, DoF=3, location_x=16.25, location_y=8)
Joint(ex2, DoF=3, location_x=16.25, location_y=16, force_x=10/1000)

Member(ex2, left_joint=1, right_joint=2)
Member(ex2, left_joint=2, right_joint=3)
Member(ex2, left_joint=5, right_joint=4)
Member(ex2, left_joint=6, right_joint=5)
Member(ex2, left_joint=2, right_joint=5)
Member(ex2, left_joint=3, right_joint=6)

ex2.solve()
ex2.plot_stress_and_strain()
ex2.plot_displacement()