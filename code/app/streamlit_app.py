"""Argus Cantilever-lite dashboard."""
import streamlit as st
import json

st.title("Argus-Panoptes: Acoustics NDT")
mat = st.selectbox("Material", ["mild-steel", "al-6061", "soda-glass", "acrylic"])
ci = st.slider("Cloud index (demo)", 0, 100, 20)
refl = st.checkbox("Reflector detected")
risk = "HIGH" if ci > 65 or refl else ("WATCH" if ci > 35 else "OK")
st.metric("Risk", risk)
st.metric("Cloud index", ci)
st.write(f"Material: {mat}")
st.caption("Wire to fuse_report.report.json in next iteration.")
