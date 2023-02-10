import streamlit as st
from PIL import Image
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt

#calc code start
U=1.1*220/np.sqrt(3)

l=st.slider(label="power line lenght in km:", min_value=50, max_value=400, value=100, key='slider1')

X1=0.34*l
X0=0.95*l
R1=0
R0=0

Z1=X1*1j+R1
Z2=Z1
Z0=X0*1j+R0

a_1=-0.5+(np.sqrt(3)/2)*1j
a_2=-0.5-(np.sqrt(3)/2)*1j

T_s = np.array([[1,1,1],[a_2,a_1,1],[a_1,a_2,1]])

T_si=(1/3)*np.array([[1,a_1,a_2],[1,a_2,a_1],[1,1,1]])


I1=0
I2=0
I0=0





def calc_systems(I1,I2,I0):
    I_120=np.array([I1,I2,I0])
    I_rst=np.matmul(T_s,I_120)

    I_z1=T_s[0]*I_120
    I_z2=T_s[1]*I_120
    I_z0=T_s[2]*I_120
    
    lim=1.1*max(cm.polar(I_rst[0])[0],cm.polar(I_rst[1])[0],cm.polar(I_rst[2])[0])+0.00001
    
    w=lim/200

    
    
    return I_rst, I_z1, I_z2, I_z0, lim ,w

#calc code end




#site code start


st.title("Symmetrical components")
st.markdown("To determine the current in case of a fault, the method of symmetrical components is used.")
st.markdown("This method disassembles the original sequence into 3 sequences, that add up as the original sequence again.")

pic = Image.open('pages/pics/evee_systems.png')

picLocation = st.empty()
picLocation.image(pic,width=700)

st.markdown("**Turn the Power on to see how the current and the sequences look in a working power system without a fault!**")

imageLocation1 = st.empty()
image = Image.open('pages/pics/pt_000.png')

imageLocation1.image(image,width=700)
powerb= st.radio(
    "👇 POWER:",
    ('OFF', 'ON'), horizontal=True, label_visibility="visible",key='Pb1')


if powerb == 'OFF':
    I_rst1, I_z11, I_z21, I_z01, lim1,w1 = calc_systems(0,0,0)


if powerb == 'ON':
    i1=U/(500)
    i2=0
    i0=0
    I_rst1, I_z11, I_z21, I_z01, lim1, w1 =calc_systems(i1,i2,i0)

fig1,ax1 = plt.subplots(1, figsize=(8, 7))

ax1.arrow(0,0,I_rst1[0].real,I_rst1[0].imag,color='#DF0AFF',head_width=3*w1,width=w1, label = "$I_\mathrm{L1}$")
ax1.arrow(0,0,I_rst1[2].real,I_rst1[2].imag,color='#0000FF',head_width=3*w1,width=w1, label = "$I_\mathrm{L2}$")
ax1.arrow(0,0,I_rst1[1].real,I_rst1[1].imag,color='#00BFFF',head_width=3*w1,width=w1, label = "$I_\mathrm{L3}$")

ax1.set_xlim([-lim1, lim1])
ax1.set_ylim([-lim1, lim1])
ax1.set_title("Original system")
ax1.legend(loc='lower right')
ax1.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax1.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax1.grid()
st.pyplot(fig1)    


fig2,ax2 = plt.subplots(1, figsize=(6, 5))
ax2.arrow(0,0,I_z11[0].real,I_z11[0].imag,color='#DF0AFF',head_width=3*w1,width=w1)
ax2.arrow(0,0,I_z21[0].real,I_z21[0].imag,color='#00BFFF',head_width=3*w1,width=w1)
ax2.arrow(0,0,I_z01[0].real,I_z01[0].imag,color='#0000FF',head_width=3*w1,width=w1)
ax2.set_xlim([-lim1, lim1])
ax2.set_ylim([-lim1, lim1])
ax2.set_title("Positive sequence")
ax2.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax2.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax2.grid()
st.pyplot(fig2) 


fig3,ax3 = plt.subplots(1, figsize=(6, 5))
ax3.arrow(0,0,I_z11[1].real,I_z11[1].imag,color='#DF0AFF',head_width=3*w1,width=w1)
ax3.arrow(0,0,I_z21[1].real,I_z21[1].imag,color='#00BFFF',head_width=3*w1,width=w1)
ax3.arrow(0,0,I_z01[1].real,I_z01[1].imag,color='#0000FF',head_width=3*w1,width=w1)
ax3.set_xlim([-lim1, lim1])
ax3.set_ylim([-lim1, lim1])
ax3.set_title("Negative sequence")
ax3.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax3.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax3.grid()
st.pyplot(fig3) 


