"""
Demo: Understanding st.session_state in Streamlit

This file demonstrates how session state works and why it's important.
Run this with: streamlit run session_state_demo.py
"""

import streamlit as st

st.title("🔐 Session State Demo")

st.markdown("""
**The Problem:** Streamlit reruns your entire script from top to bottom every time you interact with it.
Without session state, all variables are reset!
""")

# ----- Demo 1: Without Session State -----
st.header("❌ Without Session State (Data Lost)")

# This counter resets to 0 every time!
counter_no_state = 0

col1, col2 = st.columns(2)
with col1:
    if st.button("Increment (No State)", key="btn1"):
        counter_no_state += 1  # This change is lost immediately!

with col2:
    st.metric("Counter Value", counter_no_state)
    st.caption("This always shows 0 because the variable resets on every rerun")

st.divider()

# ----- Demo 2: With Session State -----
st.header("✅ With Session State (Data Persists)")

# Initialize session state (only runs if key doesn't exist)
if "counter_with_state" not in st.session_state:
    st.session_state.counter_with_state = 0
    st.info("Created 'counter_with_state' in session vault!")

col1, col2 = st.columns(2)
with col1:
    if st.button("Increment (With State)", key="btn2"):
        st.session_state.counter_with_state += 1  # This persists!

with col2:
    st.metric("Counter Value", st.session_state.counter_with_state)
    st.caption("This persists across reruns!")

st.divider()

# ----- Demo 3: Storing Complex Objects -----
st.header("🗃️ Storing Complex Objects")

# Initialize a dictionary in session state
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "name": "",
        "pets": [],
        "preferences": {}
    }

name_input = st.text_input("Your Name", value=st.session_state.user_data["name"])

if st.button("Save Name"):
    st.session_state.user_data["name"] = name_input
    st.success(f"Saved '{name_input}' to session state!")

if st.session_state.user_data["name"]:
    st.info(f"👋 Hello, {st.session_state.user_data['name']}! Your name is saved in session state.")

st.divider()

# ----- Demo 4: Checking Before Creating -----
st.header("🔍 Pattern: Check Before Creating")

st.code("""
# Good practice: Check if object exists before creating
if "owner" not in st.session_state:
    st.session_state.owner = Owner(id="1", name="Alex")
else:
    # Reuse existing owner
    st.write(f"Welcome back, {st.session_state.owner.name}!")

# Only update if changed
if st.session_state.owner.name != new_name:
    st.session_state.owner.name = new_name
""", language="python")

st.divider()

# ----- Demo 5: Viewing Session State -----
st.header("🔬 View All Session Data")

if st.checkbox("Show all session state keys"):
    st.json(dict(st.session_state))

st.divider()

# ----- Key Takeaways -----
st.header("📚 Key Takeaways")

st.markdown("""
1. **Check before creating**: Use `if "key" not in st.session_state:` pattern
2. **Think of it as a vault**: Data survives reruns until browser tab closes
3. **Access like a dictionary**: `st.session_state["key"]` or `st.session_state.key`
4. **Store anything**: Strings, lists, dictionaries, custom objects (Owner, Pet, etc.)
5. **Initialize at the top**: Put initialization code early in your script

**Common Pattern:**
```python
# At the top of your script
if "owner" not in st.session_state:
    st.session_state.owner = None  # Initialize to None

# Later, when creating the object
if st.session_state.owner is None:
    st.session_state.owner = Owner(id="1", name=owner_name)
```
""")

# Reset button
if st.button("🔄 Reset All Session State"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
