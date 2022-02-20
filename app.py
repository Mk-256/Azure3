import pandas as pd
import plotly_express as px
import plotly.figure_factory as ff
import streamlit as st

st.set_page_config(page_title='Mks Things',
                   page_icon=':art:',
                   layout='wide')

df = pd.read_excel(io='datas.xlsx')

#st.dataframe(df)
  #--Nav bar

st.sidebar.header('Customise Here..')
team = st.sidebar.multiselect(
    "Select Team",
    options=df['Team_Name'].unique(),
    default=df['Team_Name'].unique()
)

pcode = st.sidebar.multiselect(
    "Select Project Code",
    options=df['ProjectCode'].unique(),
    default=df['ProjectCode'].head()
)

pname = st.sidebar.multiselect(
    "Select Project Name",
    options=df['Y21_Project_Name'].unique(),
    default=df['Y21_Project_Name'].head()
)

group = st.sidebar.multiselect(
    "Select Group Name",
    options=df['Group_Name'].unique(),
    default=df['Group_Name'].unique()
)

part = st.sidebar.multiselect(
    "Select Part Name",
    options=df['Part_Name'].unique(),
    default=df['Part_Name'].head()
)

sqa = st.sidebar.multiselect(
    "Select SQA",
    options=df['SQA'].unique(),
    default=df['SQA'].unique()
)


df_selection = df.query(
    "  Team_Name == @team & Group_Name ==  @group  & SQA == @sqa   "
)


#--Mainn

st.title(':speedboat: KPI Samsung Dashboard')
st.markdown('##')

#KPI

total_time = int(df_selection["Total_time_Taken"].sum())
avg_day =  round(df_selection["PLM_KPI_1"].mean(), 2)
clock_rating = int(round(avg_day, 0))
avg_time = round(df_selection["Total_time_Taken"].mean(), 2)
defects = int(df_selection["No_of_Defects"].sum())
avg_defects = round(df_selection["No_of_Defects"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Total Time :')
    st.subheader(f"{total_time} s")
with middle_column:
    st.subheader('Average Number of Days')
    st.subheader(f":hourglass: {clock_rating}")
with right_column:
    st.subheader('Average Time :')
    st.subheader(f":watch:{avg_time}")
lh , rh,shh =st.columns(3)
with lh:
    st.subheader('Total Defects :')
    st.subheader(f'{defects}')
with rh:
    st.subheader('Average Defects :')
    st.subheader(f'{avg_defects}')
st.markdown("---")


# sales by bar chart

time_by_group = (
    df_selection.groupby(by=["Group_Name"]).sum()[["Total_time_Taken"]]
)
fig_group_time = px.bar(
    time_by_group,
    x="Total_time_Taken",
    y=time_by_group.index,
    orientation="h",
    title="<b>Time taken for a Group</b>",
    color_discrete_sequence=["#FF6103"] * len(time_by_group),
    template="plotly_white",
)

fig_group_time.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#one more bar

team_by_defects = (
    df_selection.groupby(by=["Team_Name"]).sum()[["No_of_Defects"]]
)
fig_team_defect = px.area(
    team_by_defects,
    x="No_of_Defects",
    y=team_by_defects.index,
    orientation="h",
    title="<b>Defects by a Team</b>",
    color_discrete_sequence=["#7FFF00"] * len(team_by_defects),

)
##third


team_by_sqa = (
    df_selection.groupby(by=["SQA"]).sum()[["No_of_Defects"]]
)
fig_team_sqa = px.line(
    team_by_sqa,
    x="No_of_Defects",
    y=team_by_sqa.index,
    orientation="h",
    title="<b>Defects by SQA</b>",
    color_discrete_sequence=["#00C78C"] * len(team_by_sqa),

)
fig_team_sqa.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)





#fourth
figgg = px.pie(df, values='Total_time_Taken', names='Part_Name', title='<b>Time taken for a Group</b>')
#st.plotly_chart(figgg)

#fifth


fig_scatter = px.scatter(df_selection, x="PLM_KPI_1", y="Total_time_Taken",title='<b>PLM for Individual</b>')
#st.plotly_chart(fig_scatter)

#sixt

fig_vio = px.violin(df_selection, y="Part_Name", x="Group_Name", color="SQA", box=True, points="all",
          hover_data=df.columns,title='<b>Parts Vs Groups Vs SQA</b>')
#st.plotly_chart(fig_vio)

#combo

left_column, middle, right_column= st.columns(3)
left_column.plotly_chart(fig_team_sqa, use_container_width=True)
middle.plotly_chart(figgg, use_container_width=True)
right_column.plotly_chart(fig_vio, use_container_width=True)

left, mid, right= st.columns(3)
left.plotly_chart(fig_group_time, use_container_width=True)
mid.plotly_chart(fig_scatter, use_container_width=True)
right.plotly_chart(fig_team_defect, use_container_width=True)



#sevent
fig_sun = px.sunburst(df_selection, path=['ProjectCode', 'Group_Name', 'Part_Name'], values='No_of_Defects',title='<b>SunBurst of ProjectCodes</b>')
#st.plotly_chart(fig_sun)

#eight
fig_bar = px.scatter_polar(df_selection, r="Team_Name", theta="Part_Name",
                       color="Group_Name", symbol="ProjectCode", size="Total_time_Taken",
                       color_discrete_sequence=px.colors.sequential.Plasma_r,template="plotly_dark",title='<b>Polar Among Group,Project,Time</b>')
#st.plotly_chart(fig_bar)
#nine
fig_funnel = px.funnel(df_selection, x='Part_Name', y='No_of_Defects',title='<b>Part vs Total Defects</b>')
#st.plotly_chart(fig_funnel)

#Combo

l, m, r= st.columns(3)
l.plotly_chart(fig_sun, use_container_width=True)
m.plotly_chart(fig_bar, use_container_width=True)
r.plotly_chart(fig_funnel, use_container_width=True)

#hide st
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