fig4,ax4 = plt.subplots(1, figsize=(6, 5))
ax4.arrow(0,lim1/4,I_z11[2].real,I_z11[2].imag,color='#DF0AFF',head_width=3*w1,width=w1)
ax4.arrow(0,0,I_z21[2].real,I_z21[2].imag,color='#00BFFF',head_width=3*w1,width=w1)
ax4.arrow(0,-lim1/4,I_z01[2].real,I_z01[2].imag,color='#0000FF',head_width=3*w1,width=w1)
ax4.set_xlim([-lim1, lim1])
ax4.set_ylim([-lim1, lim1])
ax4.set_title("Zero sequence")
ax4.set_xlabel("$\Re(\mathrm{I})$ in kA ")
ax4.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax4.grid()
st.pyplot(fig4) 



st.markdown("In case of a fault, a phase of the powerline will get connected to another phase or the ground. The fault will lead to a fault-current in the phase but also influence the current of the other phases")
st.markdown("💭 What will happen to the current in phase L2, if a tree falls into the power line and connects L3 with the ground?")

choice1 = st.radio(
    "choice1",
    ('The current in L2 will get higher', 'The current in L2 will be 0', 'The current in L2 will not change'), horizontal=False, label_visibility="hidden",key='ch1')

if choice1 == 'The current in L2 will get higher' or choice1 == 'The current in L2 will be 0' or choice1 == 'The current in L2 will not change':
    st.markdown("👇 **Go try it! Connect L3 to the ground by clicking the switch!**")

    
imageLocation2 = st.empty()
image2 = Image.open('pages/pics/pt_000.png')
imageLocation2.image(image2,width=700)

sw10=st.checkbox('', key='10')  


image000 = Image.open('pages/pics/pt_000.png')
image100 = Image.open('pages/pics/pt_100.png')
image010 = Image.open('pages/pics/pt_010.png')
image001 = Image.open('pages/pics/pt_001.png')
image011 = Image.open('pages/pics/pt_011.png')
image101 = Image.open('pages/pics/pt_101.png')
image110 = Image.open('pages/pics/pt_110.png')
image111 = Image.open('pages/pics/pt_111.png')   
    
if not sw10:
    imageLocation2.image(image000,width=700)
if sw10:
    imageLocation2.image(image100,width=700)



if not sw10:
    i1=U/(500)
    i2=0
    i0=0
    I_rst2, I_z12, I_z22, I_z02, lim2,w2 =calc_systems(i1,i2,i0)  


if sw10:
    i1=U/(2*Z1+Z0)
    i2=i1*a_1
    i0=i1*a_2
    I_rst2, I_z12, I_z22, I_z02, lim2,w2 =calc_systems(i1,i2,i0) 

    
fig21,ax21 = plt.subplots(1, figsize=(8, 7))
ax21.arrow(0,0,I_rst2[0].real,I_rst2[0].imag,color='#DF0AFF',head_width=3*w2,width=w2, label = "$I_\mathrm{L1}$")
ax21.arrow(0,0,I_rst2[2].real,I_rst2[2].imag,color='#0000FF',head_width=3*w2,width=w2, label = "$I_\mathrm{L2}$")
ax21.arrow(0,0,I_rst2[1].real,I_rst2[1].imag,color='#00BFFF',head_width=3*w2,width=w2, label = "$I_\mathrm{L3}$")
ax21.set_xlim([-lim2, lim2])
ax21.set_ylim([-lim2, lim2])
ax21.set_title("Original system")
ax21.legend(loc='lower right')
ax21.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax21.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax21.grid()
st.pyplot(fig21)    


fig22,ax22 = plt.subplots(1, figsize=(6, 5))
ax22.arrow(0,0,I_z12[0].real,I_z12[0].imag,color='#DF0AFF',head_width=3*w2,width=w2)
ax22.arrow(0,0,I_z22[0].real,I_z22[0].imag,color='#00BFFF',head_width=3*w2,width=w2)
ax22.arrow(0,0,I_z02[0].real,I_z02[0].imag,color='#0000FF',head_width=3*w2,width=w2)
ax22.set_xlim([-lim2, lim2])
ax22.set_ylim([-lim2, lim2])
ax22.set_title("Positive sequence")
ax22.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax22.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax22.grid()
st.pyplot(fig22) 


