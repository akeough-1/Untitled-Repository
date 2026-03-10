import sys
import numpy as np
from scipy.optimize import fsolve

def val_print(obj,atr_name:str,precision:int,unit_str:str=""):
    try:
        value = getattr(obj,atr_name)
    except AttributeError:
        raise AttributeError(f"atr_name {atr_name} not in obj {obj}. ")
    
    value = round(value,precision)
    print(f"{atr_name} = {value} {unit_str}")

class Constants():
    R = 1
    Cp = 7/2*R
    Cv = 5/2*R
    gamma = 7/5

class Metric_Constants(Constants):
    R = 287
    R_units = "J/kg/K"
    Cp = 7/2*R
    Cv = 5/2*R
    gamma = 7/5

    def atm2Pa(P:float) -> float:
        return P*101325
    
    def Pa2atm(P:float) -> float:
        return P/101325
    
class Imperial_Constants(Constants):
    R = 1716
    R_units = "ft*lb/lbm/K"
    Cp = 7/2*R
    Cv = 5/2*R
    gamma = 7/5

    def atm2lbf(P:float) -> float:
        return P*101325*0.020886
    
    def lbf2atm(P:float) -> float:
        return P/101325/0.020886

# h2 - h1 = Cp*(T2 - T1)
# e2 - e1 = Cv*(T2 - T1)
# s2 - s1 = Cp*ln(T2/T1) - R*ln(P2/P1) = Cv*ln(T2/T1) + R*ln(rho1/rho2)

# P2/P1 = (rho2/rho1)^gamma = (T2/T1)^(gamma/(gamma-1))

def calculate_ideal_gas(units:str,pressure:float=None,density:float=None,temp:float=None) -> float:
    """units = \"metric\" or \"imperial\""""
    input_err = False
    if pressure == None and density == None:
        input_err = True
    if pressure == None and temp == None:
        input_err = True
    if density == None and temp == None:
        input_err = True
    if pressure == None and density == None and temp == None:
        input_err = True

    if input_err == True:
        raise ValueError("Must input at least two units")

    if units == "metric":
        R = 287
        P_units = "Pa"
        rho_units = "kg/m^3"
        t_units = "K"
    elif units == "imperial":
        R = 1716
        P_units = "lb/ft^2"
        rho_units = "slug/ft^3"
        t_units = "R"

    else:
        raise ValueError("Error: units must be \"metric\" or \"imperial\"")

    if pressure == None:
        pressure = density*R*temp
        #print(f"P = {pressure} "+P_units)
        return pressure
    if density == None:
        density = pressure/R/temp
        #print(f"rho = {density} "+rho_units)
        return density
    if temp == None:
        temp = pressure/R/density
        #print(f"T = {temp} "+t_units)
        return temp

def vel2mach(R:float,velocity:float,temp:float) -> float:
    a = (1.4*R*temp)**0.5
    Mach = velocity/a
    return Mach

def mach2vel(R:float,mach:float,temp:float) -> float:
    a = (1.4*R*temp)**0.5
    vel = mach*a
    return vel

