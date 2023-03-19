import streamlit as st
from PIL import Image
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt

#calc code start
U=1.1*220/np.sqrt(3)

l=st.slider(label="power line length in km:", min_value=50, max_value=400, value=100, key='slider1')

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


st.title("Symmetrical components simulation model")
st.markdown("Use this model to test and combine different types of fault. Set the type of fault by clicking on the switches and then turning the power on.  \n" "👇 **Try to find the worst case scenario for the power line by changing the distance and the type of fault!**")

image000 = Image.open('pages/pics/pt_000.png')
image100 = Image.open('pages/pics/pt_100.png')
image010 = Image.open('pages/pics/pt_010.png')
image001 = Image.open('pages/pics/pt_001.png')
image011 = Image.open('pages/pics/pt_011.png')
image101 = Image.open('pages/pics/pt_101.png')
image110 = Image.open('pages/pics/pt_110.png')
image111 = Image.open('pages/pics/pt_111.png')  



    
imageLocation4 = st.empty()
image4 = Image.open('pages/pics/pt_000.png')
imageLocation4.image(image4,width=800)


sw100=st.checkbox('', key='100')  
sw010=st.checkbox('', key='010')
sw001=st.checkbox('', key='001')


if not sw001 and not sw100 and not sw010:    #000
    imageLocation4.image(image000,width=800)   

if sw100 and not sw010 and not sw001:       #100
    imageLocation4.image(image100,width=800)
    
if sw010 and not sw100 and not sw001:       #010
    imageLocation4.image(image010,width=800)

if sw001 and not sw010 and not sw100:       #001
    imageLocation4.image(image001,width=800)   
    
if sw100 and sw010 and not sw001:          #110
    imageLocation4.image(image110,width=800)    
    
if sw010 and not sw100 and sw001:           #011
    imageLocation4.image(image011,width=800)    
    
if sw001 and sw100 and not sw010:           #101
    imageLocation4.image(image101,width=800)    
    
if sw001 and sw100 and sw010:              #111
    imageLocation4.image(image111,width=800)  

powerb4= st.radio(
    "👇 POWER:",
    ('OFF', 'ON'),key='Pb4' ,horizontal=True, label_visibility="visible")
    
    
if powerb4 == 'OFF':
    I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(0,0,0)
    
if powerb4 == 'ON':
    
    if not sw001 and not sw100 and not sw010:    #000
        i1=U/(500)
        i2=0
        i0=0
        I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(i1,i2,i0)   

    if sw100 and not sw010 and not sw001:       #100
        i1=U/(2*Z1+Z0)
        i2=i1*a_1
        i0=i1*a_2
        I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(i1,i2,i0) 
    if sw010 and not sw100 and not sw001:       #010
        i1=U/(2*Z1)
        i2=-U/(2*Z1)
        i0=0
        I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(i1,i2,i0) 
    if sw001 and not sw010 and not sw100:       #001
        i1=1*U/(2*Z1)
        i2=a_1*-U/(2*Z1)
        i0=0
        I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(i1,i2,i0) 
    if sw100 and sw010 and not sw001:          #110
        i1=U/(Z1+((Z1*Z0)/(Z1+Z0)))
        i2=-(U-i1*Z1)/Z1
        i0=-(U-i1*Z1)/Z0
        I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(i1,i2,i0) 

    if sw010 and not sw100 and sw001:           #011
        i1=U/(Z1)
        i2=0
        i0=0
        I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(i1,i2,i0) 

    if sw001 and sw100 and not sw010:           #101
        i1=1*U/(2*Z1)
        i2=a_1*-U/(2*Z1)
        i0=0
        p_rst4, I_z14, p_z24, I_z04, limfg4,wfg4 =calc_systems(i1,i2,i0) 
        
        t1=U/(2*Z1+Z0)
        t2=i1*a_1
        t0=i1*a_2
        t_rst4, t_z14, I_z24, t_z04, lim4,w4 =calc_systems(t1,t2,t0) 
        
        I_rst4=[p_rst4[0],t_rst4[1],p_rst4[2]]
        

    if sw001 and sw100 and sw010:              #111
        i1=U/(Z1)
        i2=0
        i0=0
        I_rst4, I_z14, I_z24, I_z04, lim4,w4 =calc_systems(i1,i2,i0) 
    
    
fig41,ax41 = plt.subplots(1, figsize=(8, 7))
ax41.arrow(0,0,I_rst4[0].real,I_rst4[0].imag,color='#DF0AFF',head_width=3*w4,width=w4, label = "$I_\mathrm{L1}$")
ax41.arrow(0,0,I_rst4[2].real,I_rst4[2].imag,color='#0000FF',head_width=3*w4,width=w4, label = "$I_\mathrm{L2}$")
ax41.arrow(0,0,I_rst4[1].real,I_rst4[1].imag,color='#00BFFF',head_width=3*w4,width=w4, label = "$I_\mathrm{L3}$")
ax41.set_xlim([-lim4, lim4])
ax41.set_ylim([-lim4, lim4])
ax41.set_title("Original system")
ax41.legend(loc='lower right')
ax41.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax41.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax41.grid()
st.pyplot(fig41)    


