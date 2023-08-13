import streamlit as st
import random
import openpyxl
from datetime import datetime, timedelta

# Function definitions

def determine_recommendation_(hemoglobin_state, hematological_state, gender):
    if gender == 'Male':
        if hemoglobin_state == 'Severe Anemia' or hematological_state == 'Pancytopenia':
            return "Measure BP once a week"
        elif hemoglobin_state == 'Moderate Anemia' or hematological_state == 'Anemia':
            return "Measure BP every 3 days, Give aspirin 5g twice a week"
        elif hemoglobin_state == 'Mild Anemia' or hematological_state == 'Suspected Leukemia':
            return "Measure BP every day, Give aspirin 15g every day, Diet consultation"
        elif hemoglobin_state == 'Normal Hemoglobin' or hematological_state == 'Leukemoid reaction':
            return "Measure BP twice a day, Give aspirin 15g every day, Exercise consultation, Diet consultation"
        else:
            return "Measure BP every hour, Give 1 gr magnesium every hour, Exercise consultation, Call family"
    else: # Female
        if hemoglobin_state == 'Severe Anemia' or hematological_state == 'Pancytopenia':
            return "Measure BP every 3 days"
        elif hemoglobin_state == 'Moderate Anemia' or hematological_state == 'Anemia':
            return "Measure BP every 3 days, Give Celectone 2g twice a day for two days drug treatment"
        elif hemoglobin_state == 'Mild Anemia' or hematological_state == 'Suspected Leukemia':
            return "Measure BP every day, Give 1 gr magnesium every 3 hours, Diet consultation"
        elif hemoglobin_state == 'Normal Hemoglobin' or hematological_state == 'Leukemoid reaction':
            return "Measure BP twice a day, Give 1 gr magnesium every hour, Exercise consultation, Diet consultation"
        else:
            return "Measure BP every hour, Give 1 gr magnesium every hour, Exercise consultation, Call help"

def determine_hemoglobin_state(hemoglobin_level, gender):
    if gender == 'Male':
        if 0 <= hemoglobin_level <= 9:
            return "Severe Anemia"
        elif 9 < hemoglobin_level <= 11:
            return "Moderate Anemia"
        elif 11 < hemoglobin_level <= 13:
            return "Mild Anemia"
        elif 13 < hemoglobin_level <= 16:
            return "Normal Hemoglobin"
        else:
            return "Polyhemia"
    else: # Female
        if 0 <= hemoglobin_level <= 8:
            return "Severe Anemia"
        elif 8 < hemoglobin_level <= 10:
            return "Moderate Anemia"
        elif 10 < hemoglobin_level <= 12:
            return "Mild Anemia"
        elif 12 < hemoglobin_level <= 14:
            return "Normal Hemoglobin"
        else:
            return "Polyhemia"


def determine_hematological_state(hemoglobin_level, wbc_level, gender):
    # You've provided two tables for Hemoglobin-level -> WBC-level, so I'm using the first one here.
    if gender == 'Male' :
        if 0 <= hemoglobin_level <= 13:
            if 0 <= wbc_level <= 4000:
                return "Pancytopenia"
            elif 4000 < wbc_level <= 10000:
                return "Anemia"
            else:
                return "Suspected Leukemia"
        elif 13 < hemoglobin_level <= 16:
            if 0 <= wbc_level <= 4000:
                return "Leukopenia"
            elif 4000 < wbc_level <= 10000:
                return "Normal"
            else:
                return "Leukemoid reaction"
        else:
            if 0 <= wbc_level <= 4000:
                return "Suspected Polycytemia Vera"
            elif 4000 < wbc_level <= 10000:
                return "Polyhemia"
            else:
                return "Suspected Polycytemia Vera"
    else :#female
        if 0 <= hemoglobin_level <= 12:
            if 0 <= wbc_level <= 4000:
                return "Pancytopenia"
            elif 4000 < wbc_level <= 10000:
                return "Anemia"
            else:
                return "Suspected Leukemia"
        elif 12 < hemoglobin_level <= 14:
            if 0 <= wbc_level <= 4000:
                return "Leukopenia"
            elif 4000 < wbc_level <= 10000:
                return "Normal"
            else:
                return "Leukemoid reaction"
        else:
            if 0 <= wbc_level <= 4000:
                return "Suspected Polycytemia Vera"
            elif 4000 < wbc_level <= 10000:
                return "Polyhemia"
            else:
                return "Suspected Polycytemia Vera"





