import os
import math
import sys

g = 9.81
radian = math.pi/180
h = 7
Hs_zero = 5
Foreshore_slope = 1 / 20
Ts = 9
S = 2
Gamma_s = 2.7
Gamma_w = 1
alfa = 0.5
Kd_breaking = 2
Kd_nonbreaking = 4
Kr = 1
P = 0.4
StormDuration = 6

def main():
    Hudson()
    VanderMeer()

def Hudson():
    L_zero = 1.56 * (Ts ** 2)
    h_over_Lzero = h / L_zero
    
    print(f"\nHudson's Methodology:")

    try:
        Ks = float(input(f"(h/L_zero = {h_over_Lzero}) For Hudson Method Enter Ks Value: "))
        os.system("cls")
    except:
        print("Ks can be just a number, check it.")
        sys.exit(1)
        
    Hs_toe_Hudson = Hs_zero * Ks * Kr

    BreakingCondition = ""
    W_50 = 0
    
    if Hs_toe_Hudson / h < 0.6:
        BreakingCondition = "Non Breaking Waves"
        Hs_design = 1.27 * Hs_toe_Hudson
        Kd = Kd_nonbreaking
        W_50 = (Gamma_s * Hs_design ** (3) * alfa) / (((Gamma_s / Gamma_w ) - 1) ** (3) * Kd)
    else:
        BreakingCondition = "Breaking Waves"
        Hs_design = 0.78 * h
        Kd = Kd_breaking
        W_50 = (Gamma_s * Hs_design ** (3) * alfa) / (((Gamma_s / Gamma_w ) - 1) ** (3) * Kd)
    print(f"\nHudson's Methodology => Design Condition: {BreakingCondition} , Design Wave Height: {Hs_design} m , Stability Coefficient: {Kd} and Armor Stone Weight (W_50)= {W_50} t\n")

def VanderMeer():
    Tp = 1.05 * Ts
    L_zero_p = 1.56 * Tp ** 2
    S_zero_p = Hs_zero / L_zero_p
    h_over_Lzero_p = h / L_zero_p

    print(f"\nVan der Meer's Methodology:")
    print(f"\nForeshore Slope (Sea Bed Slope) = {Foreshore_slope} m")
    print(f"S_zero_p = {S_zero_p}")
    print(f"h_over_Lzero_p = {h_over_Lzero_p}")

    Hs_toe_VanDerMeer_over_h = float(input("\nEnter Interpolated Hs_toe/h value obtained from energy decay charts: "))
    Hs_toe_VanDerMeer = Hs_toe_VanDerMeer_over_h * h

    global VanDerMeerApproachCheck
    VanDerMeerApproachCheck = h / Hs_toe_VanDerMeer
    print(f"Check whether h/Hs_toe value smaller or higher than 3. Usually, we use Van der Meer Approach if the value is higher than 3 => h/Hs_toe: {VanDerMeerApproachCheck}")
    Tm = 0.81 * Ts
    Psi_m = alfa / (((2 * math.pi / g) * Hs_toe_VanDerMeer / Tm ** 2) ** (1/2))
    Psi_cr = (6.2 * P ** (0.31) * alfa ** (1/2)) ** (1 / (P + 0.5))
    N = StormDuration * 3600 / Tm

    if Psi_m < Psi_cr:
        D_50 = Hs_toe_VanDerMeer / (((Gamma_s / Gamma_w) - 1) * 6.2 * P ** (0.18) * (S / (N) ** (1/2)) ** (0.2) * Psi_m ** (-0.5))
        W_50 = Gamma_s * D_50 ** 3
        print(f"\nVan der Meer's Methodology => Type of Breaking: Plunging, D_50 = {D_50} m and Armor Stone Weight (W_50)= {W_50} t")
    else :
        D_50 = Hs_toe_VanDerMeer / (((Gamma_s / Gamma_w) - 1) * 1 * P ** (-0.13) * (S / (N) ** (1/2)) ** (0.2) * alfa ** (1/2) * Psi_m ** P)
        W_50 = Gamma_s * D_50 ** 3
        print(f"\nVan der Meer's Methodology => Type of Breaking: Surging, D_50 = {D_50} m and Armor Stone Weight (W_50)= {W_50} t")
    
    Entered_W_50_filter = float(input("\nEnter the Weight of Armor Stone (W_50) to Calculate Weight of Filter: "))
    W_50_filter_min = Entered_W_50_filter / 15
    W_50_filter_max = Entered_W_50_filter / 10

    print(f"\nMaximum weight of the filter (W_50_filter_max)= {W_50_filter_max} t and Minimum weight of the filter (W_50_filter_min)= {W_50_filter_min} t")
    Selected_W_50_filter = float(input("\nEnter the Selected Weight of Filter Unit to Calculate Weight of Core: "))
    W_50_core_min = Selected_W_50_filter / 25
    W_50_core_max = Selected_W_50_filter / 10

    print(f"Maximum weight of the core (W_50_core_max)= {W_50_core_max} t and Minimum weight of the core (W_50_core_min)= {W_50_core_min} t")
    W_50_for_thickness = float(input("\nEnter the Weight of Armour Stone for Average Thickness Calculation: "))
    thickness = 2 * 1 * ( W_50_for_thickness / Gamma_s ) ** (1/3)
    
    print(f"Average thickness for selected stone = {thickness} m")
    W_50_for_B = float(input("\nEnter the Weight of Armour Stone for Minimum Crest Width: "))
    B = 2 * 1 * ( W_50_for_B / Gamma_s ) ** (1/3)
    
    print(f"Minimum crest width for rock = {B} m")
    

if __name__ == "__main__":
    main()