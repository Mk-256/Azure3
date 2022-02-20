import dash
import plotly.express as px

import pandas as pd
df = pd.read_csv('data.csv')

fig_pie = px.pie(data_frame=df, names='Team Name', values='No of Defects')
fig_pie.show()
print('\n')
ok=px.bar(data_frame=df, x='No of Defects', y='No of Defects')
ok.show()