######## Streamlit App
st.title("Patient Information Viewer")

# Allow user to select a specific time and hour
selected_time = st.time_input("Select Time", value=datetime.now().time(), key="time_knowledgebase")

# Display selected time
st.write(f"Selected Time: {selected_time.strftime('%H:%M:%S')}")



names = ['Benjamin', 'David', 'Sarah', 'Emily', 'Michael', 'Matthew', 'Laura', 'Rebecca', 'Daniel', 'Jessica']
# Generate 10 patients

def generate_patient():
    patient_name = random.choice(names)
    names.remove(patient_name)  # remove the name from the list to ensure uniqueness
    
    age = random.randint(20, 80)
    gender = random.choice(['Male', 'Female'])
    hemoglobin_level = random.uniform(0, 17)
    wbc_level = random.randint(0, 15000)
    
    hemoglobin_state = determine_hemoglobin_state(hemoglobin_level, gender)
    hematological_state = determine_hematological_state(hemoglobin_level, wbc_level, gender)
    treatment_recommendation = determine_recommendation_(hemoglobin_state, hematological_state, gender)
    
    treatments = [
        "bp	recurrent	day	3	1", 
        "celectone	recurrent	day	1	2	2	g",
        "aspirin	recurrent	week	1	2	5	g"
    ]
    
    histories = [
        "Allergic State	Bronchospasm	none", 
        "Microalbumin [Mass/volume] in Urine by Test strip	5000	cells/ml", 
        "Hemoglobin [Mass/volume] in Arterial blood	9.3	gr/dl", 
        "Temperature of Skin	36.3	degrees-celsious", 
        "Color of Skin	Erythema	none",
        "Chills State	Shaking	none"
    ]
    
    treatment = random.choice(treatments)
    history_entries = random.sample(histories, 3)
    
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    
    return {
        'name': patient_name,
        'age': age,
        'gender': gender,
        'hemoglobin_level': hemoglobin_level,
        'wbc_level': wbc_level,
        'hemoglobin_state': hemoglobin_state,
        'hematological_state': hematological_state,
        'treatment_recommendation': treatment_recommendation,
        'treatment': treatment,
        'history': [
            {
                'entry': entry,
                'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                'previous_timestamp': yesterday.strftime('%Y-%m-%d %H:%M:%S')
            } for entry in history_entries
        ]
    }


patients = [generate_patient() for _ in range(10)]

# Select patient
selected_patient_name = st.selectbox("Select a patient", [patient['name'] for patient in patients])

for patient in patients : 
    if patient['name'] == selected_patient_name:
        st.markdown(f"### {patient['name']}'s Details")
        st.write(f"Age: {patient['age']}")
        st.write(f"Gender: {patient['gender']}")
        st.write(f"Hemoglobin Level: {patient['hemoglobin_level']:.2f}")
        st.write(f"WBC Level: {patient['wbc_level']}")
        st.write(f"Hemoglobin State: {patient['hemoglobin_state']}")
        st.write(f"Hematological State: {patient['hematological_state']}")
        st.write(f"Treatment Recommendation: {patient['treatment_recommendation']}")

        # Create tabs for states, treatments, and history
        selected_tab = st.selectbox("Select Tab", ["States", "Treatments", "History"])

        if selected_tab == "States" :
            st.write("### Patient States")
            st.write("Hemoglobin State:", patient['hemoglobin_state'])
            st.write("Hematological State:", patient['hematological_state'])
        elif selected_tab == "Treatments" :
            st.write("### Patient Treatments")
            st.write("Treatment Recommendation:", patient['treatment_recommendation'])
            st.write("Current Treatment:", patient['treatment'])
        elif selected_tab == 'History' :
            st.write("### Patient History")
            st.write("Recent History Entries:")
            for entry in patient['history']:
                st.write(f"- {entry['entry']} (Timestamp: {entry['timestamp']}, Previous Timestamp: {entry['previous_timestamp']})")

    