class Isentropic_Flow():
    def __init__(self,gamma:float=1.4,M:float=None,P_ratio:float=None,rho_ratio:float=None,T_ratio:float=None,
                 P1:float=None,rho1:float=None,T1:float=None):
        """Requires one of M, P_ratio, rho_ratio, or T_ratio.
        Inputing P1, rho1, and/or T1 will output P0, rho0, and/or T0"""

        self.ga = gamma

        if M:
            self.M = M
            self.rho_ratio = (1 + M**2/5)**(5/2)
            self.P_ratio = (1 + M**2/5)**(7/2)
            self.T_ratio = (1 + (gamma-1)/2*M**2)

        elif P_ratio:
            self.P_ratio = P_ratio
            self.M = (5*((P_ratio)**(2/7) - 1))**0.5
            self.rho_ratio = (1 + M**2/5)**(5/2)
            self.T_ratio = (1 + (gamma-1)/2*M**2)

        elif rho_ratio:
            self.rho_ratio = rho_ratio
            self.M = (5*((rho_ratio)**(2/5) - 1))**0.5
            self.P_ratio = (1 + M**2/5)**(7/2)
            self.T_ratio = (1 + (gamma-1)/2*M**2)

        elif T_ratio:
            self.T_ratio = T_ratio
            self.M = (2/(gamma - 1)*(T_ratio - 1))**0.5
            self.rho_ratio = (1 + M**2/5)**(5/2)
            self.P_ratio = (1 + M**2/5)**(7/2)

        else:
            print("ERROR: insuficient inputs")
            sys.exit()

        if P1:
            self.P0 = self.P_ratio*P1
        else:
            self.P0 = None

        if rho1:
            self.rho0 = self.rho_ratio*rho1
        else:
            self.rho0 = None

        if T1:
            self.T0 = self.T_ratio*T1
        else:
            self.T0 = None

    def __repr__(self) -> str:
        M = round(self.M,4)
        P_ratio = round(self.P_ratio,4)
        rho_ratio = round(self.rho_ratio,4)
        T_ratio = round(self.T_ratio,4)
        return f"\nM = {M}\nP0/P = {P_ratio}\nrho0/rho = {rho_ratio}\nT0/T = {T_ratio}\n"

