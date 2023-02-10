import streamlit as st
import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np
from PIL import Image

st.header("Three-Phase Short Circuit at Generator Outlet")

st.markdown(r'''
            ⚠️ **See the model below, now a fault occurs near the generator!**
            ''')
image111 = Image.open('pages/pics/Gen.png')
st.image(image111)
st.markdown(r'''
             **Fault Identification**\
            📍 Lolation: at the terminal of a synchronous generator\
            🔎 Type: three-phase to ground short circuit\
            💭 Question: How does the fault current look like?
            ''')
Vn = 110e3                              # Nominal voltage [V]
E = Vn * np.sqrt(2) / np.sqrt(3)        # Peak phase voltage [V]
f = 50                                  # Frequency [Hz]
w = 2*np.pi*f                           # Frequency [rad / s]
Xd=1.5                                  # Direct axis synchronous reactance
Xd1 = 0.18                              # Direct axis transient reactance
Xd2 = 0.12                              # Direct axis subtransient reactance
Ta = 100e-3                             # Armature time constant
Td1 = 1                                 # Direct axis short circuit transient time constant
Td2 = 75e-3                             # Direct axis hort circuit subtransient time constant
Theta = np.pi/2                         # Impedence angle; Assume pure inductive case
N = 12000                               # Number of points used
t = np.linspace(0, 1.2*Td1, N)            # Time [s]

# DC current (i_DC)
def DirectCurrent(t,Alpha,Ta=Ta,Xd=Xd,E=E,Theta=Theta):
    y = (E/Xd2) * np.exp(-t/Ta) * np.sin(Theta-Alpha)
    return y

# Subtransient component of AC current (i"_AC)
def SubtransientCurrent(t, Alpha,Td2=Td2, Xd2=Xd2, Xd1=Xd1, E=E,  Theta=Theta, w=w):
    y = E * (1/Xd2 - 1/Xd1) * np.exp(-t/Td2) * np.sin(w*t+Alpha-Theta)
    return y

# Transient component of AC current (i'_AC)
def TransientCurrent(t, Alpha, Td1=Td1, Xd1=Xd1, Xd=Xd, E=E, Theta=Theta, w=w):
    y = E * (1/Xd1 - 1/Xd) * np.exp(-t/Td1) * np.sin(w*t+Alpha-Theta)
    return y

# Steady-state component of AC current (i_SS)
def SteadyStateCurrent(t, Alpha, Xd=Xd, E=E, Theta=Theta, w=w):
    y = E/Xd * np.sin(w*t+Alpha-Theta)
    return y

#  Alternative Circuit(i_AC(t))
def AlternativeCurrent(t,Alpha):
    y = SubtransientCurrent(t,Alpha) + TransientCurrent(t,Alpha) + SteadyStateCurrent(t,Alpha)
    return y

#  Total Short Circuit Current (i(t))
def TotalCurrent(t,Alpha):
    y = DirectCurrent(t,Alpha) + AlternativeCurrent(t,Alpha)
    return y

# explanation
container = st.container()
container.markdown(r'''
                   Because the short-circuit current is mainly influenced by the generator d-axis reactance, 
                   $\theta$ is selected as $\pi/2$ here. 
                   Same as for the case far away generator, 
                   $\alpha$ is primarily chosen to be $\alpha=(\theta-\pi/2)$ at the occurrence of the short circuit. 
                   The fault current in one phase of an unloaded synchronous machine 
                   during a three-phase short circuit is shown below.
                   ''')

# interactive input
st.markdown(r'''
            **Now it's your turn to decide when the short circuit takes place!**
            '''
            r'''
            👇Please select source angle $\alpha$ when short circuit occurs.
            ''')
alpha_in = st.slider("Voltage Source Angle(\N{DEGREE SIGN})", -90, 90, 0)

# Plot data
plt.style.use("ggplot")
fig1,ax1 = plt.subplots()

ax1.plot(t,AlternativeCurrent(t,alpha_in*np.pi/180)/1000, color="orange", label = "AC component $i_{AC}(t)$", zorder = 2, alpha = 0.7)
ax1.plot(t,DirectCurrent(t,alpha_in*np.pi/180)/1000, color="r", label = "DC component $i_{DC}(t)$", zorder = 3 )
ax1.plot(t,TotalCurrent(t,alpha_in*np.pi/180)/1000, color='blue', label = "Total short circuit current $i(t)$", zorder = 1)

ax1.set_xlim([0, np.max(t)])
ax1.set_ylim([np.min(AlternativeCurrent(t,alpha_in*np.pi/180))/1000-100, np.max(TotalCurrent(t,alpha_in*np.pi/180))/1000+100])
ax1.set_title("Three-phase short circuit current at generator outlet ")
ax1.legend(loc='upper right')
ax1.set_xlabel("Time in s")
ax1.set_ylabel("Short circuit current in kA")

