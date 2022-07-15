# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit



import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Heart rate Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----

@st.cache
def get_data_from_csv():
    df = pd.read_csv(
        filepath_or_buffer="HeartRate.csv",low_memory=False)

    df["hour"] = pd.to_datetime(df["creationDate"],format="%Y-%m-%d %H:%M:%S").dt.hour
    df["year"] = pd.to_datetime(df["creationDate"], format="%Y-%m-%d %H:%M:%S").dt.year
    df["month"] = pd.to_datetime(df["creationDate"], format="%Y-%m-%d %H:%M:%S").dt.month
    df["day"] = pd.to_datetime(df["creationDate"], format="%Y-%m-%d %H:%M:%S").dt.day
    df['dateInt']=df['year'].astype(str) +" "+ df['month'].astype(str).str.zfill(2)+" "+ df['day'].astype(str).str.zfill(2)
    df['Date'] = pd.to_datetime(df['dateInt'], format='%Y %m %d')
    df["dotw"] = df["Date"].dt.weekday
    return df

df = get_data_from_csv()


print(df)

#st.dataframe(df)

st.sidebar.header("Please Filter Here:")
years = st.sidebar.multiselect(
    "Select the years:",
    options=df["year"].unique(),
    default=df["year"].unique()
)

df_selection = df.query(
    "year == @years"
)

st.sidebar.header("Please Filter Here:")
months = st.sidebar.multiselect(
    "Select the years:",
    options=df["month"].unique(),
    default=df["month"].unique()
)

df_selection = df.query(
    "month == @months"
)


st.sidebar.header("Please Filter Here:")
dayofweek = st.sidebar.multiselect(
    "Select the years:",
    options=df["dotw"].unique(),
    default=df["dotw"].unique()
)

df_selection = df.query(
    "dotw == @dayofweek"
)

st.dataframe(df_selection)


# ---- MAINPAGE ----
st.title(":bar_chart: Average ")
st.markdown("##")

# TOP KPI's
average_hr = (df_selection["value"].mean())
sd_hr = (df_selection["value"].std())

left_column,right_column= st.columns(2)

with left_column:
    st.subheader("Average HR:")
    st.subheader(f"{average_hr}")

with right_column:
    st.subheader("sd HR:")
    st.subheader(f"{sd_hr}")

st.markdown("""---""")

# SALES BY HOUR [BAR CHART]
heart_rate_by_weekday = df_selection.groupby(by=["dotw"]).sum()[["value"]]
heart_rate_dotw = px.bar(
    heart_rate_by_weekday ,
    x=heart_rate_by_weekday.index ,
    y="value",
    title="<b>heart_rate_by_version</b>",
    color_discrete_sequence=["#0083B8"] * len(heart_rate_by_weekday),
    template="plotly_white")

heart_rate_dotw.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(heart_rate_dotw, use_container_width=True)

# SALES BY HOUR [BAR CHART]
heart_rate_by_hour = df_selection.groupby(by=["hour"]).mean()[["value"]]
heart_rate_hour = px.bar(
    heart_rate_by_hour ,
    x=heart_rate_by_hour.index ,
    y="value",
    title="<b>heart_rate_by_hour</b>",
    color_discrete_sequence=["#0083B8"] * len(heart_rate_by_hour),
    template="plotly_white")

heart_rate_hour.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

right_column.plotly_chart(heart_rate_hour, use_container_width=True)
