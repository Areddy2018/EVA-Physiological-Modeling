import numpy as np
import matplotlib.pyplot as plt

# Returns walking speed in km/hr given slope angle
# Modified to return 2 km/hr instead of 5 km/hr at 0 slope
def tobler(slopeAngle):
    dh_dx = np.tan(slopeAngle*(np.pi/180))
    # Add factor to modify expression to 2 km/hr for level walking
    modification_factor = 2/5
    walking_speed = 6*modification_factor*np.exp(-3.5*abs(dh_dx + 0.05))
    
    return(walking_speed,dh_dx)

# Energy expenditure (metabolic rate) using Modified Load Carrying Decision Aid (LCDA) walking equation
# Returns metabolic rate as W
def energyExpenditure(payload_weight, walking_speed, dh_dx):
    # Surface grade as percentage
    G = 100*dh_dx
    # Walking speed as m/s
    S = walking_speed*(5/18)
    energy_expenditure = (1.44 + 1.94*S**0.43 + 0.24*S**4 + 0.34*S*G*(1 - 1.05**(1 - 1.1**(G + 32))))*payload_weight
    # Reduced energy expenditure due to partial gravity: https://pubmed.ncbi.nlm.nih.gov/1490989/#:~:text=When%20gravity%20is%20reduced%20by,at%20low%20levels%20of%20gravity.
    # Assume walking and not running
    reduced_energy_expenditure = (2/3)*energy_expenditure
    # 1 Watt = 1 Joule per second
    # Convert Watt --> Joule/second --> kcal/second
    metabolic_rate = reduced_energy_expenditure/4184
    
    return metabolic_rate

# Return O2 consumption based on metabolic rate in liters
# 5 kcal of energy liberated by body to consume 1 liter of O2
def o2Consumption(metabolic_rate, dt):
    # Respiratory quotient: https://www.lpi.usra.edu/lunar/ALSEP/pdf/31111000673366.pdf (cite)
    literConversion = 1/5
    # Time step dt in seconds
    o2_consumption = metabolic_rate*literConversion*dt
    
    return o2_consumption

# Remaining O2 in liters based on current amount and consumption
def remainingO2(current_O2, o2_consumption):
    remainingO2 = current_O2 - o2_consumption

    return remainingO2

def timeElapsed(currentTimeElapsed, dt):
    
    return currentTimeElapsed + dt

# TODO: determine actual O2 storage of PLSS tanks
