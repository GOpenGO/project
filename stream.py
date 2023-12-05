import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import warnings

warnings.simplefilter('ignore')

df = pd.read_csv("tobacco.csv")
df['Smoke everyday'] = df['Smoke everyday'].str.rstrip('%').astype(float)
df['Smoke some days'] = df['Smoke some days'].str.rstrip('%').astype(float)
df['Former smoker'] = df['Former smoker'].str.rstrip('%').astype(float)
df['Never smoked'] = df['Never smoked'].str.rstrip('%').astype(float)
df = df.dropna()

new_df = df.groupby('Year')['Smoke everyday'].mean().reset_index()
plt.plot(
    new_df['Year'],
    new_df['Smoke everyday']
)
st.pyplot(plt)
plt.clf()
new_df = df.groupby('Year')['Former smoker'].mean().reset_index()
plt.scatter(
    "Year",
    "Former smoker",
    data=new_df,
)
st.pyplot(plt)
plt.clf()
plt.hist(df["Never smoked"], bins=20)
plt.title("Non-smokers")
plt.xlabel("Percent")
plt.ylabel("Count")
st.pyplot(plt)
plt.clf()
new_df = df.groupby('Year')['Smoke everyday'].mean().reset_index()
new1_df = df.groupby('Year')['Smoke some days'].mean().reset_index()
f_df = pd.merge(new_df, new1_df, on="Year")
f_df['Sum'] = f_df['Smoke everyday'] + f_df['Smoke some days']
f_df = f_df.drop('Smoke everyday', axis=1)
f_df = f_df.drop('Smoke some days', axis=1)

new_df = df.groupby('Year')['Former smoker'].mean().reset_index()
new1_df = df.groupby('Year')['Never smoked'].mean().reset_index()
f1_df = pd.merge(new_df, new1_df, on="Year")
f1_df['Sum'] = f1_df['Former smoker'] + f1_df['Never smoked']
f1_df = f1_df.drop('Former smoker', axis=1)
f1_df = f1_df.drop('Never smoked', axis=1)
plt.plot(f1_df['Sum'], label="Not smoking")
plt.plot(f_df['Sum'], label="Smoking")
plt.legend()
st.pyplot(plt)
plt.clf()

new_df = df.groupby('State')['Smoke everyday'].mean().reset_index()
new1_df = df.groupby('State')['Smoke some days'].mean().reset_index()
f_df = pd.merge(new_df, new1_df, on="State")
f_df['Sum'] = f_df['Smoke everyday'] + f_df['Smoke some days']
f_df = f_df.drop('Smoke everyday', axis=1)
f_df = f_df.drop('Smoke some days', axis=1)

new_df = df.groupby('State')['Former smoker'].mean().reset_index()
new1_df = df.groupby('State')['Never smoked'].mean().reset_index()
f1_df = pd.merge(new_df, new1_df, on="State")
f1_df['Sum'] = f1_df['Former smoker'] + f1_df['Never smoked']
f1_df = f1_df.drop('Former smoker', axis=1)
f1_df = f1_df.drop('Never smoked', axis=1)

r_df = pd.merge(f_df, f1_df, on="State")
r_df = r_df.rename(columns={'Sum_x': 'Smokers', 'Sum_y': 'Non-smokers'})
res = px.bar(r_df, x='State', y=['Smokers', 'Non-smokers'])
res.update_layout(xaxis_title='States', yaxis_title='values', title='Smokers and Non-smokers')
st.plotly_chart(res)

state_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
r_df['State'] = r_df['State'].map(state_dict)

fig = px.choropleth(r_df,
                    locations='State',
                    locationmode='USA-states',
                    color='Smokers',
                    scope="usa",
                    title='smokers per state')
st.plotly_chart(fig)
fig = px.choropleth(r_df,
                    locations='State',
                    locationmode='USA-states',
                    color='Non-smokers',
                    scope="usa",
                    title='Non-smokers per state')
st.plotly_chart(fig)