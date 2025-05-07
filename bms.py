import streamlit as st
import pandas as pd
import mysql.connector

st.title("Battery Voltage Discharge Analysis")

# Button to trigger analysis
if st.button("Analyse Data"):

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host="82.180.143.66",
            user="u263681140_students",
            password="testStudents@123",
            database="u263681140_students"
        )

        # SQL query
        query = """
        SELECT 
            DATE(dateTime) AS date,
            MAX(CAST(vtg AS DECIMAL(10, 2))) AS max_voltage,
            MIN(CAST(vtg AS DECIMAL(10, 2))) AS min_voltage,
            (MAX(CAST(vtg AS DECIMAL(10, 2))) - MIN(CAST(vtg AS DECIMAL(10, 2)))) AS daily_discharge
        FROM BMS1
        WHERE CAST(vtg AS DECIMAL(10, 2)) > 9
        GROUP BY DATE(dateTime)
        ORDER BY DATE(dateTime);
        """

        # Read data into DataFrame
        df = pd.read_sql(query, conn)

        # Display the results
        st.success("Data Retrieved Successfully!")
        st.dataframe(df)

        # Optional: Add plot
        st.line_chart(df.set_index('date')['daily_discharge'])

        # Close connection
        conn.close()

    except Exception as e:
        st.error(f"Error: {e}")
