import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotly import express as px
import warnings

warnings.simplefilter('ignore')

df = pd.read_csv("tobacco.csv")

st.title("Tobacco Use 1995-2010")
st.header("This dashboard will present the information tobaco users, which were made between 1995 and 2010")

st.write("Let's display my dataset")
st.dataframe(df)
st.subheader("Description")
st.text("Year - year \nState - the name of the state \nSmoke every day - the number of people who smoke every day in  (%)\nSmoke some day - the number of people who smoke some day (%)\nFormer smoker - the number of people who quit smoking (%)\nNever smoked - the number of people who never smoked(%)\nLocation - the exact location of the interviewed person")
df['Smoke everyday'] = df['Smoke everyday'].str.rstrip('%').astype(float)
df['Smoke some days'] = df['Smoke some days'].str.rstrip('%').astype(float)
df['Former smoker'] = df['Former smoker'].str.rstrip('%').astype(float)
df['Never smoked'] = df['Never smoked'].str.rstrip('%').astype(float)
st.subheader("Let's delete % sign in df")
st.dataframe(df)

st.title("Descriptive statistics")
st.write("Let's display some statistics, which includes mean, median, standard deviation and some other information about numerical fields")
st.write(df.describe(include='all'))
st.write("State:")
st.write(df['State'].describe())
st.write("Every day smokers:")
st.write(df['Smoke everyday'].describe())
st.write("median")
st.write(df['Smoke everyday'].median())
st.write("Smoke some days:")
st.write(df['Smoke some days'].describe())
st.write("median")
st.write(df['Smoke some days'].median())
st.write("Smoke some days:")
st.write(df['Former smoker'].describe())
st.write("median")
st.write(df['Former smoker'].median())
st.title("Data cleanup")
st.subheader("Check for any NaN values:")
st.write(df.isnull().sum().sum())
st.subheader("Now delete all of them")
st.write(df = df.dropna())
df = df.dropna()
st.title("Plots")
st.subheader("Number of the every day smoker through the years")
new_df = df.groupby('Year')['Smoke everyday'].mean().reset_index()

plt.plot(
    new_df['Year'],
    new_df['Smoke everyday']
)
st.pyplot(plt)
plt.clf()
st.write("correlation")
st.write(df['Year'].corr(df['Smoke everyday']))
st.write("This plot shows how the number of every day smokers slowly decreased by 7% throgh the years. ")

st.subheader("Former smokers")
new_df = df.groupby('Year')['Former smoker'].mean().reset_index()
plt.scatter(
    "Year",
    "Former smoker",
    data=new_df,
)
st.pyplot(plt)
plt.clf()
st.write("correlation")
st.write(df['Year'].corr(df['Former smoker']))
st.write("This graph proves previous statement. We can see that the number of former slowly increasing throgh the yesrs.")


st.subheader("Non-smokers average")
plt.hist(df["Never smoked"], bins=20)
plt.title("Non-smokers")
plt.xlabel("Percent")
plt.ylabel("Count")
st.pyplot(plt)
plt.clf()
st.write("This graph shows that more than a half is not smoking. This graph combines statistics on *Former smoker* and *Never smoked*")

st.subheader("Detailed overview. Is the number of smokers is decreasing?")
st.write("As we could notice from the first and second graphs, the number of *Former smoker* was incresing and the number of *Smoke everyday* is decresing.\n Let's make two groups which contains people who is not smoking and who is smoking.")
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
st.write("The graphs shows that difference between this two groups is slowly incresing, which means that people quit smoking.")

st.subheader("Detailed overview. Which region of USA smokes more?")
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
st.write("As can be seen from the map, the majority of smokers is from Kentuky and also the least number of smokers is in Utha.")

st.subheader("Data transformation.")
st.write("Let's add two new collums of *Smokers* and *Non-smokers* to our databse. This each of this collum will contain the sum of two other collum from our database.")
df['Smokers'] = df['Smoke everyday'] + df['Smoke some days']
df['Non-smokers'] = df['Former smoker'] + df['Never smoked']
st.write(df)