class Oblique_Shock():
    def __init__(self, units:str, M1:float, gamma:float=1.4, wave_angle_beta:float=None, calc_strong_beta:bool=False,
                 defl_angle_theta:float=None, M2:float=None, P_ratio:float=None, rho_ratio:float=None, P1:float=None,
                 P0_1:float=None,T1:float=None,T0_1:float=None,rho1:float=None):
        """\"units\" = \"metric\" or \"imperial\"\n
        All angles in radians"""

        self.ga = gamma

        if units == "metric":
            Cp = Metric_Constants.Cp
            R = Metric_Constants.R
        elif units == "imperial":
            Cp = Imperial_Constants.Cp
            R = Imperial_Constants.R
        else:
            raise ValueError("Must input units as \"metric\" or \"imperial\"")

        if wave_angle_beta is None and defl_angle_theta is None:
            if P_ratio is not None:
                M1n = ((P_ratio - 1)*(self.ga + 1)/(2*self.ga) + 1)**0.5
            elif rho_ratio is not None:
                M1n = (2*rho_ratio/((self.ga - 1)*rho_ratio - (self.ga + 1)))**0.5
                
            else:
                raise ValueError("Need pressure or density ratio if no angle input")
            
            self.beta = np.asin(M1n/M1) #rad
            M2n = self.calc_M(self.ga,M1n)
            self.theta = self.theta_beta_M_rel(self.ga, beta=self.beta, M1=M1)

        elif wave_angle_beta is not None:
            self.beta = wave_angle_beta
            M1n = M1*np.sin(self.beta)
            M2n = self.calc_M(self.ga,M1n)
            self.theta = self.theta_beta_M_rel(self.ga, beta=self.beta, M1=M1)

        elif defl_angle_theta is not None:
            self.theta = defl_angle_theta

            # check to make sure input theta is within maximum possible value
            theta_max = self.calc_theta_max(M1,gamma)
            if self.theta > theta_max:
                theta = round(np.rad2deg(self.theta),3)
                theta_max = round(np.rad2deg(theta_max),3)
                raise ValueError(f"Deflection angle theta ({theta} deg) is greater than theta_max ({theta_max} deg): shock detatched")
            
            self.beta = self.theta_beta_M_rel(self.ga, theta=self.theta, M1=M1)
            M1n = M1*np.sin(self.beta)
            M2n = self.calc_M(self.ga,M1n)

        # use M1 to calculate all other values (even if already input)
        self.P_ratio = 1 + 2*self.ga/(self.ga + 1)*(M1n**2 - 1)
        self.T_ratio = (1 + 2*self.ga/(self.ga + 1)*(M1n**2 - 1))*(2 + (self.ga - 1)*M1n**2)/((self.ga + 1)*M1n**2)
        self.rho_ratio = ((self.ga + 1)*M1n**2)/(2 + (self.ga - 1)*M1n**2)

        self.ds = Cp*np.log(self.T_ratio) - R*np.log(self.P_ratio)
        self.P0_ratio = np.exp(-self.ds/R)
        self.T0_ratio = 1

        self.M1 = M1
        self.M2 = M2n/np.sin(self.beta - self.theta)
        self.mu = np.atan(1/((M1**2 - 1)**0.5)) # Mach Angle

        # calculating values across shock based on user input
        # neglecting the else statements causing problems with subclassing
        if P1 is not None:
            self.P2 = self.P_ratio*P1
        else:
            self.P2 = None

        if P0_1 is not None:
            self.P0_2 = self.P0_ratio*P0_1
        else:
            self.P0_2 = None

        if T1 is not None:
            self.T2 = self.T_ratio*T1
        else:
            self.T2 = None

        if T0_1 is not None:
            self.T0_2 = self.T0_ratio*T0_1
        else:
            self.T0_2 = None

        if rho1 is not None:
            self.rho2 = self.rho_ratio*rho1
        else:
            self.rho2 = None
    
    @staticmethod
    def calc_M(gamma:float,M:float) -> float:
        """input M1 or M2 the equation is the same :)"""
        return ((1 + ((gamma - 1)/2)*M**2)/(gamma*M**2 - (gamma - 1)/2))**0.5
    
    @staticmethod
    def theta_beta_M_rel(gamma:float,M1:float,theta:float=None,beta:float=None,calc_strong_beta:bool=False) -> float:
        if theta is None and beta is None:
            raise ValueError("Must provide theta or beta")
        
        if theta is None:
            theta = np.atan(2/np.tan(beta) * (M1**2*np.sin(beta)**2 - 1)/(M1**2*(gamma + np.cos(2*beta)) + 2))
            return theta

        else:
            def residual(beta,theta,M1):
                return (theta - np.atan(2/np.tan(beta) * (M1**2*np.sin(beta)**2 - 1)/(M1**2*(gamma + np.cos(2*beta)) + 2)))
            
            if calc_strong_beta is False:
                start = 0.01 # don't start at zero or you get division by zero error
            else:
                start = np.pi - 0.01

            sol = fsolve(residual, x0=start, args=(theta,M1))

            # sometimes it outputs a 0D array that isn't recognized as 0D? idk why but this fixes it
            if type(sol) is np.ndarray:
                sol = sol[0]
            return sol
        
    @staticmethod
    def calc_theta_max(M1:float,gamma:float=1.4) -> float:
        new_theta = 0

        for beta in np.linspace(np.pi/2,0,50):
            old_theta = new_theta
            new_theta = np.atan(2/np.tan(beta) * (M1**2*np.sin(beta)**2 - 1)/(M1**2*(gamma + np.cos(2*beta)) + 2))
            if new_theta < old_theta:
                new_theta = old_theta
                break

        # create enough of a gap to overcome previous small step size
        new_beta = beta + 0.05
        new_theta = np.atan(2/np.tan(beta) * (M1**2*np.sin(beta)**2 - 1)/(M1**2*(gamma + np.cos(2*beta)) + 2))

        for beta in np.linspace(new_beta,0,10000):
            old_theta = new_theta
            new_theta = np.atan(2/np.tan(beta) * (M1**2*np.sin(beta)**2 - 1)/(M1**2*(gamma + np.cos(2*beta)) + 2))
            if new_theta < old_theta:
                theta_max = old_theta
                break

        return theta_max

    # using print() on a shock object executes the following:
    def __repr__(self) -> str:
        M1 = round(self.M1,4)
        M2 = round(self.M2,4)
        mu = round(self.mu,4)
        theta = round(self.theta,4)
        beta = round(self.beta,4)
        P_ratio = round(self.P_ratio,4)
        T_ratio = round(self.T_ratio,4)
        rho_ratio = round(self.rho_ratio,4)
        entropy = round(self.ds,4)
        P0_ratio = round(self.P0_ratio,4)
        T0_ratio = round(self.T0_ratio,4)

        base_str = f"\nM1 = {M1}\nM2 = {M2}\nMach Angle mu = {mu}\ndefl angle theta = {theta}\nwave angle beta = {beta}\nP2/P1 = {P_ratio}\n"
        base_str += f"T2/T1 = {T_ratio}\nrho2/rho1 = {rho_ratio}\ns2 - s1 = {entropy}\nP0_2/P0_1 = {P0_ratio}\nT0_2/T0_1 = {T0_ratio}"

        if self.P2 is not None:
            P2 = round(self.P2,4)
            base_str += f"\nP2 = {P2}"
        if self.P0_2 is not None:
            P0_2 = round(self.P0_2,4)
            base_str += f"\nP0_2 = {P0_2}"
        if self.T2 is not None:
            T2 = round(self.T2,4)
            base_str += f"\nT2 = {T2}"
        if self.T0_2 is not None:
            T0_2 = round(self.T0_2,4)
            base_str += f"\nT0_2 = {T0_2}"
        if self.rho2 is not None:
            rho2 = round(self.rho2,4)
            base_str += f"\nrho2 = {rho2}"

        return base_str
        
