import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from datetime import date

subprocess.call(['sh', './get_data.sh'])

df_pers = pd.read_csv('data/russia_losses_personnel.csv')
df_pers.drop(df_pers.columns[[1, 3]], inplace=True, axis=1)

df_eqp = pd.read_csv('data/russia_losses_equipment.csv')
df_eqp.drop(df_eqp.columns[[1]], inplace=True, axis=1)

fig = go.Figure()
today = date.today().strftime("%B %d, %Y")

for col_name in np.array(personnel.columns)[1:]:
    fig.add_trace(go.Scatter(x = personnel['date'], y = personnel[col_name], mode = 'lines+markers', 
                             name = col_name))

fig.update_layout(
    title="Russian Personnel Losses and Prisoners of War Taken as of " + str(today),
    xaxis_title="Date",
    yaxis_title="Soldiers",
    legend_title="Legend",
    font=dict(
        family='Avenir Black',
        size=16
    )
)

fig.show()
fig.write_image("personnel_losses_trace.png")