fig23,ax23 = plt.subplots(1, figsize=(6, 5))
ax23.arrow(0,0,I_z12[1].real,I_z12[1].imag,color='#DF0AFF',head_width=3*w2,width=w2)
ax23.arrow(0,0,I_z22[1].real,I_z22[1].imag,color='#00BFFF',head_width=3*w2,width=w2)
ax23.arrow(0,0,I_z02[1].real,I_z02[1].imag,color='#0000FF',head_width=3*w2,width=w2)
ax23.set_xlim([-lim2, lim2])
ax23.set_ylim([-lim2, lim2])
ax23.set_title("Negative sequence")
ax23.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax23.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax23.grid()
st.pyplot(fig23) 


fig24,ax24 = plt.subplots(1, figsize=(6, 5))
ax24.arrow(0,lim2/4,I_z12[2].real,I_z12[2].imag,color='#DF0AFF',head_width=3*w2,width=w2)
ax24.arrow(0,0,I_z22[2].real,I_z22[2].imag,color='#00BFFF',head_width=3*w2,width=w2)
ax24.arrow(0,-lim2/4,I_z02[2].real,I_z02[2].imag,color='#0000FF',head_width=3*w2,width=w2)
ax24.set_xlim([-lim2, lim2])
ax24.set_ylim([-lim2, lim2])
ax24.set_title("Zero sequence")
ax24.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax24.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax24.grid()
st.pyplot(fig24)     
  
if not sw10:
    st.markdown("☝️ **Click on the switch to simulate the fault and check your choice!**")
                                
    
if sw10 and choice1 == 'The current in L2 will be 0':
                
    st.markdown(r'''
                **:green[Your answer was correct!]**\
                📝 The fault between phase L3 and ground leads to an extremely high fault-current,
                contains the whole power of the system. Therefore the currents in phase L1 and L2 are 0.
                ''')
    
if sw10 and (choice1 == 'The current in L2 will get higher' or choice1 == 'The current in L2 will not change'):   
    st.markdown(r'''
                **:red[Your answer was not correct!]**\
                📝 The fault between phase L3 and ground leads to an extremely high fault-current, 
                that contains the whole power of the system. Therefore the currents in phase L1 and L2 are 0.
                ''')   
    

    
st.markdown("💭 Besides faults between one or multiple phases and ground, there are also phase-phase faults.  \n"  "How will the current in phase L1 change if there is a short circuit between the phases L1 and L2?")

c3 = st.radio(
    "c3",
    ('The current in L1 will be 0', 'The current in L1 will be the same as the current in L2', 'The current in L1 will be the negative of the current in L2'), horizontal=False, label_visibility="hidden",key='ch3')

if c3 == 'The current in L1 will be 0' or c3 == 'The current in L1 will be the same as the current in L2' or c3 == 'The current in L1 will be the negative of the current in L2':
    st.markdown("👇 **Go try it! Connect L1 to L2 by clicking the switch!**")    
    
    
    
imageLocation3 = st.empty()
image3 = Image.open('pages/pics/pt_000.png')
imageLocation3.image(image3,width=700)

sw01=st.checkbox('', key='01')  
    
if not sw01:
    imageLocation3.image(image000,width=700)
if sw01:
    imageLocation3.image(image001,width=700)
    

    
    
if not sw01:
    i1=U/(500)
    i2=0
    i0=0
    I_rst3, I_z13, I_z23, I_z03, lim3,w3 =calc_systems(i1,i2,i0) 
    
if sw01:
    i1=1*U/(2*Z1)
    i2=a_1*-U/(2*Z1)
    i0=0
    I_rst3, I_z13, I_z23, I_z03, lim3,w3 =calc_systems(i1,i2,i0) 

    
fig31,ax31 = plt.subplots(1, figsize=(8, 7))
ax31.arrow(0,0,I_rst3[0].real,I_rst3[0].imag,color='#DF0AFF',head_width=3*w3,width=w3, label = "$I_\mathrm{L1}$")
ax31.arrow(0,0,I_rst3[2].real,I_rst3[2].imag,color='#0000FF',head_width=3*w3,width=w3, label = "$I_\mathrm{L2}$")
ax31.arrow(0,0,I_rst3[1].real,I_rst3[1].imag,color='#00BFFF',head_width=3*w3,width=w3, label = "$I_\mathrm{L3}$")
ax31.set_xlim([-lim3, lim3])
ax31.set_ylim([-lim3, lim3])
ax31.set_title("Original system")
ax31.legend(loc='lower right')
ax31.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax31.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax31.grid()
st.pyplot(fig31)    


