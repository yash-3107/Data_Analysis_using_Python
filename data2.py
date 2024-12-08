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
os.chdir(currentDirectory)
# Plot: Filename vs Electrolyte Resistance (Re)
fig_re = px.line(newDF, x='filename', y='Re', 
                 title='Filename vs Electrolyte Resistance (Re)',
                 labels={'filename': 'Filename', 'Re': 'Electrolyte Resistance (Re)'},
                 line_shape='linear', markers=True)

# Plot: Filename vs Charge Transfer Resistance (Rct)
fig_rct = px.line(newDF, x='filename', y='Rct', 
                  title='Filename vs Charge Transfer Resistance (Rct)',
                  labels={'filename': 'Filename', 'Rct': 'Charge Transfer Resistance (Rct)'},
                  line_shape='linear', markers=True)

# Plot: Filename vs Battery Impedance
fig_impedance = px.line(newDF, x='filename', y='Battery_impedance', 
                        title='Filename vs Battery Impedance',
                        labels={'filename': 'Filename', 'Battery_impedance': 'Battery Impedance'},
                        line_shape='linear', markers=True)

# Saving the plots as HTML files
fig_re.write_html("fig_re.html")
fig_rct.write_html("fig_rct.html")
fig_impedance.write_html("fig_impedance.html")

# Initialize Dash app
app = dash.Dash(__name__)

# Layout to display all three plots
app.layout = html.Div(children=[
    html.H1("Multiple Plotly Graphs"),
    dcc.Graph(figure=fig_re),
    dcc.Graph(figure=fig_rct),
    dcc.Graph(figure=fig_impedance),
])

# Generate the app layout as HTML string
html_layout = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plotly Graphs</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Multiple Plotly Graphs</h1>
    <div id="graph_re">{graph_re_html}</div>
    <div id="graph_rct">{graph_rct_html}</div>
    <div id="graph_impedance">{graph_impedance_html}</div>
</body>
</html>
"""

with open("fig_re.html", "r", encoding="utf-8") as f:
    graph_re_html = f.read()

with open("fig_rct.html", "r", encoding="utf-8") as f:
    graph_rct_html = f.read()

with open("fig_impedance.html", "r", encoding="utf-8") as f:
    graph_impedance_html = f.read()

graph_re_html = graph_re_html.replace("{", "{{").replace("}", "}}")
graph_rct_html = graph_rct_html.replace("{", "{{").replace("}", "}}")
graph_impedance_html = graph_impedance_html.replace("{", "{{").replace("}", "}}")

# Combine them into the final HTML layout
final_html_content = html_layout.replace("{graph_re_html}", graph_re_html)\
                                .replace("{graph_rct_html}", graph_rct_html)\
                                .replace("{graph_impedance_html}", graph_impedance_html)

# Save to 'index.html'
with open("index.html", "w", encoding="utf-8") as file:
    file.write(final_html_content)

if __name__ == "__main__":
    app.run_server(debug=True)