import streamlit as st
import random
from datetime import datetime, timedelta

# Function definitions

def determine_recommendation_(hemoglobin_state, hematological_state, gender):
    if gender == 'Male':
        if hemoglobin_state == 'Severe Anemia' or hematological_state == 'Pancytopenia':
            return "Measure BP once a week"
        elif hemoglobin_state == 'Moderate Anemia' or hematological_state == 'Anemia':
            return "Measure BP every 3 days, Give aspirin 5g twice a week"
        elif hemoglobin_state == 'Mild Anemia' or hematological_state == 'Suspected Leukemia':
            return "Measure BP every day, Give aspirin 15g every day, Diet consultation"
        elif hemoglobin_state == 'Normal Hemoglobin' or hematological_state == 'Leukemoid reaction':
            return "Measure BP twice a day, Give aspirin 15g every day, Exercise consultation, Diet consultation"
        else:
            return "Measure BP every hour, Give 1 gr magnesium every hour, Exercise consultation, Call family"
    else: # Female
        if hemoglobin_state == 'Severe Anemia' or hematological_state == 'Pancytopenia':
            return "Measure BP every 3 days"
        elif hemoglobin_state == 'Moderate Anemia' or hematological_state == 'Anemia':
            return "Measure BP every 3 days, Give Celectone 2g twice a day for two days drug treatment"
        elif hemoglobin_state == 'Mild Anemia' or hematological_state == 'Suspected Leukemia':
            return "Measure BP every day, Give 1 gr magnesium every 3 hours, Diet consultation"
        elif hemoglobin_state == 'Normal Hemoglobin' or hematological_state == 'Leukemoid reaction':
            return "Measure BP twice a day, Give 1 gr magnesium every hour, Exercise consultation, Diet consultation"
        else:
            return "Measure BP every hour, Give 1 gr magnesium every hour, Exercise consultation, Call help"

def determine_hemoglobin_state(hemoglobin_level, gender):
    if gender == 'Male':
        if 0 <= hemoglobin_level <= 9:
            return "Severe Anemia"
        elif 9 < hemoglobin_level <= 11:
            return "Moderate Anemia"
        elif 11 < hemoglobin_level <= 13:
            return "Mild Anemia"
        elif 13 < hemoglobin_level <= 16:
            return "Normal Hemoglobin"
        else:
            return "Polyhemia"
    else: # Female
        if 0 <= hemoglobin_level <= 8:
            return "Severe Anemia"
        elif 8 < hemoglobin_level <= 10:
            return "Moderate Anemia"
        elif 10 < hemoglobin_level <= 12:
            return "Mild Anemia"
        elif 12 < hemoglobin_level <= 14:
            return "Normal Hemoglobin"
        else:
            return "Polyhemia"


def determine_hematological_state(hemoglobin_level, wbc_level, gender):
    # You've provided two tables for Hemoglobin-level -> WBC-level, so I'm using the first one here.
    if gender == 'Male' :
        if 0 <= hemoglobin_level <= 13:
            if 0 <= wbc_level <= 4000:
                return "Pancytopenia"
            elif 4000 < wbc_level <= 10000:
                return "Anemia"
            else:
                return "Suspected Leukemia"
        elif 13 < hemoglobin_level <= 16:
            if 0 <= wbc_level <= 4000:
                return "Leukopenia"
            elif 4000 < wbc_level <= 10000:
                return "Normal"
            else:
                return "Leukemoid reaction"
        else:
            if 0 <= wbc_level <= 4000:
                return "Suspected Polycytemia Vera"
            elif 4000 < wbc_level <= 10000:
                return "Polyhemia"
            else:
                return "Suspected Polycytemia Vera"
    else :#female
        if 0 <= hemoglobin_level <= 12:
            if 0 <= wbc_level <= 4000:
                return "Pancytopenia"
            elif 4000 < wbc_level <= 10000:
                return "Anemia"
            else:
                return "Suspected Leukemia"
        elif 12 < hemoglobin_level <= 14:
            if 0 <= wbc_level <= 4000:
                return "Leukopenia"
            elif 4000 < wbc_level <= 10000:
                return "Normal"
            else:
                return "Leukemoid reaction"
        else:
            if 0 <= wbc_level <= 4000:
                return "Suspected Polycytemia Vera"
            elif 4000 < wbc_level <= 10000:
                return "Polyhemia"
            else:
                return "Suspected Polycytemia Vera"