fig32,ax32 = plt.subplots(1, figsize=(6, 5))
ax32.arrow(0,0,I_z13[0].real,I_z13[0].imag,color='#DF0AFF',head_width=3*w3,width=w3)
ax32.arrow(0,0,I_z23[0].real,I_z23[0].imag,color='#00BFFF',head_width=3*w3,width=w3)
ax32.arrow(0,0,I_z03[0].real,I_z03[0].imag,color='#0000FF',head_width=3*w3,width=w3)
ax32.set_xlim([-lim3, lim3])
ax32.set_ylim([-lim3, lim3])
ax32.set_title("Positive sequence")
ax32.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax32.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax32.grid()
st.pyplot(fig32) 


fig33,ax33 = plt.subplots(1, figsize=(6, 5))
ax33.arrow(0,0,I_z13[1].real,I_z13[1].imag,color='#DF0AFF',head_width=3*w3,width=w3)
ax33.arrow(0,0,I_z23[1].real,I_z23[1].imag,color='#00BFFF',head_width=3*w3,width=w3)
ax33.arrow(0,0,I_z03[1].real,I_z03[1].imag,color='#0000FF',head_width=3*w3,width=w3)
ax33.set_xlim([-lim3, lim3])
ax33.set_ylim([-lim3, lim3])
ax33.set_title("Negative sequence")
ax33.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax33.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax33.grid()
st.pyplot(fig33) 


fig34,ax34 = plt.subplots(1, figsize=(6, 5))
ax34.arrow(0,lim3/4,I_z13[2].real,I_z13[2].imag,color='#DF0AFF',head_width=3*w3,width=w3)
ax34.arrow(0,0,I_z23[2].real,I_z23[2].imag,color='#00BFFF',head_width=3*w3,width=w3)
ax34.arrow(0,-lim3/4,I_z03[2].real,I_z03[2].imag,color='#0000FF',head_width=3*w3,width=w3)
ax34.set_xlim([-lim3, lim3])
ax34.set_ylim([-lim3, lim3])
ax34.set_title("Zero sequence")
ax34.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax34.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax34.grid()
st.pyplot(fig34)       

if not sw01:
    st.markdown("☝️ **Click on the switch to simulate the fault and check your choice!**")
    
if sw01 and c3 == 'The current in L1 will be the negative of the current in L2':   
    st.markdown(r'''
                **:green[Your answer was correct!]**\
                📝 The fault between the phases L1 and L2 leads to an extremely high fault-current between the phases. 
                Based on Kirchhoff's junction rule, 
                the current that goes through phase L1 has to go back into phase L2 in the opposite direction, 
                therefore the angle between both currents is 180°.
                ''')    
    
if sw01 and c3 == 'The current in L1 will be 0' or c3 == 'The current in L1 will be the same as the current in L2':   
    st.markdown(r'''
                **:red[Your answer was not correct.]**\
                📝 The fault between the phases L1 and L2 leads to an extremely high fault-current between the phases. 
                Based on Kirchhoff's junction rule, 
                the current that goes through phase L1 has to go back into phase L2 in the opposite direction, 
                therefore the angle between both currents is 180°.
                ''')        
    
    
    
    
    
    
    
st.markdown("But the type of fault is not the only parameter that influence the fault current. Another important parameter is the place of the fault.")       
st.markdown("👇 **Change the lenght of the power line to control the place of the fault and watch how the fault current changes!**  \n"   "💭 What influence has the lenght of the power line on the fault current?")      
c2= st.radio(
    "lenght",
    ('The increase of the lenght has no influence on the fault current','The increase of the lenght leads to a higher fault current', 'The increase of the lenght leads to a lower fault current'),key='ch2' ,horizontal=False, label_visibility="hidden")    


