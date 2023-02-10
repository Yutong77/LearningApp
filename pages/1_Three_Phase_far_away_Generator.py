import streamlit as st
import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np
from PIL import Image
st.header("Three-Phase Short Circuit far away Generator")

container_fault = st.container()
fault= st.radio(
    "👇Three Switches:",
    ('OFF', 'ON'), horizontal=True, label_visibility="visible",key='Pb1')
if fault == 'OFF':
    container_fault.markdown(r'''
            Now the model shows power system is operating normally and without faults.
            Turn off the three switches on the line to introduce the fault.
            ''')
    image000 = Image.open('pages/pics/pt_000.1.png')
    container_fault.image(image000)
elif fault == 'ON':
    container_fault.markdown(r'''
            ⚠️ **See the model below, a fault occurs in the power system!**
            ''')
    image111 = Image.open('pages/pics/pt_111.1.png')
    container_fault.image(image111)



    st.markdown(r'''
                 **Fault Identification**\
                📍 Lolation: far away from the generator \
                🔎 Type: three-phase to ground short circuit\
                💭 Question: How does the fault current look like?
                ''')



    # Determine parameters and define functions
    Vn = 110e3                              # Nominal voltage [V]
    E = Vn * np.sqrt(2) / np.sqrt(3)        # Peak phase voltage [V]
    l = 80                                  # Line length [km]
    L = 0.001 * l                          # Line inductance [H]
    R = 0.02 * l                           # Line resistance [Ohm]
    f = 50                                  # Frequency [Hz]
    w = 2*np.pi*f                           # Frequency [rad / s]
    Z = np.sqrt(R**2 + (w*L)**2)            # Impedance (magnitude) [Ohm]


    tau = L/R                               # Time constant [s]
    theta_ideal = np.pi/2                   # pure inductance case
    theta_practical = np.arctan(w*L/R)      # inductance in series with resistance
    N = 10000                               # Number of points used
    t = np.linspace(0, 4*tau, N)            # Time [s]

    # AC voltage source 
    def voltage(t,alpha, E=E):
        y = E*np.sin(w*t+alpha)
        return y

    # Unidirectional component of short circuit current (i_DC)
    def unidirectional(t,alpha, theta , tau = tau, E=E, Z=Z):
        y = - (E/Z)*np.exp(-t/tau) * np.sin(alpha - theta)
        return y

    # Sinusoidal component of short circuit current (i_AC)
    def sinusoidal(t, alpha ,theta, E=E, Z=Z, w=w):
        y = (E/Z)*np.sin(w*t+alpha - theta)
        return y

    # Short circuit current i = i_DC + i_AC
    def TotalCurrent(t,alpha ,theta):
        y = sinusoidal(t,alpha ,theta) + unidirectional(t,alpha ,theta)
        return y

    # interactive input
    container = st.container()
    container.markdown(r'''
                       Let's first assume that the transmission line is purely inductive with no resistance,
                       i.e. $\theta=\pi/2$. 
                       Since we are primarily interested in the worst scenario,
                       which leads to the largest fault current, 
                       we choose the voltage source angle at the occurrence of the short circuit to be $\alpha=(\theta-\pi/2)$.\
                       Because the three phases of the system are symmetrical, 
                       for simplicity, the short-circuit current of only one phase is presented. 
                       Moreover we assume that the system is operating under no-load condition. The corresponding short circuit current plot is shown below.
                       ''')

    st.markdown(r'''
                **Now it's your turn to choose the scenario that you are interested in!**
                '''
                r'''
                👇 Please select source angle $\alpha$ and impedance angle $\theta$ when short circuit occurs.
                ''')
    columns = st.columns([2, 1])
    alpha_in = columns[0].slider("Voltage Source Angle(\N{DEGREE SIGN})", -90, 90, 0)
    theta_in = columns[1].radio('Impedance Angle ',
                        ('ideal case','practical case'))
    if theta_in == "practical case":
        theta = theta_practical
    else:
        theta = theta_ideal
    theta_deg = np.around(theta*180/np.pi, 2)
    expander1 = st.expander("💡Tips")
    expander1.markdown(f'''
                       In the ideal case the line resistance is neglected with an impedance angle of 90\N{DEGREE SIGN}, 
                       while in practice it is taken into account 
                       and the impedance angle is {np.around(theta_practical*180/np.pi,2)}\N{DEGREE SIGN}.
                       '''
                       r'''
                       If you are also interested in the largest fault current, please choose $\alpha=(\theta-\pi/2)$.\
                       Do you want to see the fault current without a DC component, then please set $|\alpha|=\theta$.
                       ''')
    # Current RMS
    # Isc_rms = np.sqrt( (1/np.max(t)) * quad(short_cc_current_squared, 0, np.max(t))[0] )
    # Short circuit current


    # Plot data
    plt.style.use("ggplot")
    fig, ax = plt.subplots()
    ax.plot(t, unidirectional(t,alpha_in*np.pi/180, theta)/1000, color="red", label = "DC component $i_{DC}(t)$")
    ax.plot(t, sinusoidal(t,alpha_in*np.pi/180, theta)/1000, color="green", label = "AC component $i_{AC}(t)$")
    ax.plot(t, TotalCurrent(t,alpha_in*np.pi/180, theta)/1000, color='blue', label = "Total short circuit current $i(t)$")
    # ax.plot(t, voltage(t,alpha_in*np.pi/180)/1e5, color='yellow',linestyle='--', label = "Voltage $v(t)$")
    ax.set_xlim([0, np.max(t)])
    ax.set_ylim([np.min(TotalCurrent(t,alpha_in*np.pi/180, theta))/1000-2, np.max(TotalCurrent(t,alpha_in*np.pi/180, theta))/1000 + 2])
    ax.set_title("Three phase short circuit current")
    ax.legend(loc='upper right')
    ax.set_xlabel("Time in s")
    ax.set_ylabel("Short circuit current in kA")

    container.pyplot(fig)

    # explanation
    st.markdown(r'''
                   📝 **Explanations**
                '''
                r''' 
                   The total fault current is composed of AC component and DC component, 
                   and can be written as
                   ''')
    st.latex(r'''
                i(t)=i_{ac}(t)+i_{dc}(t)\\
                i_{ac}(t)=\frac{\sqrt{2}V_{n}}{\sqrt{3}Z}sin(\omega t+\alpha-\theta)\\\
                i_{dc}(t)=-\frac{\sqrt{2}V_{n}}{\sqrt{3}Z}sin(\alpha-\theta)e^{-t/T}
                ''')
    st.markdown(r'''
                    The AC fault current (also called steady-state fault current), is a sinusoid and equal in amplitude.
                    The DC offset current, decays exponentially with time constant T=L/R. 
                    It appears because the current on the inductor cannot change abruptly.
                    ''')
    st.markdown(r'''
                    The above describes a short circuit that occurs on the transmission line, far from the generator, 
                    so the generator can be equivalent as a voltage source, 
                    then what would the short circuit current look like if the fault occurred close to the generator? 
                    '''
                r'''
                    💡You can use sidebar on the left side to select *Three Phase Generator Outlet* page.
                    ''')
