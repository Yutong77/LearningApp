import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Introduction"
)
st.header("Learning app for visualizing of fault currents")


st.write("Welcome to the Learning app for visualizing of fault currents. This app is part of the project energy supply with renewable energies  from the winter semester 2022/23.")
st.write("Faults should always be avoided in the grid. Unfortunately, despite precautions, faults occur again and again, which must therefore also be considered. The faults must be understood so that precautions can be taken on the system to protect the grid from collapsing.")
st.write("This App is used to simulate the common faults in a grid and to recognize the dependencies of individual parameters. In addition, the adjustable variables are explained.")



st.markdown("First, the 👉<a href='Three_Phase_far_away_Generator' target='_self'>short circuit far away the generator</a> is discussed. Thereby the transient process is shown.", unsafe_allow_html=True)
imageLocation = st.empty()
image = Image.open('pics/screen2.png')
imageLocation.image(image,width=500)
st.write("Subsequently, the 👉<a href='Three_Phase_Generator_Outlet' target='_self'>generator near short circuit</a> is considered. As with the short circuit far away the generator, the transient process of the current is shown here.", unsafe_allow_html=True)
imageLocation = st.empty()
image = Image.open('pics/screen3.png')
imageLocation.image(image,width=500)
st.write("Then, the 👉<a href='Symmetrical_Components' target='_self'>phase to ground or phase to phase short circuits</a> are considered. The effect on the individual phase currents is shown. It describes the steady state after the transient processes are completed.", unsafe_allow_html=True)
imageLocation = st.empty()
image = Image.open('pics/screen1.png')
imageLocation.image(image,width=500)
st.write("In   👉<a href='Symetrical_Components_Simulation_Model' target='_self'>the last part</a> you can try to find the worst scenario for the power line.", unsafe_allow_html=True)
imageLocation = st.empty()
image = Image.open('pics/screen1l.png')
imageLocation.image(image,width=500)
st.write("Through our app, we hope you understand the faults that may happen in the grid and by which parameters they can be regulated. Click 👉<a href='Three_Phase_far_away_Generator' target='_self'>here</a> to start with the short circuit far away the generator.", unsafe_allow_html=True)