fig42,ax42 = plt.subplots(1, figsize=(6, 5))
ax42.arrow(0,0,I_z14[0].real,I_z14[0].imag,color='#DF0AFF',head_width=3*w4,width=w4)
ax42.arrow(0,0,I_z24[0].real,I_z24[0].imag,color='#00BFFF',head_width=3*w4,width=w4)
ax42.arrow(0,0,I_z04[0].real,I_z04[0].imag,color='#0000FF',head_width=3*w4,width=w4)
ax42.set_xlim([-lim4, lim4])
ax42.set_ylim([-lim4, lim4])
ax42.set_title("Positive sequence")
ax42.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax42.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax42.grid()
st.pyplot(fig42) 


fig43,ax43 = plt.subplots(1, figsize=(6, 5))
ax43.arrow(0,0,I_z14[1].real,I_z14[1].imag,color='#DF0AFF',head_width=3*w4,width=w4)
ax43.arrow(0,0,I_z24[1].real,I_z24[1].imag,color='#00BFFF',head_width=3*w4,width=w4)
ax43.arrow(0,0,I_z04[1].real,I_z04[1].imag,color='#0000FF',head_width=3*w4,width=w4)
ax43.set_xlim([-lim4, lim4])
ax43.set_ylim([-lim4, lim4])
ax43.set_title("Negative sequence")
ax43.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax43.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax43.grid()
st.pyplot(fig43) 


fig44,ax44 = plt.subplots(1, figsize=(6, 5))
ax44.arrow(0,lim4/4,I_z14[2].real,I_z14[2].imag,color='#DF0AFF',head_width=3*w4,width=w4)
ax44.arrow(0,0,I_z24[2].real,I_z24[2].imag,color='#00BFFF',head_width=3*w4,width=w4)
ax44.arrow(0,-lim4/4,I_z04[2].real,I_z04[2].imag,color='#0000FF',head_width=3*w4,width=w4)
ax44.set_xlim([-lim4, lim4])
ax44.set_ylim([-lim4, lim4])
ax44.set_title("Zero sequence")
ax44.set_xlabel("$\Re(\mathrm{I})$ in kA")
ax44.set_ylabel("$\Im(\mathrm{I})$ in kA")
#ax44.grid()
st.pyplot(fig44)       

if sw010 and sw001 and powerb4 == 'ON' and l == 50:
    st.markdown("**Correct!**  \n"  "📝 The worst case for the power line means the highest fault current. Since the voltage is constant, the highest current results when the impedance is at the lowest, which happens when the length of the power line is the shortest and when there is a 3-phase fault. Because in this case, the ground impedance, which is higher than the power line impedance, isn't part of the fault circuit. The connection between the resulting neutral point and ground is not relevant since they both have the same potential")

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
    top: 110px;
    background-color:  /*rgb(255, 255, 102); yellow*/ 
    border-radius: 4px;
    z-index:2;
    }
    
    div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*imag1*/ 
    position: absolute;
    left: 0px;
    top: 100px;
    z-index:1;
    }
    
    div.element-container:nth-child(5) > div:nth-child(1) > label:nth-child(1) > span:nth-child(1){                /*Switch 100*/ 
    position: absolute;
    left: 640px;
    top: 528px;
    height: 40px;  
    width: 26px;
    background-color:  Transparent;
    border-style: none;
    z-index:2;
    background-image: none;
    transition-duration: 1ms;
    }
    
    div.element-container:nth-child(6) > div:nth-child(1) > label:nth-child(1) > span:nth-child(1){                /*Switch 010*/ 
    position: absolute;
    left: 695px;
    top: 428px;
    height: 40px;  
    width: 26px;
    background-color:  Transparent;
    border-style: none;
    z-index:2;
    background-image: none;
    transition-duration: 1ms;
    }
    
    div.element-container:nth-child(7) > div:nth-child(1) > label:nth-child(1) > span:nth-child(1){                /*Switch 001*/ 
    position: absolute;
    left: 735px;
    top: 362px;
    height: 40px;  
    width: 26px;
    background-color:  Transparent;
    border-style: none;
    z-index:2;
    background-image: none;
    transition-duration: 1ms;
    }
    
    .stRadio{          /*pwb*/ 
    position: absolute;
    left: 0px;
    top: 600px;
    z-index:2;
    }
    
    .stSlider{          /*slider*/ 
    position: absolute;
    left: 0px;
    top: 820px;
    z-index:1;
    }
    
    div.element-container:nth-child(9) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*os1*/ 
    position: absolute;
    left: 00px;
    top: 800px;
    flex: 0 0 auto;
    max-width: 720px;
    min-width: 720px;
    height: 600px;
    z-index:1;
    }

    
    div.element-container:nth-child(10) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ps1*/ 
    position: absolute;
    left: -100px;
    top: 1385px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(11) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*ns1*/ 
    position: absolute;
    left: 220px;
    top: 1370px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(12) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > img:nth-child(1){          /*zs1*/ 
    position: absolute;
    left: 540px;
    top: 1355px;
    flex: 0 0 auto;
    max-width: 300px;
    height:280px;
    z-index:1;
    }
    
    div.element-container:nth-child(13) > div:nth-child(1) > div:nth-child(1) > p:nth-child(1){          /*mark2*/ 
    position: absolute;
    left: 0px;
    top: 1650px;
    background-color:  
    border-radius: 4px;
    z-index:2;
    }
   
</style>""", unsafe_allow_html=True)