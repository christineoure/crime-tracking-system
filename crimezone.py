import mysql.connector
from mysql.connector import Error
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Major Incident Categories Dictionary
incident_categories = {
    "Terror Related": "Incidents related to terrorism",
    "Crime": "General crime incidents",
    "Conflict": "Ethnic or region-based conflicts",
    "Robbery": "Incidents involving theft or violent robbery",
    "Fraud": "Financial or identity fraud",
    "Social Crimes": "Socially motivated crimes like harassment or vandalism",
    "Other": "Other types of incidents not classified above"
}

# Step 1: Insert data into the database
def insert_crime_record(terror_related, crime, conflict, robbery, fraud, social_crimes, other, narrative, location, recommendation):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='crimes',
            user='root',
            password='Oure1234!%'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            query = '''
                INSERT INTO records (timestamp, `Terror Related`, Crime, Conflict, Robbery, Fraud, `Social Crimes`, Other, Narrative, Location, Recommendation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            timestamp = datetime.now()
            values = (timestamp, terror_related, crime, conflict, robbery, fraud, social_crimes, other, narrative, location, recommendation)
            cursor.execute(query, values)
            connection.commit()
            st.success(f"Record added successfully at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}!")
    except Error as e:
        st.error(f"Failed to insert record: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Step 2: Generate Reports
def generate_report(period):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='crimes',
            user='root',
            password='Oure1234!%'
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            if period == "Weekly":
                start_date = datetime.now() - timedelta(days=7)
            elif period == "Monthly":
                start_date = datetime.now() - timedelta(days=30)
            elif period == "Quarterly":
                start_date = datetime.now() - timedelta(days=90)
            elif period == "Annually":
                start_date = datetime.now() - timedelta(days=365)
            else:
                st.warning("Invalid report period selected.")
                return

            query = """
                SELECT id, timestamp, `Terror Related`, Crime, Conflict, Robbery, Fraud, `Social Crimes`, Other, Narrative, Location, Recommendation 
                FROM records WHERE timestamp >= %s
            """
            cursor.execute(query, (start_date,))
            records = cursor.fetchall()

            if records:
                df = pd.DataFrame(records)
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                st.subheader(f"{period} Report")
                st.write(df)
                st.success(f"Total records: {len(records)}")
            else:
                st.info(f"No records found for the selected {period} period.")
    except Error as e:
        st.error(f"Error generating report: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Step 3: Display records from the database
def display_crime_records():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='crimes',
            user='root',
            password='Oure1234!%'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT id, timestamp, `Terror Related`, Crime, Conflict, Robbery, Fraud, `Social Crimes`, Other, Narrative, Location, Recommendation FROM records")
            records = cursor.fetchall()
            if records:
                st.table(
                    [{"ID": r[0], "Timestamp": r[1].strftime('%Y-%m-%d %H:%M:%S'), "Terror Related": r[2], "Crime": r[3],
                      "Conflict": r[4], "Robbery": r[5], "Fraud": r[6], "Social Crimes": r[7], "Other": r[8],
                      "Narrative": r[9], "Location": r[10], "Recommendation": r[11]} for r in records]
                )
            else:
                st.info("No crime records available.")
    except Error as e:
        st.error(f"Error fetching records: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

# Step 4: Streamlit UI
def main():
    st.title("Crime Tracking System")
    st.subheader("Record details of crimes")

    # Input fields for the user
    st.write("### Incident Details")
    terror_related = st.text_input("Terror Related (Yes/No):")
    crime = st.text_input("Crime (General):")
    conflict = st.text_input("Conflict:")
    robbery = st.text_input("Robbery:")
    fraud = st.text_input("Fraud:")
    social_crimes = st.text_input("Social Crimes:")
    other = st.text_input("Other:")
    narrative = st.text_area("Narrative:", placeholder="Describe the incident in detail")
    location = st.text_input("Location:", placeholder="Enter location")
    recommendation = st.text_area("Recommendation:", placeholder="Add any recommendations")

    # Submit Button
    if st.button("Submit Incident Record"):
        if narrative and location:
            insert_crime_record(terror_related, crime, conflict, robbery, fraud, social_crimes, other, narrative, location, recommendation)
        else:
            st.warning("Please fill in all the mandatory fields.")

    # Display existing records
    st.subheader("Existing Crime Records")
    display_crime_records()

    # Generate reports
    st.subheader("Generate Reports")
    report_period = st.selectbox("Select Report Period:", ["Weekly", "Monthly", "Quarterly", "Annually"])
    if st.button("Generate Report"):
        generate_report(report_period)

if __name__ == "__main__":
    main()
