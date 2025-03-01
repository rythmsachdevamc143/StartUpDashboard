import streamlit as st 
import pandas as pd
import plotly.express as px

df = pd.read_csv("startup_cleaned.csv")
df['investors'] = df['investors'].fillna('Undisclosed')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

st.set_page_config(layout="wide", page_title="Startup Funding Analysis")


def load_overall_analysis():
    st.title("Overall Analysis")

    total = round(df['amount'].sum(),2)
    max_funding = round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0],2)
    mean_funding = round(df.groupby('startup')['amount'].sum().mean(),2)
    total_startups = df['startup'].nunique()
    # mom_investment_list = df.groupbuy(['month','year'])['startup'].count()
    col1,clo2,clo3,clo4 = st.columns(4)
   

    with col1:
        st.metric(label="Total Funding", value=f"₹{total} Cr.")
    with clo2:
        st.metric(label="Maximum Funding", value=f"₹{max_funding} Cr.")
    with clo3:
        st.metric(label="Average Funding", value=f"₹{mean_funding} Cr.")
    with clo4:
        st.metric(label="Total Startups", value=f"{total_startups}")
    
    st.header("Month on Month Analysis")
    temp_df = df.groupby(['month','year'])['amount'].sum().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    temp_df['startups'] = df.groupby(['month','year'])['startup'].count().values
    fig1 = px.line( x=temp_df['x_axis'], y=temp_df['amount'], title="Month on Month Funding Analysis", labels={'x':'Month-Year','y':'Amount in Crore Rs.'})
    st.plotly_chart(fig1)
    fig2 = px.line( x=temp_df['x_axis'], y=temp_df['startups'], title="Month on Month Startup Analysis", labels={'x':'Month-Year','y':'Number of Startups'})
    st.plotly_chart(fig2)


def load_investor_details(investor):
    investor_df = df[df['investors'].str.contains(investor)]
    # investor_df.head()[['date','startup','vertical','city','round','amount']]
    st.subheader("Most Recent Investments")
    st.dataframe(investor_df.head()[['date','startup','vertical','city','round','amount']])
    st.subheader("Biggest Investments")
    st.dataframe(investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False))
    big_series = investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False)
    vertical_series = investor_df.groupby('vertical')['amount'].sum()
    city_series = investor_df.groupby('city')['amount'].sum()
    # print(city_series)
    
    year_series = investor_df.groupby('year')['amount'].sum()
    total_investment = vertical_series.sum()

# Filter out values below 0.5% and sum them into 'Others'
    threshold = 0.005 * total_investment  # 0.5% of total investment
    above_threshold = vertical_series[vertical_series >= threshold]
    below_threshold = vertical_series[vertical_series < threshold]

# Add 'Others' category if needed
    if not below_threshold.empty:
       above_threshold['Others'] = below_threshold.sum()

# Create pie chart
    fig2 = px.pie(
        values=above_threshold.values, 
        names=above_threshold.index, 
        title="Investments by Vertical"
      )
    fig = px.bar(x=big_series.index, y=big_series.values, 
             title="Biggest Investments", 
             labels={'x': 'Startup', 'y': 'Amount in Crore Rs.'})
    fig3 = px.pie(values=city_series.values, names=city_series.index, 
             title="Investments by City")
    fig4 = px.line(x=year_series.index, y=year_series.values, 
             title="Investments by Year", 
             labels={'x': 'Year', 'y': 'Amount in Crore Rs.'})
    st.plotly_chart(fig)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)   

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One", ["Overall Analysis","Investor Analysis"])

if option == "Overall Analysis":
    load_overall_analysis()
else:
    selected_investor = st.sidebar.selectbox("Select One", sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        st.title(selected_investor)
        load_investor_details(selected_investor)