class Normal_Shock(Oblique_Shock):
    def __init__(self, units:str, gamma:float=1.4, M1:float=None, M2:float=None,
                 P_ratio:float=None, rho_ratio:float=None, P1:float=None,
                 P0_1:float=None,T1:float=None,T0_1:float=None,rho1:float=None):
        """\"units\" = \"metric\" or \"imperial\"\n
        All angles in radians"""

        self.ga = gamma
        beta = np.pi/2 # 90 degree wave angle (normal)

        if M1 is None:
            if M2 is not None:
                M1 = self.calc_M(self.ga,M2)
            elif P_ratio is not None:
                M1 = ((P_ratio - 1)*(self.ga + 1)/(2*self.ga) + 1)**0.5
            elif rho_ratio is not None:
                M1 = (2*rho_ratio/((self.ga - 1)*rho_ratio - (self.ga + 1)))**0.5
            else:
                raise ValueError("Insufficient inputs")
        
        # call Oblique_Shock __init__ with beta = 90 deg
        super().__init__(units, M1, self.ga, wave_angle_beta=beta, M2=M2, P_ratio=P_ratio,
                         rho_ratio=rho_ratio, P1=P1, P0_1=P0_1, T1=T1,
                         T0_1=T0_1, rho1=rho1)

def pitot_tube(supersonic:bool=False,gamma:float=1.4,M:float=None,stagnation_P:float=None,
               static_P:float=None,P_ratio:float=None) -> float:
    """If input M, output P_02/P1\n
    Else output M"""
    if supersonic == False:
        if M:
            P_ratio = (1 + (gamma - 1)/2*M**2)**(gamma/(gamma - 1))
            return P_ratio
        
        elif (stagnation_P != None and static_P != None) or P_ratio != None:
            if P_ratio == None:
                P_ratio = stagnation_P/static_P           
            M = (2/(gamma - 1)*(P_ratio**((gamma - 1)/gamma) - 1))**0.5
            return M
        
        else:
            raise ValueError("Insufficient inputs")

    elif supersonic == True:
        if M:
            P_ratio = (((gamma + 1)**2*M**2)/(4*gamma*M**2 - 2*(gamma - 1)))**(gamma/(gamma - 1)) * (1 - gamma + 2*gamma*M**2)/(gamma + 1)
            return P_ratio
        
        elif (stagnation_P != None and static_P != None) or P_ratio != None:
            from scipy.optimize import fsolve
            if P_ratio == None:
                P_ratio = stagnation_P/static_P

            def residual(M,gamma,P_ratio):
                return (((gamma + 1)**2*M**2)/(4*gamma*M**2 - 2*(gamma - 1)))**(gamma/(gamma - 1)) * (1 - gamma + 2*gamma*M**2)/(gamma + 1) - P_ratio
            
            return fsolve(residual, x0=1, args=(gamma,P_ratio))
        
        else:
            raise ValueError("Insufficient inputs")
    else:
        raise TypeError("Input \"supersonic\" must be True or False")
    
