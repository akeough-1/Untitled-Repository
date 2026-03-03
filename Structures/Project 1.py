import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Beam():
    """Class to store data and functions for a beam. Contains the elastic constants (I would have to change 
    the way this is set up to allow variable geometry) and a list of Joints generated along the beam."""
    def __init__(self, E:float, I:float):
        self.E = E
        self.I = I

        self.joints = []

    def solve_reactions(self):
        """Function to solve for the unknown reaction forces and displacements along the beam using the stiffness method.
        To calculate the global stiffness matrix, I expanded each of the local stiffness matricies to a global size by filling
        in the indicies outside out its members with zeros. The global stiffness matrix S is the sum of all of the local matricies.
        I know this isn't the most efficient way to do it (or the way recommended in the notes), but it's the way that makes the most
        sense to me conceptually and I'm not really constrained by the number of computations for solving this or similar beam problems."""
        
        self.joint_locations = [] # the locations of every joint in the beam
        num_nodes = len(self.joints)*2
        self.loads = np.zeros((num_nodes,1)) 
        self.free_nodes = []
        self.fixed_nodes = []
        node_num = 0

        for joint in self.joints:
            self.joint_locations.append(joint.location)

            if joint.DoF == 0:
                self.fixed_nodes.append(node_num)
                self.fixed_nodes.append(node_num+1)
            elif joint.DoF == 1:
                self.fixed_nodes.append(node_num)
                self.free_nodes.append(node_num+1)
            elif joint.DoF == 2:
                self.free_nodes.append(node_num)
                self.free_nodes.append(node_num+1)
            
            self.loads[node_num] = joint.applied_force
            self.loads[node_num+1] = joint.applied_moment

            node_num+=2 # the loop handles two nodes at a time (two for each joint)

        num_members = len(self.joint_locations) - 1
        self.members = []
        for i in range(0,num_members):
            length = self.joint_locations[i+1] - self.joint_locations[i]
            self.members.append(Member(self.E, self.I, length=length, left_joint=self.joints[i], right_joint=self.joints[i+1]))

        active = np.array([0,4])
        self.S_mat = np.zeros((num_nodes,num_nodes))
        self.k = []
        for member in self.members:
            self.k.append(member.k)
            member.k_global = np.zeros((num_nodes,num_nodes))
            member.k_global[active[0]:active[1],active[0]:active[1]] = member.k
            self.S_mat+=member.k_global
            active+=2

        fixed_array = np.array(self.fixed_nodes)
        self.S_mat = np.delete(np.delete(self.S_mat, fixed_array, axis=0), fixed_array, axis=1)
        self.loads = np.delete(self.loads,fixed_array, axis=0)
        # displactement at each free node
        self.disp = np.linalg.solve(self.S_mat, self.loads)

        self.d_global = np.zeros((num_nodes,1))
        i = 0
        for node in self.free_nodes:
            self.d_global[node] = self.disp[i]
            i+=1

        active = np.arange(4)
        self.u_list = []
        self.Q_global = []
        for i in range(len(self.members)):
            self.members[i].u = self.d_global[active]
            Q_i = self.members[i].k @ self.members[i].u
            Q_i = np.round(Q_i,10)

            self.members[i].Q = Q_i
            self.members[i].u = self.d_global[active]

            Q_global_i = np.zeros((num_nodes,1))
            Q_global_i[active] = Q_i
            self.Q_global.append(Q_global_i)

            active+=2

        self.Q_global = np.array(sum(self.Q_global))

    def calc_disp(self):
        """Function to iteratively calculate the displacement at each point using discontinuity"""
        def mac(x,a):
            """Function to replicate the Macaulay function"""
            if x <= a:
                return 0
            elif x > a:
                return x - a
        
        Q = self.Q_global
        forces = Q[np.arange(0,len(Q),2)]
        moments = Q[np.arange(1,len(Q),2)]

        locations = self.joint_locations

        C1 = float(self.d_global[0])
        C2 = float(self.d_global[1])

        num_points = 100
        displ = np.zeros(num_points)
        x = np.linspace(0,locations[-1],num_points)
        for i in np.arange(num_points):
            for j in np.arange(len(locations)):
                a = locations[j]

                displ[i] += forces[j]/6*mac(x[i],a)**3 - moments[j]/2*mac(x[i],a)**2
            displ[i] += C1*x[i] + C2

        displ /= (self.I*self.E)
        
        plt.plot(displ)
        plt.show
            
    def to_dataframe(self):
        """Function to convert parameters to Pandas DataFrames with the appropriate indicies"""
        for member in self.members:
            member.k = pd.DataFrame(member.k, index=member.k_index, columns=member.k_index)
            member.Q = pd.DataFrame(member.Q, index=member.k_index)
            member.u = pd.DataFrame(member.u, index=member.k_index)
        self.P = pd.DataFrame(self.loads, index=np.arange(1,len(self.loads)+1))
        self.S = pd.DataFrame(self.S_mat, index=np.arange(1,len(self.S_mat)+1), columns=np.arange(1,len(self.S_mat)+1))
        self.d = pd.DataFrame(self.disp, index=[i+1 for i in self.free_nodes])
        self.R = pd.DataFrame(self.Q_global[self.fixed_nodes], index=[i+1 for i in self.fixed_nodes])    

    def print_results(self):
        """Function to print some or all of the parameters to the terminal so I can copy/paste them nicely"""
        for i in np.arange(len(self.members)):
            print(f"\nk{i+1}\n",self.members[i].k)
        
        for i in np.arange(len(self.members)):
            print(f"\nQ{i+1}\n",self.members[i].Q)

        for i in np.arange(len(self.members)):
            print(f"\nu{i+1}\n",self.members[i].u)

        print("\nP\n",self.P)

        print("\nS\n",self.S)

        print("\nDisplacement\n",self.d)

        print("\nReactions\n",self.R)      

