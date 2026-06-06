import streamlit as st
import json

# ==========================================
# 1. LOAD THE KNOWLEDGE BASE
# ==========================================
# This reads the external JSON file we just created
with open('kb.json', 'r') as file:
    rules = json.load(file)

# A dictionary to translate code variables into human-readable UI questions
# A dictionary to translate code variables into human-readable UI questions
question_map = {
    "power_led": {
        "text": "What is the state of the robot's main Power LED?", 
        "options": ["BRIGHT", "DIM", "OFF"]
    },
    "compilation_status": {
        "text": "Did your Arduino/Scratch code compile successfully?", 
        "options": ["SUCCESS_NO_ERRORS", "SYNTAX_ERROR"]
    },
    "motor_commanded": {
        "text": "What did you command the motors to do in your code?", 
        "options": ["FORWARD", "BACKWARD", "STOP"]
    },
    "physical_movement": {
        "text": "How is the physical robot moving?", 
        "options": ["FORWARD", "STOPPED", "SPINNING_RIGHT", "SPINNING_LEFT", "JITTERY_OR_WEAK"]
    },
    "serial_monitor": {
        "text": "How is the Serial Monitor behaving on your computer?", 
        "options": ["PRINTING_NORMALLY", "FROZEN_OR_CRASHING", "NO_OUTPUT"]
    }
}

# ==========================================
# 2. SESSION STATE (The Engine's Memory)
# ==========================================
if 'known_facts' not in st.session_state:
    st.session_state.known_facts = {} # Stores {symptom: (value, confidence)}
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = None

# ==========================================
# 3. BACKWARD CHAINING INFERENCE ENGINE
# ==========================================
def evaluate_hypotheses():
    """Goal-driven logic: Iterates through diagnoses and proves them backward."""
    for rule in rules:
        hypothesis = rule["diagnosis"]
        is_viable = True
        min_user_confidence = 1.0 # Used for Fuzzy Logic Math
        
        # Work backward through the required conditions
        for symptom, required_state in rule["conditions"].items():
            
            if symptom not in st.session_state.known_facts:
                # FACT MISSING: Pause engine, ask user
                st.session_state.current_question = symptom
                return 
            
            # FACT EXISTS: Check it
            user_val, user_cf = st.session_state.known_facts[symptom]
            
            if user_val != required_state:
                # HYPOTHESIS REJECTED: Mismatch
                is_viable = False
                break 
            else:
                # FACT MATCHES: Track the weakest link for Fuzzy Logic
                min_user_confidence = min(min_user_confidence, user_cf)
                
        if is_viable:
            # GOAL PROVEN!
            st.session_state.diagnosis = hypothesis
            st.session_state.final_cf = rule["base_certainty"] * min_user_confidence
            st.session_state.explanation = rule["explanation"]
            st.session_state.current_question = None
            return

    # If no hypotheses match
    st.session_state.diagnosis = "Inconclusive. The bug is outside our current knowledge base."
    st.session_state.current_question = None

# ==========================================
# 4. USER INTERFACE (Streamlit)
# ==========================================
st.set_page_config(page_title="RoboTutor Expert System", page_icon="🤖")
# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🤖 RoboTutor Navigation")
page = st.sidebar.radio("Go to:", ["🔍 Diagnostic Engine", "📚 View Knowledge Base"])

if page == "📚 View Knowledge Base":
    st.title("📚 Knowledge Base Explorer")
    st.write(f"The system currently contains **{len(rules)}** production rules.")
    
    # Loop through the JSON data and display it cleanly
    for i, rule in enumerate(rules):
        with st.expander(f"Rule {i+1}: {rule['diagnosis']}"):
            st.write("**IF the following conditions are met:**")
            for condition, value in rule['conditions'].items():
                st.code(f"{condition} == {value}")
            
            st.write(f"**THEN Confidence:** {rule['base_certainty'] * 100}%")
            st.info(f"**Explanation:** {rule['explanation']}")

elif page == "🔍 Diagnostic Engine":
    st.title("🤖 RoboTutor Diagnostics")
    st.write("Welcome to RoboTutor. I will ask you targeted questions to diagnose your hardware/software bug.")
    st.divider()
    
    # Start the engine
    if st.session_state.diagnosis is None and st.session_state.current_question is None:
        evaluate_hypotheses()
    
    # --- STATE 1: ASKING A QUESTION ---
    if st.session_state.current_question:
        q_data = question_map[st.session_state.current_question]
        
        st.subheader("Step 1: System Query")
        user_answer = st.selectbox(q_data["text"], ["Select..."] + q_data["options"])
        
        st.subheader("Step 2: Uncertainty Module")
        confidence_input = st.radio("How confident are you in this observation?", 
                                    ("High (100% Sure)", "Medium (Somewhat Sure)", "Low (Just guessing)"))
        
        if confidence_input == "High (100% Sure)":
            cf_multiplier = 1.0
        elif confidence_input == "Medium (Somewhat Sure)":
            cf_multiplier = 0.6
        else:
            cf_multiplier = 0.3
        
        if st.button("Submit Observation", type="primary"):
            if user_answer != "Select...":
                # Save fact and force app to rerun to check the next step
                st.session_state.known_facts[st.session_state.current_question] = (user_answer, cf_multiplier)
                st.session_state.current_question = None
                st.rerun()
            else:
                st.error("Please select an observation from the dropdown.")
    
    # --- STATE 2: DIAGNOSIS REACHED ---
    if st.session_state.diagnosis:
        st.success("### 🎯 Diagnosis Reached:")
        st.write(f"**{st.session_state.diagnosis}**")
        
        if "Inconclusive" not in st.session_state.diagnosis:
            st.warning(f"**Calculated System Confidence:** {st.session_state.final_cf * 100:.1f}%")
            
            # Hybrid Explanation Facility
            with st.expander("🤔 View Engine Reasoning (Explanation Facility)"):
                st.write("#### 1. Your Verified Observations (Dynamic Trace)")
                st.write("The Inference Engine worked backward and verified these facts:")
                for symptom, data in st.session_state.known_facts.items():
                    user_val, user_cf = data
                    st.write(f"- Checked **{symptom}**: You answered **{user_val}** *(Confidence: {user_cf})*")
                
                st.divider()
                st.write("#### 2. Pedagogical Context")
                st.info(st.session_state.explanation)
    
        st.divider()
        if st.button("Restart Consultation"):
            st.session_state.clear()
            st.rerun()