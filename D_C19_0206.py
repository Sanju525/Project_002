import ibm_db
# import ibm_db_dbi
import pandas as pd
import streamlit as st
import altair as alt
# import numpy as np
# from vega_datasets import data

# Replace the placeholder values with your actual Db2 hostname, username, and password:

dsn_hostname = "dashdb-txn-sbox-yp-lon02-02.services.eu-gb.bluemix.net" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
dsn_uid = "ctq40624"        # e.g. "abc12345"
dsn_pwd = "c52g+549kn1s6wb1"      # e.g. "7dBZ3wWt9XN6$o0J"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"            # e.g. "BLUDB"
dsn_port = "50000"                # e.g. "50000"
dsn_protocol = "TCPIP"            # i.e. "TCPIP"

# Create the dsn connection string
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

#print the connection string to check correct values are specified
# print(dsn)

# ====== Data Initialization ======= #
chart_data = pd.DataFrame()

State_data = []
ActiveCases_data = []
Cured_data = []
Death_data = []
Confirmed_data = []

# =================================== #

#Create database connection

try:
    conn = ibm_db.connect(dsn, "", "")
    # print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)
    print()
    # data0 = pd.read_sql('select * from C19_0206', pconn)
    sql = "select * from C19_0206"
    dataExec = ibm_db.exec_immediate(conn, sql)
    data_fetched_loop = ibm_db.fetch_both(dataExec)
    while data_fetched_loop:
        # print("NAMEOFSTATE_UT", data_fetched_loop[0])
        State_data.append(data_fetched_loop[0])
        ActiveCases_data.append(data_fetched_loop[1])
        Cured_data.append(data_fetched_loop[2])
        Death_data.append(data_fetched_loop[3])
        Confirmed_data.append(data_fetched_loop[4])
        data_fetched_loop = ibm_db.fetch_both(dataExec)
    try:
        ibm_db.close(conn)
        print('Connection Closed')
    except:
        print('Connection Still ON')

except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )
    exit(0)

chart_data['NameofState'] = State_data
chart_data['Active_cases'] = ActiveCases_data
chart_data['Cured_data'] = Cured_data
chart_data['Death_data'] = Death_data
chart_data['Confirmed_data'] = Confirmed_data




# print(chart_data)
# print(chart_data)
st.title('COVID 19 INDIA')
st.header('Day 02-06-2020')

def chartM_v1():
    chart_v1 = alt.Chart(chart_data).mark_bar().encode(
    x='NameofState',
    y='Active_cases',
    ).properties(title='State v/s ActiveCases',height=500)
    st.altair_chart(chart_v1)
    if st.checkbox('Show Raw Data'):
        st.dataframe(data = pd.DataFrame({'State':State_data,'Active Cases': ActiveCases_data},columns=['State','Active Cases']), height=930, width=500)
def chartM_v2():
    chart_v2 = alt.Chart(chart_data).mark_bar().encode(
        x='NameofState',
        y='Cured_data'
    ).properties(title='State v/s Cured_cases', height=500)
    st.altair_chart(chart_v2)
    if st.checkbox('Show Raw Data'):
        st.dataframe(data = pd.DataFrame({'State':State_data,'Cured/Migrated/Discharged': Cured_data},columns=['State','Cured/Migrated/Discharged']), height=930, width=500)
def chartM_v3():
    chart_v3 = alt.Chart(chart_data).mark_bar().encode(
        x='NameofState',
        y='Death_data'
    ).properties(title="State v/s Death's",height=500)
    st.altair_chart(chart_v3)
    if st.checkbox('Show Raw Data'):
        st.dataframe(data = pd.DataFrame({'State':State_data,'Death\'s': Death_data},columns=['State','Death\'s']), height=930, width=500)
def chartM_v4():
    chart_v4 = alt.Chart(chart_data).mark_bar().encode(
        x='NameofState',
        y='Confirmed_data'
    ).properties(title="State v/s Confirmed Cases", height=500)
    st.altair_chart(chart_v4)
    if st.checkbox('Show Raw Data'):
        st.dataframe(data = pd.DataFrame({'State':State_data,'Confirmed Cases': Confirmed_data},columns=['State','Confirmed Cases']), height=930, width=500)

add_selectbox = st.sidebar.selectbox(
    'Select a graph to show',
    ('Name of State v/s Active Cases',\
     'Name of State v/s Cured',\
     'Name of State v/s Deaths',\
     'Name of State v/s Confirmed Cases')
)
if add_selectbox == 'Name of State v/s Active Cases':
    chartM_v1()
elif add_selectbox == 'Name of State v/s Cured':
    chartM_v2()
elif add_selectbox == 'Name of State v/s Deaths':
    chartM_v3()
else:
    chartM_v4()