if c2=='The increase of the lenght leads to a lower fault current':
    st.markdown(r'''
                ** :green[Thats correct!]**\
                📝 A power line can be electrical represented by an inductor that has an inductance per unit length. 
                The resulting fault current is the quotient of the voltage and the absolute value of the power line impedance. 
                With a lower lenght of the power line, the impedance gets smaller and the fault current increases.
                ''') 
    
    esb = Image.open('pages/pics/pl_esb.png')
    esbLocation = st.empty()
    esbLocation.image(esb,width=700)
    
    st.latex(r'''X = j \omega L'\cdot l \; \; \; \; \;\; \; \; \; \; \; I_\mathrm{Fault}=\frac{U}{|X|}''')
    

if c2=='The increase of the lenght leads to a higher fault current' or c2=='The increase of the lenght has no influence on the fault current':
    st.markdown(r'''
                ** :red[Thats not correct.]** \
                📝 A power line can be electrical represented by an inductor that has an inductance per unit length. 
                The resulting fault current is the quotient of the voltage and the absolute value of the power line impedance. 
                With a lower lenght of the power line, the impedance gets smaller and the fault current increases.
                ''') 
    esb = Image.open('pages/pics/pl_esb.png')
    esbLocation = st.empty()
    esbLocation.image(esb,width=700)
    
    st.latex(r'''X = j \omega L'\cdot l \; \; \; \; \;\; \; \; \; \; \; I_\mathrm{Fault}=\frac{U}{|X|}''')


st.markdown("As you have seen so far the height of the fault current is depending on the type of fault and on the place of the fault.  \n"  "Use the full 👉<a href='Symmetrical_components_simulation_model' target='_self'>simulation model</a>  on the next page to test different faults and to find the worst case scenario for the power line!  \n"  "    \n"  "  ")  


