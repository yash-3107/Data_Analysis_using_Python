# install all libraries that are essential
import os
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html

currentDirectory = os.getcwd()

#getting to loc where 7500+ files are stored
destination = os.path.join(currentDirectory,'data')
os.chdir(destination)

#making data frame for metadata too
metadata = pd.read_csv('../metadata.csv')
filesinDest = os.listdir('.')

#making new data frame to store all the values of metadata where type = 'impedance' #because only in those rows 'Re' and 'Rct' is present
newDF = pd.DataFrame({'filename':[],'Re':[],'Rct':[]})
for element in range(1,7565):
    if metadata.loc[element-1,'type'] == 'impedance':
        newDF.loc[len(newDF)] = [f'{metadata.loc[element-1,'filename']}',metadata.loc[element-1,'Re'],metadata.loc[element-1,'Rct']]
c = 0

#now it is time to actually find the files in data folder for which value of 'Re' and #'Rct' is given in metadata and ignoring other files
for file in filesinDest:
    fileDF = pd.read_csv(file)
    if file == newDF.loc[c,'filename']:
        fileDF['Battery_impedance'] = fileDF['Battery_impedance'].apply(lambda x: complex(x))
        average = fileDF['Battery_impedance'].apply(np.abs).mean()
        newDF.loc[c,'Battery_impedance'] = average
        c+=1
    if c == len(newDF):
        break

#FINALLY MAGIC HAPPENSE 

# Plot: Filename vs Electrolyte Resistance (Re)
fig_re = px.line(newDF, x='filename', y='Re', 
                 title='Filename vs Electrolyte Resistance (Re)',
                 labels={'filename': 'Filename', 'Re': 'Electrolyte Resistance (Re)'},
                 line_shape='linear', markers=True)
fig_re.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig_re.show()

# Plot: Filename vs Charge Transfer Resistance (Rct)
fig_rct = px.line(newDF, x='filename', y='Rct', 
                  title='Filename vs Charge Transfer Resistance (Rct)',
                  labels={'filename': 'Filename', 'Rct': 'Charge Transfer Resistance (Rct)'},
                  line_shape='linear', markers=True)
fig_rct.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig_rct.show()

# Plot: Filename vs Battery Impedance
fig_impedance = px.line(newDF, x='filename', y='Battery_impedance', 
                        title='Filename vs Battery Impedance',
                        labels={'filename': 'Filename', 'Battery_impedance': 'Battery Impedance'},
                        line_shape='linear', markers=True)
fig_impedance.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig_impedance.show()
os.chdir(currentDirectory)

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Multiple Plotly Graphs"),
    dcc.Graph(figure=fig_re),
    dcc.Graph(figure=fig_rct),
    dcc.Graph(figure=fig_impedance),
])
    
if __name__ == "__main__":
    app.run_server(debug=True)


