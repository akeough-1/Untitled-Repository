class Isentropic_Flow():

    @staticmethod
    def calculate_values(input_var:str,value:float) -> list | None:
        gamma = 1.4

        if input_var == "M":
            M = value
            rho_ratio = (1 + M**2/5)**(5/2)
            P_ratio = (1 + M**2/5)**(7/2)
            T_ratio = (1 + (gamma-1)/2*M**2)
        
        elif input_var == "rho":
            rho_ratio = value
            M = (5*((rho_ratio)**(2/5) - 1))**0.5
            P_ratio = (1 + M**2/5)**(7/2)
            T_ratio = (1 + (gamma-1)/2*M**2)
        
        elif input_var == "P":
            P_ratio = value
            M = (5*((P_ratio)**(2/7) - 1))**0.5
            rho_ratio = (1 + M**2/5)**(5/2)
            T_ratio = (1 + (gamma-1)/2*M**2)
        
        elif input_var == "T":
            T_ratio = value
            M = (2/(gamma - 1)*(T_ratio - 1))**0.5
            rho_ratio = (1 + M**2/5)**(5/2)
            P_ratio = (1 + M**2/5)**(7/2)
        
        else:
            print("Error: input str not recognized")
            return None
        
        output = [M,rho_ratio,P_ratio,T_ratio]
        for i in range(4):
            val = round(output[i],3)
            output[i] = val
        return output

    @staticmethod
    def command_interface():
        cmd_input = input("Enter M, rho, P, or T then value (rho = 4.12): ")
        cmd_input = cmd_input.replace(" ","")

        for i in range(1,len(cmd_input)):
            if cmd_input[i] == "=":
                sep_index = i
                break

            if i >= len(cmd_input) - 1:
                print("Error: input requires '=' symbol")
                return None

        input_var = cmd_input[0:sep_index]
        value = float(cmd_input[sep_index+1:])

        M,rho_ratio,P_ratio,T_ratio = Isentropic_Flow.calculate_values(input_var,value)
        print(f"M = {M}, rho_0/rho = {rho_ratio}, P_0/P = {P_ratio}, T_0/T = {T_ratio}")

if __name__ == "__main__":
    Isentropic_Flow.command_interface()