class Expansion_Fan():
    """requirements:
    input M1 and theta
    ouput M2, mu1, mu2, isentropic ratios before & after, P2/P1, T2/T1, rho2/rho1 before & after
    program gives the right answer"""
    def __init__(self,units:str,M1:float,defl_angle_theta:float=None,gamma:float=1.4,
                 P1:float=None,T1:float=None,rho1:float=None,
                 P2:float=None,T2:float=None,rho2:float=None):
        """If input P1, T1, and/or rho1, make sure they are in SI units (or Imperial equiv)"""
        if defl_angle_theta is not None:
            self.M1 = M1
            self.theta = defl_angle_theta
            self.gamma = gamma

            self.nu1 = self.calc_nu(self.M1,self.gamma)
            self.nu2 = self.theta + self.nu1

            def residual(M,theta,nu1,ga):
                nu2 = self.calc_nu(M,ga)
                zero = nu2 - nu1 - theta
                return zero
            
            self.M2 = fsolve(residual, x0=self.M1, args=(self.theta,self.nu1,self.gamma))[0]

            self.mu1 = np.atan(1/(self.M1**2 - 1)**0.5)
            self.mu2 = np.atan(1/(self.M2**2 - 1)**0.5)

            state1 = Isentropic_Flow(self.gamma,self.M1)
            state2 = Isentropic_Flow(self.gamma,self.M2)
            
            self.P0_ratio1 = state1.P_ratio
            self.P0_ratio2 = state2.P_ratio
            self.P_ratio = self.P0_ratio1/self.P0_ratio2

            self.T0_ratio1 = state1.T_ratio
            self.T0_ratio2 = state2.T_ratio
            self.T_ratio = self.T0_ratio1/self.T0_ratio2

            self.rho0_ratio1 = state1.rho_ratio
            self.rho0_ratio2 = state2.rho_ratio
            self.rho_ratio = self.rho0_ratio1/self.rho0_ratio2

            if P1 and T1 and not rho1:
                rho1 = calculate_ideal_gas(units,pressure=P1,temp=T1)
            elif T1 and rho1 and not P1:
                P1 = calculate_ideal_gas(units,temp=T1,density=rho1)
            elif P1 and rho1 and not T1:
                T1 = calculate_ideal_gas(units,pressure=P1,density=rho1)

            if P1 is not None:
                self.P1 = P1
                self.P2 = self.P_ratio*P1
                self.P0 = self.P0_ratio1*P1

            if T1 is not None:
                self.T1 = T1
                self.T2 = self.T_ratio*T1
                self.T0 = self.T0_ratio1*T1

            if rho1 is not None:
                self.rho1 = rho1
                self.rho2 = self.rho_ratio*rho1
                self.rho0 = self.rho0_ratio1*rho1

        elif P2 is not None:
            self.M1 = M1
            self.P1 = P1
            self.P2 = P2
            state1 = Isentropic_Flow(self,gamma,M=self.M1,P1=self.P1)
            self.P0 = state1.P_ratio*self.P1
            self.P0_ratio1 = self.P0/self.P1
            self.P0_ratio2 = self.P0/self.P2
            
            state2 = Isentropic_Flow(self.gamma,P_ratio=self.P0_ratio2)
            self.M2 = state2.M

            self.nu1 = self.calc_nu(self.M1,self.gamma)
            self.nu2 = self.calc_nu(self.M2,self.gamma)
            
            self.theta = self.nu2 - self.nu1

            if T1 is not None:
                self.T1 = T1
                self.T2 = self.T_ratio*T1
                self.T0 = self.T0_ratio1*T1

            if rho1 is not None:
                self.rho1 = rho1
                self.rho2 = self.rho_ratio*rho1
                self.rho0 = self.rho0_ratio1*rho1
        
    def calc_nu(self,M:float) -> float:
        g = self.gamma
        return ((g + 1)/(g - 1))**0.5 * np.atan(((g - 1)/(g + 1)*(M**2 - 1))**0.5) - np.atan((M**2 - 1)**0.5)

    def __repr__(self):
        out_str = ""
        for atr in self.__dict__:
            out_str += f"{atr} = {round(float(getattr(self,atr)),4)}\n"
        return out_str