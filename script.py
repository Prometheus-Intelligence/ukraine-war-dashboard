import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pprint
import requests
import json
from datetime import date
from newsapi import NewsApiClient
from wordcloud import WordCloud

subprocess.call(['sh', './shells/get_data.sh'])

df_pers = pd.read_csv('data/russia_losses_personnel.csv')
df_pers.drop(df_pers.columns[[1, 3]], inplace=True, axis=1)

df_eqp = pd.read_csv('data/russia_losses_equipment.csv')
df_eqp.drop(df_eqp.columns[[1]], inplace=True, axis=1)

pfig = go.Figure()
efig = go.Figure()
today = date.today().strftime("%B %d, %Y")

for col_name in np.array(df_pers.columns)[1:]:
    pfig.add_trace(go.Scatter(x = df_pers['date'], y = df_pers[col_name], mode = 'lines+markers', 
                             name = col_name))

for col_name in np.array(df_eqp.columns)[1:]:
    efig.add_trace(go.Scatter(x = df_eqp['date'], y = df_eqp[col_name], mode = 'lines+markers', 
                             name = col_name))

pfig.update_layout(
    title="Russian Personnel Losses and Prisoners of War Taken as of " + str(today),
    xaxis_title="Date",
    yaxis_title="Soldiers",
    legend_title="Legend",
    font=dict(
        family='Avenir Black',
        size=13
    )
)

efig.update_layout(
    title="Russian Equipment Losses as of " + str(today),
    xaxis_title="Date",
    yaxis_title="Amount",
    legend_title="Legend",
    font=dict(
        family='Avenir Black',
        size=16
    )
)

pfig.write_image("output/personnel_losses_trace.png")
efig.write_image("output/equipment_losses_trace.png")

df_eqp_sum = df_eqp.iloc[:, 1:].sum()
df_eqp_sum = df_eqp_sum.reset_index()
df_eqp_sum.columns = ['equip_item', 'amount']

sum_fig = px.pie(df_eqp_sum, values='amount', names='equip_item', 
    title='Equipment Losses as of ' + str(today))

sum_fig.update_layout(
font=dict(
        family='Avenir Black',
        size=16
    )
)

sum_fig.write_image("output/equipment_losses_pie.png")
subprocess.call(['sh', './shells/remove_data.sh'])

with open('secrets.json', 'r') as f:
    json_data = json.load(f)

API_key = json_data['API_Key']
url = 'https://newsapi.org/v2/everything?'
parameters = {
    'q': 'ukraine war',
    'pageSize': 20,
    'apiKey': API_key
}

response = requests.get(url, params=parameters)
response_json = response.json()

text_file = open("output/latest_headlines.txt", "w")
combined_headlines = ''

for article in response_json['articles']:
    text_file.write(article['title'] + "\n")
    combined_headlines += article['title'] + ' '

text_file.close()
wordcloud = WordCloud(max_font_size=40).generate(combined_headlines)

plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('output/ukraine_word_cloud.png', dpi=2000)