container.pyplot(fig1)

# Show the Detailed Components of Current
container.markdown(r'''
               📝 **Explanations**
            '''
            r''' 
            Similar to the case of a short circuit far away from the generator, 
            the short circuit current also consists of a DC component and an AC component. 
            The difference is that the AC component no longer oscillates with equal amplitude, 
            but decays before converging to a steady state value. 
            '''
            r'''
            To figure out why the AC component oscillates in this way, 
            please refer to the following plot showing more detailed components.
               ''')

fig2,ax2 = plt.subplots()
ax2.plot(t, SubtransientCurrent(t,alpha_in*np.pi/180)/1000, color="m", label = "Subtransient", zorder = 3 )
ax2.plot(t, TransientCurrent(t,alpha_in*np.pi/180)/1000, color="y", label = "Transient", zorder = 1)
ax2.plot(t, SteadyStateCurrent(t,alpha_in*np.pi/180)/1000, color="c", label = "Steady-state", zorder = 2)
ax2.plot(t,DirectCurrent(t,alpha_in*np.pi/180)/1000, color="red", label = "DC component")

ax2.set_xlim([0, np.max(t)])
ax2.set_ylim([np.min(AlternativeCurrent(t,alpha_in*np.pi/180))/1000+200, np.max(TotalCurrent(t,alpha_in*np.pi/180))/1000-600])
ax2.set_title("Short circuit current components at generator outlet ")
ax2.legend(loc='upper right')
ax2.set_xlabel("Time in s")
ax2.set_ylabel("Short circuit current in kA")

container.pyplot(fig2)

# explanation
expander1 = container.expander("📝 Explanations")
expander1.markdown(r'''
                    The decaying AC component has three periods, from subtransient to transient eventually reaching steady state. 
                    The initial period of decay of the short-circuit current is called the subtrasient period 
                    in which the current decay is governed mainly by the d-axis short-circuit subtransient time constant $T_d^{"}$. 
                    At a later time, when *t* is larger than $T_d^{"}$, the first term has decayed almost to zero, 
                    the current continues to decay governed by a relatively large time constant, 
                    namely the d-axis short-circuit transient time constant $T_d^{'}$. 
                    This period of the short-circuit current is called the transient period. 
                    When *t* is much larger than $T_d^{'}$, the AC current approaches its steady-state value. 
                    The currents can be written as follows.
                    ''')
expander1.latex(r'''
                i(t)=i_{ac}(t)+i_{dc}(t)\\\
                i_{ac}(t)=\frac{\sqrt{2}V_{n}}{\sqrt{3}}[(\frac{1}{X_{d}^{"}}-\frac{1}{X_{d}^{'}})e^{-t/T_d^{"}}
                +(\frac{1}{X_{d}^{'}}-\frac{1}{X_{d}})e^{-t/T_d^{'}}+\frac{1}{X_{d}}]sin(\omega t+\alpha-\theta)\\\
                i_{dc}(t)=\frac{\sqrt{2}V_{n}}{\sqrt{3}X_{d}^{"}}sin(\alpha-\theta)e^{-t/T_A}
                ''')
expander1.markdown(r'''
                  where $X_{d}^{"} =$ direct axis subtransient reactance\
                  $X_{d}^{'} =$ direct axis transient reactance\
                  $X_d =$ direct axis synchronous reactance\
                  with the relationship: $X_{d}^{"} < X_{d}^{'} < X_d$
                ''')
expander2 = st.expander("💭 Why does the current change in this way?")
expander2.markdown(r'''
                    The appearance of DC offset current is due to the fact that 
                    the flux linkages of each stator phase cannot change instantaneously. 
                    The current is proportional to the flux linkages at the instant of short-circuit 
                    and then decays with armature time constant $T_A$.
                    '''
                   r'''
                    The magnetic flux induced by the short-circuit armature currents is 
                    initially forced to flow through high reluctance paths 
                    that are not linked to the field winding or damper circuits of the generator. 
                    The armature inductance, which is inversely proportional to reluctance, is therefore initially low. 
                    As the flux then moves toward the lower reluctance paths, the armature inductance increases.
                    ''')
st.markdown(r'''
            All we study now are symmetrical faults, 
            they may result in severe consequences but do not occur as often as asymmetrical faults, 
            for example single-phase to ground fault. 
            It is very complicated to study asymmetric faults directly, 
            therefore the symmetric component decomposition method is introduced.
            '''
            r'''
            💡You can use sidebar on the left side to select *Symmetrical components* page.
            ''')
