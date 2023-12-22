import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'])

# Set the title of the dashboard

app.title = "Automobile Sales Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# Create custom Plotly templates
plotly_template = {
    'layout': {
        'paper_bgcolor': 'black',
        'plot_bgcolor': 'black',
        'font': {
            'color': 'white'
        }
    }
}

# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', "color": "white", "font-size": 36}),
    html.Div([
        #TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:", style={'color': 'white'}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '100%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center', 'color': 'black'}
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder="Select Year",
            style={'width': '100%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center', 'color': 'black'}
        )
    ]),
    html.Div([ #TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ], style={'padding-top': '20px', 'justify-content': 'center'}),
], style={'background-color': 'black', 'color': 'white'})

# Define custom CSS styles
app.css.append_css({
    'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
})

#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Define the callback function to update the output container based on the selected statistics and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]


#TASK 2.5: Create and display graphs for Recession Report Statistics

        # Create charts for Recession Period Statistics
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation over Recession Period",
                template=plotly_template
            )
        )

        average_sales = recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Number of Vehicles Sold by Type',
                color="Vehicle_Type",
                template=plotly_template
            )
        )

        exp_rec = recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                names=exp_rec['Vehicle_Type'],
                values=exp_rec["Advertising_Expenditure"],
                title="Ads Expense per Vehicle",
                template=plotly_template
            )
        )

        emp_rec = recession_data.groupby(["Vehicle_Type", "unemployment_rate"])["Automobile_Sales"].sum().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                emp_rec,
                x=emp_rec['unemployment_rate'],
                y=emp_rec["Automobile_Sales"],
                color=emp_rec["Vehicle_Type"],
                title="Unemployment and Sales per Vehicle",
                template=plotly_template
            )
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]
    
 # TASK 2.6: Create and display graphs for Yearly Report Statistics
    elif selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Create charts for Yearly Report Statistics
        yas = data.groupby('Year')['Automobile_Sales'].sum().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x="Year", y='Automobile_Sales',
                                            title="Yearly Automobile Sales",
                                            template=plotly_template))

        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                                            title="Total Monthly Automobile Sales",
                                            template=plotly_template))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
                                           x="Vehicle_Type",
                                           y="Automobile_Sales",
                                           color="Vehicle_Type",
                                           title='Average Vehicles Sold by Vehicle Type in the year {}'.format(
                                               input_year),
                                           template=plotly_template))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data,
                                           values="Advertising_Expenditure",
                                           names="Vehicle_Type",
                                           title="Ads Expense per Vehicle Type",
                                           template=plotly_template))

        return [
            html.Div(className='chart-item', children=[html.Div(Y_chart1), html.Div(Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(Y_chart3), html.Div(Y_chart4)])
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
