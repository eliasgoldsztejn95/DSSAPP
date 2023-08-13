import streamlit as st
import datetime
from datetime import  timedelta
import pandas as pd
import io
import copy

st.set_page_config(layout="wide")


# Use st.beta_columns() to create columns
col1, col2, col3 = st.columns([1, 2, 2])  # Adjust the column widths as needed

# Provide a unique key for the date input widget
current_date_input_key = "current_date_input_key"
current_time_input_key = "current_time_input_key"

valid_date_input_key = "valid_date_input_key"
valid_time_input_key = "valid_time_input_key"

valid_start_date_input_key = "valid_start_date_input_key"
valid_start_time_input_key = "valid_start_hout_input_key"

valid_end_date_input_key = "valid_end_date_input_key"
valid_end_time_input_key = "valid_time_input_key"

valid_insert_date_input_key = "valid_insert_date_input_key"
valid_insert_time_input_key = "valid_insert_time_input_key"

valid_delete_date_input_key = "valid_delete_date_input_key"

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = False

# Global variables

with col1:
    st.title("Data")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
    if uploaded_file:
        st.session_state['is_uploaded_file'] = True
        st.session_state['uploaded_file'] = uploaded_file

    if st.session_state['uploaded_file']:
        # Read Excel file
        df = pd.read_excel(st.session_state['uploaded_file'], engine='openpyxl')

        # Create editable file
        edited_df = None
        if "edited_df" not in st.session_state:
            st.session_state['edited_df'] = copy.deepcopy(df)
            edited_df = st.session_state['edited_df']
            # Add Valid stop time column
            edited_df['Valid stop time'] = None
            st.session_state['edited_df'] = edited_df
        edited_df = st.session_state['edited_df']
        
        # Allow user to download edited Excel file
        if st.button("Download Edited Excel"):
            # Convert edited dataframe to Excel bytes
            edited_excel = io.BytesIO()
            edited_df.to_excel(edited_excel, index=False, engine='openpyxl')
            edited_excel.seek(0)

            # Create a link for downloading the edited Excel file
            st.download_button(
                label="Download Edited Excel",
                data=edited_excel,
                file_name="edited_excel.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
with col2:
    if st.session_state['uploaded_file']:
        st.title("Date and Patient")
        current_date = st.date_input("Select current date", datetime.date.today(), key=current_date_input_key)

        # Select hour
        current_hour = st.time_input("Select current time", key=current_time_input_key)

        current_datetime = datetime.datetime.combine(current_date, current_hour)
        # Display selected time
        #st.write("Selected Date and Time:", selected_date, selected_hour)

        # Combine "Name" and "Surname" columns and get unique combinations
        unique_names_surnames = edited_df["First name"] + " " + edited_df["Last name"]
        unique_names_surnames = unique_names_surnames.unique()

        # Create a selectbox to choose from unique combinations
        selected_name_surname = st.selectbox("Select a Name and Surname", unique_names_surnames)

        #st.write("You selected:", selected_name_surname)

selected_option = None

with col3:
    if st.session_state['uploaded_file']:
        st.title("Actions")
        # Create radio buttons for different options
        selected_option = st.radio("Select an option", ["Find 🔍", "History 🧾", "Insert ✏️", "Delete ❌"])

        # Display content based on the selected option
        if selected_option == "Find 🔍":
            st.write("Find tests done by patient since specified date.")

        elif selected_option == "History 🧾":
            st.write("Show history of tests for patient between dates.")

        elif selected_option == "Insert ✏️":
            st.write("Insert new value for past test.")

        elif selected_option == "Delete ❌":
            st.write("Delete patient test.")

#### General Functions go Here #####


# Function to filter Excel data based on date and hour range
def filter_excel_data_by_date(data, target_datetime, type, inequality):
    if inequality == 'after':
        filtered_data = data[data[type].apply(lambda x: x >= target_datetime)]
    elif inequality == 'before':
        filtered_data = data[data[type].apply(lambda x: x <= target_datetime)]
    elif inequality == 'equal':
        start_time = target_datetime - timedelta(minutes=15)
        end_time = target_datetime + timedelta(minutes=15)
        filtered_data = data[(data[type].apply(lambda x: x >= start_time)) & (data[type].apply(lambda x: x <= end_time))]
    elif inequality == 'latest':
        filtered_data = data[(data[type].dt.date == target_datetime)]
        if not filtered_data.empty:
            max_hour = filtered_data[type].dt.hour.max()
            max_hour_rows = filtered_data[filtered_data[type].dt.hour == max_hour]
            return max_hour_rows
        else:
            return None
    return filtered_data

def return_edited_file():
    if 'uploaded_file' not in st.session_state:
        return None
    if st.session_state['uploaded_file']:
        edited_df = copy.deepcopy(st.session_state['edited_df'])
        return edited_df
    return None

def session_state_date(name, phrase):
    select = None
    if name not in st.session_state:
        select = st.date_input(phrase, datetime.date.today(), key=name)
        st.session_state[name] = select
    else:
        select = st.date_input(phrase, st.session_state[name], key=name)
        st.session_state[name] = select
    return select
############################################################

if selected_option == "Find 🔍":
    # Sidebar input for Name and Surname
    st.write(f"<b>FIND TESTS for: {selected_name_surname} <b>", unsafe_allow_html=True)
    name_surname =  selected_name_surname.split(" ")
    name_input = name_surname[0]
    surname_input = name_surname[1]

    # Filter the DataFrame based on Name and Surname
    filtered_df = edited_df[(edited_df["First name"] == name_input) & (edited_df["Last name"] == surname_input)]

    # Display the list of unique values in the "loic-num" column
    if not filtered_df.empty:
        unique_nums = filtered_df["LOINC-NUM"].unique()
        selected_num = st.selectbox("Select LOINC-NUM",unique_nums)
    else:
        st.write("No matching records found.")

    valid_date = None
    if "valid_date_find" not in st.session_state:
        valid_date = st.date_input("Select valid date", datetime.date.today(), key=valid_date_input_key)
        st.session_state['valid_date_find'] = valid_date
    else:
        #valid_date = st.session_state['valid_date_find']
        valid_date = st.date_input("Select valid date", st.session_state['valid_date_find'], key=valid_date_input_key)
        st.session_state['valid_date_find'] = valid_date

    # Select hour
    include_hour = st.checkbox("Include time", value=False)
    valid_hour = None

    if include_hour:
        default_time = datetime.time(0, 0)  # Represents "None" or no time selected
        valid_hour = st.time_input("Select time", value=default_time, key = valid_time_input_key)

    ########## Write Logic ######
    if include_hour:
        valid_datetime = datetime.datetime.combine(valid_date, valid_hour)

    if (valid_date <= current_date) or ((valid_date == current_date) if include_hour is False else  ((valid_date == current_date) and (valid_hour <= current_hour))):
        # Filter LOIC-NUM
        value_find = filtered_df[(filtered_df["LOINC-NUM"] == selected_num)]
        # Filter date
        value_find = filter_excel_data_by_date(value_find, current_datetime, "Transaction time", "before")
        if include_hour:
            value_find = filter_excel_data_by_date(value_find, valid_datetime, "Valid start time", "equal")
        else:
            value_find = filter_excel_data_by_date(value_find, valid_date, "Valid start time", "latest")
        if value_find is None or value_find.empty:
            st.warning("No matches found.")
        else:
            st.write("Requested Data:")
            st.dataframe(value_find)
    else:
        st.error("Please select a valid date range.")


elif selected_option == "History 🧾":
    # Sidebar input for Name and Surname
    st.write(f"<b>HISTORY for: {selected_name_surname} <b>", unsafe_allow_html=True)
    name_surname =  selected_name_surname.split(" ")
    name_input = name_surname[0]
    surname_input = name_surname[1]

    # Filter the DataFrame based on Name and Surname
    filtered_df = edited_df[(edited_df["First name"] == name_input) & (edited_df["Last name"] == surname_input)]

    # Display the list of unique values in the "loic-num" column
    if not filtered_df.empty:
        unique_nums = filtered_df["LOINC-NUM"].unique()
        selected_num = st.selectbox("Select LOINC-NUM",unique_nums, key="history_loinc")
    else:
        st.write("No matching records found.")
    
    # Date
    col4, col5 = st.columns(2)
    default_time = datetime.time(0, 0) 
    with col4:
        valid_start_date = None
        if "valid_start_date" not in st.session_state:
            valid_start_date = st.date_input("From valid date", datetime.date.today(), key=valid_start_date_input_key)
            st.session_state['valid_start_date'] = valid_start_date
        else:
            valid_start_date = st.date_input("From valid date", st.session_state['valid_start_date'], key=valid_start_date_input_key)
            st.session_state['valid_start_date'] = valid_start_date

        valid_end_date = None
        if "valid_end_date" not in st.session_state:
            valid_end_date = st.date_input("To valid date", datetime.date.today(), key=valid_end_date_input_key)
            st.session_state['valid_end_date'] = valid_end_date
        else:
            valid_end_date = st.date_input("To valid date", st.session_state['valid_end_date'], key=valid_end_date_input_key)
            st.session_state['valid_end_date'] = valid_end_date
        #valid_end_date = st.date_input("To valid date", datetime.date.today(), key=valid_end_date_input_key)
    with col5:
        #valid_start_hour = st.time_input("From valid time", value=default_time, key = valid_start_time_input_key)
        valid_start_hour = None
        if "valid_start_hour" not in st.session_state:
            valid_start_hour = st.time_input("To valid time", default_time, key=valid_start_time_input_key)
            st.session_state['valid_start_hour'] = valid_start_hour
        else:
            valid_start_hour = st.time_input("To valid time", st.session_state['valid_start_hour'], key=valid_start_time_input_key)
            st.session_state['valid_start_hour'] = valid_start_hour
        include_history_hour = st.checkbox("Include time", key= "history_include_time", value=False)

        valid_end_hour = datetime.time(0, 0) 
        if include_history_hour:
            valid_end_hour = st.time_input("To valid time",  value=default_time, key=valid_end_time_input_key)

    ########## Write Logic ######
    valid_start_datetime = datetime.datetime.combine(valid_start_date, valid_start_hour)
    if include_history_hour:
        valid_end_datetime = datetime.datetime.combine(valid_end_date, valid_end_hour)
    valid_end_datetime = datetime.datetime.combine(valid_end_date, valid_end_hour)

    if (valid_start_datetime <= current_datetime) and  ((valid_start_date <= valid_end_date) or
                                                      ((valid_start_date == valid_end_date) if include_history_hour is False else  
                                                       ((valid_start_date == valid_end_date) and (valid_start_hour <= valid_end_hour)))):
        # Filter LOIC-NUM
        value_find = filtered_df[(filtered_df["LOINC-NUM"] == selected_num)]
        # Filter date
        value_find = filter_excel_data_by_date(value_find, current_datetime, "Transaction time", "before")
        if include_history_hour:
            value_find = filter_excel_data_by_date(value_find, valid_start_datetime, "Valid start time", "after")
            value_find = filter_excel_data_by_date(value_find, valid_end_datetime, "Valid start time", "before")
        else:
            value_find = filter_excel_data_by_date(value_find, valid_start_datetime, "Valid start time", "after")
            value_find = filter_excel_data_by_date(value_find, valid_end_datetime, "Valid start time", "before")
        if value_find is None or value_find.empty:
            st.warning("No matches found.")
        else:
            st.write("Requested Data:")
            st.dataframe(value_find)
    else:
        st.error("Please select a valid date range.")

elif selected_option == "Insert ✏️":
    # Sidebar input for Name and Surname
    st.write(f"<b>INSERT VALUE for: {selected_name_surname} <b>", unsafe_allow_html=True)
    name_surname =  selected_name_surname.split(" ")
    name_input = name_surname[0]
    surname_input = name_surname[1]

    # Filter the DataFrame based on Name and Surname
    filtered_df = edited_df[(edited_df["First name"] == name_input) & (edited_df["Last name"] == surname_input)]

    # Display the list of unique values in the "loic-num" column
    if not filtered_df.empty:
        unique_nums = filtered_df["LOINC-NUM"].unique()
        selected_num = st.selectbox("Select LOINC-NUM",unique_nums, key="loinc_insert")
    else:
        st.write("No matching records found.")

    # Select date
    valid_insert_date = None
    if "valid_insert_date" not in st.session_state:
        valid_insert_date = st.date_input("Select valid date", datetime.date.today(), key=valid_insert_date_input_key)
        st.session_state['valid_insert_date'] = valid_insert_date
    else:
        valid_insert_date = st.date_input("Select valid date", st.session_state['valid_insert_date'], key=valid_insert_date_input_key)
        st.session_state['valid_insert_date'] = valid_insert_date

    # Select hour
    valid_insert_hour = None
    if "valid_insert_hour" not in st.session_state:
        valid_insert_hour = st.time_input("Select valid time", key=valid_insert_time_input_key)
        st.session_state['valid_insert_hour'] = valid_insert_hour
    else:
        valid_insert_hour = st.time_input("Select valid time", st.session_state['valid_insert_hour'], key=valid_insert_time_input_key)
        st.session_state['valid_insert_hour'] = valid_insert_hour

    ########## Write Logic ######
    valid_datetime = datetime.datetime.combine(valid_insert_date, valid_insert_hour)

    if (valid_datetime <= current_datetime):
        
        numeric_value = st.number_input("Enter new value:")
        selected = st.button("Update", key= "check_insert")
        if selected:
            
            # Filter LOIC-NUM
            value_find = filtered_df[(filtered_df["LOINC-NUM"] == selected_num)]
            # Filter date
            value_find = filter_excel_data_by_date(value_find, current_datetime, "Transaction time", "before")
            value_find = filter_excel_data_by_date(value_find, valid_datetime, "Valid start time", "equal")

            if value_find is None or value_find.empty:
                st.warning("No matches found.")
            else:
                # Insert new row
                # Append the new row to the DataFrame

                # New row
                name_surname = selected_name_surname.split(" ")
                new_row_data = {}
                new_row_data["First name"] = name_surname[0]
                new_row_data["Last name"] = name_surname[1]
                new_row_data["LOINC-NUM"] = selected_num
                new_row_data["Value"] = numeric_value
                new_row_data["Unit"] = value_find["Unit"][0]
                new_row_data["Valid start time"] = value_find["Valid start time"][0]
                new_row_data["Transaction time"] = current_datetime
                
                new_row = pd.DataFrame([new_row_data], columns=edited_df.columns)
                edited_df = pd.concat([edited_df, new_row], ignore_index=True)

                st.session_state['edited_df'] = edited_df
                
                st.write("Old Data:")
                st.dataframe(value_find)
                st.write("Data added:")
                st.dataframe(new_row)
        else:
            st.warning("Press update button to insert new value")
    else:
        st.error("Please select a valid date range.")

elif selected_option == "Delete ❌":
    # Sidebar input for Name and Surname
    st.write(f"<b>FIND TESTS for: {selected_name_surname} <b>", unsafe_allow_html=True)
    name_surname =  selected_name_surname.split(" ")
    name_input = name_surname[0]
    surname_input = name_surname[1]

    # Filter the DataFrame based on Name and Surname
    filtered_df = edited_df[(edited_df["First name"] == name_input) & (edited_df["Last name"] == surname_input)]

    # Display the list of unique values in the "loic-num" column
    if not filtered_df.empty:
        unique_nums = filtered_df["LOINC-NUM"].unique()
        selected_num = st.selectbox("Select LOINC-NUM",unique_nums , key="loinc_delete")
    else:
        st.write("No matching records found.")

    # Select date
    valid_date_delete = None
    if "valid_date_delete" not in st.session_state:
        valid_date_delete = st.date_input("Select valid date", datetime.date.today(), key=valid_delete_date_input_key)
        st.session_state['valid_date_delete'] = valid_date_delete
    else:
        valid_date_delete = st.date_input("Select valid date", st.session_state['valid_date_delete'], key=valid_delete_date_input_key)
        st.session_state['valid_date_delete'] = valid_date_delete
    # Select hour
    include_hour = st.checkbox("Include time", value=False, key= "checkbox_include_delete")
    valid_hour = None

    if include_hour:
        default_time = datetime.time(0, 0)  # Represents "None" or no time selected
        valid_hour = st.time_input("Select time", value=default_time, key = "valid_time_delete")

    selected_new_current_date = st.checkbox("Use deletion time? (Default is current time)", key= "check_new_delete")
    if selected_new_current_date:
        delete_current_date = st.date_input("Select deletion date", datetime.date.today(), key="delete_current_date")

        default_time = datetime.time(0, 0)  # Represents "None" or no time selected
        delete_current_hour = st.time_input("Select time", value=default_time, key = "current_time_delete")

    ########## Write Logic ######
    if include_hour:
        valid_datetime = datetime.datetime.combine(valid_date_delete, valid_hour)

    if (valid_date_delete <= current_date) or ((valid_date_delete == current_date) if include_hour is False else  ((valid_date_delete == current_date) and (valid_hour <= current_hour))):
        # Filter LOIC-NUM
        value_find = filtered_df[(filtered_df["LOINC-NUM"] == selected_num)]
        # Filter date
        selected = st.button("Delete", key= "check_delete")
        if selected:
            value_find = filter_excel_data_by_date(value_find, current_datetime, "Transaction time", "before")
            if include_hour:
                value_find = filter_excel_data_by_date(value_find, valid_datetime, "Valid start time", "equal")
            else:
                value_find = filter_excel_data_by_date(value_find, valid_date_delete, "Valid start time", "latest")
            if value_find is None or value_find.empty:
                st.warning("No matches found.")
            else:
                st.write("Deleted data:")
                for index, row in edited_df.iterrows():
                    for find_index, find_row in value_find.iterrows():
                        if row.equals(find_row):
                            if selected_new_current_date:
                                edited_df.loc[index, "Valid stop time"] = datetime.datetime.combine(delete_current_date, delete_current_hour)
                            else:
                                edited_df.loc[index, "Valid stop time"] = current_datetime
                            data = edited_df.iloc[index]
                            equal_rows = edited_df[(edited_df == data).all(axis=1)]
                            st.dataframe(equal_rows)
                st.session_state['edited_df'] = edited_df
            
    else:
        st.error("Please select a valid date range.")