######## Streamlit App
st.title("Patient Information Viewer")

# Allow user to select a specific time and hour
selected_time = st.time_input("Select Time", value=datetime.now().time())

# Display selected time
st.write(f"Selected Time: {selected_time.strftime('%H:%M:%S')}")



names = ['Benjamin', 'David', 'Sarah', 'Emily', 'Michael', 'Matthew', 'Laura', 'Rebecca', 'Daniel', 'Jessica']
# Generate 10 patients

def generate_patient():
    patient_name = random.choice(names)
    names.remove(patient_name)  # remove the name from the list to ensure uniqueness
    
    age = random.randint(20, 80)
    gender = random.choice(['Male', 'Female'])
    hemoglobin_level = random.uniform(0, 17)
    wbc_level = random.randint(0, 15000)
    
    hemoglobin_state = determine_hemoglobin_state(hemoglobin_level, gender)
    hematological_state = determine_hematological_state(hemoglobin_level, wbc_level, gender)
    treatment_recommendation = determine_recommendation_(hemoglobin_state, hematological_state, gender)
    
    treatments = [
        "bp	recurrent	day	3	1", 
        "celectone	recurrent	day	1	2	2	g",
        "aspirin	recurrent	week	1	2	5	g"
    ]
    
    histories = [
        "Allergic State	Bronchospasm	none", 
        "Microalbumin [Mass/volume] in Urine by Test strip	5000	cells/ml", 
        "Hemoglobin [Mass/volume] in Arterial blood	9.3	gr/dl", 
        "Temperature of Skin	36.3	degrees-celsious", 
        "Color of Skin	Erythema	none",
        "Chills State	Shaking	none"
    ]
    
    treatment = random.choice(treatments)
    history_entries = random.sample(histories, 3)
    
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    
    return {
        'name': patient_name,
        'age': age,
        'gender': gender,
        'hemoglobin_level': hemoglobin_level,
        'wbc_level': wbc_level,
        'hemoglobin_state': hemoglobin_state,
        'hematological_state': hematological_state,
        'treatment_recommendation': treatment_recommendation,
        'treatment': treatment,
        'history': [
            {
                'entry': entry,
                'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                'previous_timestamp': yesterday.strftime('%Y-%m-%d %H:%M:%S')
            } for entry in history_entries
        ]
    }


patients = [generate_patient() for _ in range(10)]

# Select patient
selected_patient_name = st.selectbox("Select a patient", [patient['name'] for patient in patients])

for patient in patients : 
    if patient['name'] == selected_patient_name:
        st.markdown(f"### {patient['name']}'s Details")
        st.write(f"Age: {patient['age']}")
        st.write(f"Gender: {patient['gender']}")
        st.write(f"Hemoglobin Level: {patient['hemoglobin_level']:.2f}")
        st.write(f"WBC Level: {patient['wbc_level']}")
        st.write(f"Hemoglobin State: {patient['hemoglobin_state']}")
        st.write(f"Hematological State: {patient['hematological_state']}")
        st.write(f"Treatment Recommendation: {patient['treatment_recommendation']}")

        # Create tabs for states, treatments, and history
        selected_tab = st.selectbox("Select Tab", ["States", "Treatments", "History"], key="select_knowledgebase")

        if selected_tab == "States" :
            st.write("### Patient States")
            st.write("Hemoglobin State:", patient['hemoglobin_state'])
            st.write("Hematological State:", patient['hematological_state'])
        elif selected_tab == "Treatments" :
            st.write("### Patient Treatments")
            st.write("Treatment Recommendation:", patient['treatment_recommendation'])
            st.write("Current Treatment:", patient['treatment'])
        elif selected_tab == 'History' :
            st.write("### Patient History")
            st.write("Recent History Entries:")
            for entry in patient['history']:
                st.write(f"- {entry['entry']} (Timestamp: {entry['timestamp']}, Previous Timestamp: {entry['previous_timestamp']})")

    






