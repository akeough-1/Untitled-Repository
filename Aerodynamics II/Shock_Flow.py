import sys

class Shock():
    def __init__(self, gamma:float=1.4, M1:float=None, M2:float=None,
                 P_ratio:float=None, T_ratio:float=None, rho_ratio:float=None):
        
        self.ga = gamma
        
        # if no value is input for M1, calculate that first
        if not M1:
            if M2:
                self.M1 = self.calc_M(M2)
            elif P_ratio:
                self.M1 = ((P_ratio - 1)*(self.ga + 1)/(2*self.ga) + 1)**0.5
            elif rho_ratio:
                self.M1 = (2*rho_ratio/((self.ga - 1)*rho_ratio - (self.ga + 1)))**0.5
            else:
                print("Error: insufficient inputs")
                sys.exit()
        else:
            self.M1 = float(M1)

        # use M1 to calculate all other values (even if already input)
        self.M2 = self.calc_M(self.M1)
        self.P_ratio = 1 + 2*self.ga/(self.ga + 1)*(self.M1**2 - 1)
        self.T_ratio = (1 + 2*self.ga/(self.ga + 1)*(self.M1**2 - 1))*(2 + (self.ga - 1)*self.M1**2)/((self.ga + 1)*self.M1**2)
        self.rho_ratio = ((self.ga + 1)*self.M1**2)/(2 + (self.ga - 1)*self.M1**2)

        # it would be pretty sick if you could like check extra input values

        self.vals = {
            "M1":self.M1,
            "M2":self.M2,
            "P_ratio":self.P_ratio,
            "T_ratio":self.T_ratio,
            "rho_ratio":self.rho_ratio,
        }
    
    def calc_M(self,M:float) -> float:
        """input M1 or M2 the equation is the same :)"""
        return ((1 + ((self.ga - 1)/2)*M**2)/(self.ga*M**2 - (self.ga - 1)/2))**0.5
    
    def __repr__(self) -> str:
        M1 = round(self.M1,4)
        M2 = round(self.M2,4)
        P_ratio = round(self.P_ratio,4)
        T_ratio = round(self.T_ratio,4)
        rho_ratio = round(self.rho_ratio,4)
        return f"\nM1 = {M1},\nM2 = {M2},\nP2/P1 = {P_ratio},\nT2/T1 = {T_ratio},\nrho2/rho1 = {rho_ratio}\n"