#st.stop()
m = st.markdown("""
<style>
    .css-10trblm{          /*title*/ 
    position: absolute;
    left: 0px;
    top: 0px;
    z-index:1;
    }
    
    div.element-container:nth-child(3) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark1*/ 
    position: absolute;
    left: 0px;
    top: 50px;
    z-index:1;
    }
    
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark2*/ 
    position: absolute;
    left: 0px;
    top: 60px;
    z-index:1;
    }
    
    div.element-container:nth-child(5) > div:nth-child(1) > div:nth-child(2){          /*pic*/ 
    position: absolute;
    left: 0px;
    top: 130px;
    z-index:1;
    }
    
    
    div.element-container:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark3*/ 
    position: absolute;
    left: 0px;
    top: 460px;
    background-color: 
    border-radius: 4px;
    z-index:2;
    }
    
    div.element-container:nth-child(7) > div:nth-child(1) > div:nth-child(2){          /*imag1*/ 
    position: absolute;
    left: 0px;
    top: 430px;
    z-index:1;
    }
    
    div.element-container:nth-child(8) > div:nth-child(1){          /*powerbutton*/ 
    position: absolute;
    left: 0px;
    top: 910px;
    z-index:1;
    }

    div.element-container:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*os1*/ 
    position: absolute;
    left: 00px;
    top: 1040px;
    flex: 0 0 auto;
    max-width: 720px;
    min-width: 720px;
    height: 600px;
    z-index:1;
    }

    
    div.element-container:nth-child(10) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ps1*/ 
    position: absolute;
    left: -100px;
    top: 1625px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ns1*/ 
    position: absolute;
    left: 220px;
    top: 1610px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(12) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*zs1*/ 
    position: absolute;
    left: 540px;
    top: 1595px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    
    div.element-container:nth-child(13) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark4*/ 
    position: absolute;
    left: 0px;
    top: 1950px;
    background-color:  
    border-radius: 4px;
    z-index:1;
    }
    
    
    div.element-container:nth-child(14) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark5*/ 
    position: absolute;
    left: 0px;
    top: 2000px;
    background-color:
    border-radius: 4px;
    z-index:1;
    }
    
    div.element-container:nth-child(15) > div:nth-child(1) > div:nth-child(2){          /*ratio1*/ 
    position: absolute;
    left: 0px;
    top: 2050px;
    z-index:2;
    }
    
    div.element-container:nth-child(16) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark6*/ 
    position: absolute;
    left: 0px;
    top: 2090px;
    background-color:  
    border-radius: 4px;
    z-index:2;
    }
    
    div.element-container:nth-child(17) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1){          /*imag2*/ 
    position: absolute;
    left: 0px;
    top: 2000px;
    z-index:1;
    }
    
    div.element-container:nth-child(18) > div:nth-child(1) > label:nth-child(1) > span:nth-child(1){                /*Switch 100*/ 
    position: absolute;
    left: 560px;
    top: 2380px;
    height: 30px;  
    width: 20px;
    background-color:  Transparent;
    border-style: none;
    z-index:2;
    background-image: none;
    transition-duration: 1ms;
    }
    
    
    
    div.element-container:nth-child(19) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*os2*/ 
    position: absolute;
    left: 00px;
    top: 2550px;
    flex: 0 0 auto;
    max-width: 720px;
    min-width: 720px;
    height: 600px;
    z-index:1;
    }

    
    div.element-container:nth-child(20) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ps2*/ 
    position: absolute;
    left: -100px;
    top: 3135px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(21) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ns2*/ 
    position: absolute;
    left: 220px;
    top: 3110px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(22) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*zs2*/ 
    position: absolute;
    left: 540px;
    top: 3095px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(23) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*answ1*/ 
    position: absolute;
    left: 0px;
    top: 3400px;
    background-color:  
    border-radius: 4px;
    z-index:1;
    }
    
    div.element-container:nth-child(24) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark7*/ 
    position: absolute;
    left: 0px;
    top: 3600px;
    background-color: 
    border-radius: 4px;
    z-index:1;
    }
    
    div.element-container:nth-child(25) > div:nth-child(1) > div:nth-child(2){          /*ratio3*/ 
    position: absolute;
    left: 0px;
    top: 3650px;
    z-index:2;
    }
  
    
    div.element-container:nth-child(26) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark9*/ 
    position: absolute;
    left: 0px;
    top: 3740px;
    border-radius: 4px;
    z-index:2;
    }
    
    
    div.element-container:nth-child(27) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1){          /*imag3*/ 
    position: absolute;
    left: 0px;
    top: 3650px;
    z-index:1;
    }
   
    div.element-container:nth-child(28) > div:nth-child(1) > label:nth-child(1) > span:nth-child(1){                /*Switch 001*/ 
    position: absolute;
    left: 642px;
    top: 3907px;
    height: 30px;  
    width: 20px;
    background-color:   Transparent;
    border-style: none;
    z-index:2;
    background-image: none;
    transition-duration: 1ms;
    }
    
    div.element-container:nth-child(29) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*os3*/ 
    position: absolute;
    left: 00px;
    top: 4200px;
    flex: 0 0 auto;
    max-width: 720px;
    min-width: 720px;
    height: 600px;
    z-index:1;
    }

    
    div.element-container:nth-child(30) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ps3*/ 
    position: absolute;
    left: -100px;
    top: 4785px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(31) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ns3*/ 
    position: absolute;
    left: 220px;
    top: 4770px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(32) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*zs3*/ 
    position: absolute;
    left: 540px;
    top: 4755px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(33) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){                  /*answ2*/
    position: absolute;
    left: 0px;
    top: 5060px;
    border-radius: 4px;
    background-color: 
    z-index:2;
    }
    
    div.element-container:nth-child(34) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){                  /*mark10*/
    position: absolute;
    left: 0px;
    top: 5250px;
    border-radius: 4px;
    z-index:1;
    }
    
    div.element-container:nth-child(35) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){                  /*mark11*/
    position: absolute;
    left: 0px;
    top: 5300px;
    border-radius: 4px;
    background-color: 
    z-index:1;
    }
    
    div.element-container:nth-child(36) > div:nth-child(1) > div:nth-child(2){          /*ratio3*/ 
    position: absolute;
    left: 0px;
    top: 5370px;
    z-index:1;
    }
    
    .stSlider{          /*slider*/ 
    position: absolute;
    left: 0px;
    top: 6120px;
    z-index:1;
    }
   
    div.element-container:nth-child(37) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*answ3*/ 
    position: absolute;
    left: 0px;
    top: 5650px;
    border-radius: 4px;
    background-color: 
    z-index:1;
    }
    
    div.element-container:nth-child(38) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*esb*/ 
    position: absolute;
    left: 0px;
    top: 5760px;
    z-index:1;
    }
    
    .katex-html{                                                                                        /*latex*/
    position: absolute;
    left: 0px;
    top: 5990px;
    background-color:  
    border-radius: 4px;
    z-index:1;
    }
    
    
    div.element-container:nth-child(40) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){                     /*mark12*/
    position: absolute;
    left: 0px;
    top: 6050px;
    height: 200px;
    z-index:1;
    }
    
   
   
   
</style>""", unsafe_allow_html=True)




    