class Joint():
    """Class to create a new joint in a beam. Place a joint at any location where there is a support, applied moment, 
    or change in geometry. The class stores the location, degrees of freedom and the applied self.loads at the locatio (if any)
    and adds itself to a list of joints in the beam it is defined in"""
    def __init__(self, beam:Beam, location:float, DoF:int, applied_force:float=0, applied_moment:float=0):
        self.location = location
        self.applied_force = applied_force
        self.applied_moment = applied_moment
        self.DoF = DoF
        # if there is only one degree of freedom, it has to be vertical - can't restrict rotation without restricting displacement

        beam.joints.append(self)

class Member(Beam):
    """Class to define a member between two joints. Automatically generated as a part of the beam solver. 
    Contains the member length, the joints on either end, and the local stiffness matrix"""

    global_k_index = np.arange(1,5)

    def __init__(self, E:float, I:float, length:float, left_joint:Joint, right_joint:Joint):
        super().__init__(E, I)
        self.L = length
        self.JointL = left_joint
        self.JointR = right_joint

        self.k = self.stiff_mat()
        self.k_global = self.k
        self.k_index = self.global_k_index.copy()
        self.global_k_index+=2

        self.Q = np.zeros((1,4))
        self.u = np.zeros((1,4))
    
    def stiff_mat(self):
        """ Function to generate the local stiffness matrix of the member. This is only called in the __init__ 
        function but I felt weird about including this block there. Also, I might create a separate function 
        in this class to generate the 6x6 required for frame analysis."""
        s = self.E*self.I/self.L**3
        mat = np.array([[12, 6*self.L, -12, 6*self.L],
                        [6*self.L, 4*self.L**2, -6*self.L, 2*self.L**2],
                        [-12, -6*self.L, 12, -6*self.L],
                        [6*self.L, 2*self.L**2, -6*self.L, 4*self.L**2]])
        
        k = s*mat
        return k


"""Program Input - this is the only part that changes for different beams"""

project1 = Beam(E = 150e6, I = 500e-6)

# Create a joint by calling the Joint class
Joint(project1, location=0, DoF=0)
Joint(project1, location=20/5, DoF=1, applied_moment=100)
Joint(project1, location=20*2/5, DoF=2, applied_force=-350)
Joint(project1, location=20*3/5, DoF=1, applied_moment=-100)
Joint(project1, location=20*4/5, DoF=1)
Joint(project1, location=20, DoF=2, applied_force=-200)

# Run the solver and print the results to the terminal
project1.solve_reactions()
project1.calc_disp()