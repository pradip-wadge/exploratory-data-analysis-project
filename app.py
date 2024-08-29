import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    file_path = 'crime_data.csv'
    data = pd.read_csv(file_path)
    return data

crime_data = load_data()

# Sidebar filters
st.sidebar.header('Filters')

min_year, max_year = int(crime_data['Year'].min()), int(crime_data['Year'].max())
year_range = st.sidebar.slider('Select Year Range', min_year, max_year, (min_year, max_year))

# Allow 'All' to be selected for summing all crime types
crime_type = st.sidebar.selectbox('Select Crime Type', options=['All'] + list(crime_data.columns[4:-3]))

states = crime_data['STATE/UT'].unique()
selected_state = st.sidebar.selectbox('Select State/UT', options=['All'] + list(states))

districts = crime_data[crime_data['STATE/UT'] == selected_state]['DISTRICT'].unique() if selected_state != 'All' else crime_data['DISTRICT'].unique()
selected_district = st.sidebar.selectbox('Select District', options=['All'] + list(districts))

# Filtering the dataset based on selections
filtered_data = crime_data[(crime_data['Year'] >= year_range[0]) & (crime_data['Year'] <= year_range[1])]
if selected_state != 'All':
    filtered_data = filtered_data[filtered_data['STATE/UT'] == selected_state]
if selected_district != 'All':
    filtered_data = filtered_data[filtered_data['DISTRICT'] == selected_district]

# Crime trends over time
st.title('Crime Trends Over Time')

# Check if 'All' is selected for crime type
if crime_type == 'All':
    # Sum all crime types when 'All' is selected
    crime_trend = filtered_data.groupby('Year').sum().reset_index()
    fig_trend = px.line(crime_trend, x='Year', y='Total Crimes', title='Total Crimes Trend Over Years')
else:
    # Specific crime type selected
    crime_trend = filtered_data.groupby('Year')[crime_type].sum().reset_index()
    fig_trend = px.line(crime_trend, x='Year', y=crime_type, title=f'{crime_type} Trend Over Years')

# Display the trend chart
st.plotly_chart(fig_trend)

# Crime distribution by state
st.title('Crime Distribution by State')
state_distribution = filtered_data.groupby('STATE/UT')['Total Crimes'].sum().reset_index()
fig_distribution = px.bar(state_distribution, x='STATE/UT', y='Total Crimes', title='Total Crimes by State/UT')
st.plotly_chart(fig_distribution)

# Crime composition for a specific year
st.title('Crime Composition')
composition_data = filtered_data.sum().iloc[4:-3].reset_index()
composition_data.columns = ['Crime Type', 'Total']
fig_composition = px.pie(composition_data, names='Crime Type', values='Total', title=f'Crime Composition for Selected Period')
st.plotly_chart(fig_composition)