import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("🚀 Demo Streamlit Application")

# Sidebar inputs
st.sidebar.header("User Input")
name = st.sidebar.text_input("Enter your name", "Shreyas")
age = st.sidebar.slider("Select your age", 18, 60, 25)

# Show user input
st.write(f"Hello **{name}**, you are **{age}** years old!")

# Create a simple DataFrame
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Sales": [120, 200, 150, 300, 250]
}
df = pd.DataFrame(data)

st.subheader("📊 Sales Data")
st.table(df)

# Plot
fig, ax = plt.subplots()
ax.plot(df["Month"], df["Sales"], marker="o")
ax.set_title("Monthly Sales Trend")
st.pyplot(fig)

# Button
if st.button("Say Hi"):
    st.success(f"Hi {name}, welcome to the Streamlit demo! 🎉")
#Test2
#Test3