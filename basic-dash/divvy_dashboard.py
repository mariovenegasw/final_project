import seaborn as sns
from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt


app_ui = ui.page_sidebar(
            ui.sidebar(),
            ui.layout_column_wrap(
                ui.value_box("Month with maximum rides", ui.output_text("max_month_divvy")),
                ui.value_box("Maximum rides", ui.output_text("max_rides_divvy")),
                ui.value_box("Month with minimum rides", ui.output_text("min_month_divvy")),
                ui.value_box("Minimum rides", ui.output_text("min_rides_divvy")),
                fill=False,
            ),
            ui.layout_columns(
                ui.card(ui.card_header("Divvy rides per month"), ui.output_plot("line_divvy"), full_screen=True),
                ui.card(ui.card_header("Divvy rides"), ui.output_data_frame("divvy_df"), full_screen=True),
            ),
        )


def server(input, output, session):
    
    @reactive.calc
    def divvy_data():
        df = pd.read_csv('full_divvy.csv')
        return df
    
    @render.text
    def max_month_divvy():
        df = divvy_data()
        max_rides_index = df['rides'].idxmax()
        max_rides_row = df.loc[max_rides_index]
        month = max_rides_row['month']
        return month
    
    @render.text
    def max_rides_divvy():
        df = divvy_data()
        max_rides_index = df['rides'].idxmax()
        max_rides_row = df.loc[max_rides_index]
        route = max_rides_row['rides']
        return route
    
    @render.text
    def min_month_divvy():
        df = divvy_data()
        min_rides_index = df['rides'].idxmin()
        min_rides_row = df.loc[min_rides_index]
        month = min_rides_row['month']
        return month
    
    @render.text
    def min_rides_divvy():
        df = divvy_data()
        min_rides_index = df['rides'].idxmin()
        min_rides_row = df.loc[min_rides_index]
        rides = min_rides_row['rides']
        return rides
    
    @render.plot
    def line_divvy():
        df = divvy_data()
        fig = sns.lineplot(data = df, x = 'month', y = 'rides')
        plt.title('Monthly Rides 2020 - 2023')
        plt.xlabel('Month')
        plt.ylabel('Number of Rides')
        
        return fig

    
    @render.data_frame
    def divvy_df():
        df = divvy_data()
        return df

app = App(app_ui, server)
