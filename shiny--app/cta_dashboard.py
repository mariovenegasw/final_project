import seaborn as sns
from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_checkbox_group(
            "route",
            "Route",
            ["171", "172"],
            selected=["171", "172"],
        ),
        title="Filter controls",
    ),
    ui.layout_column_wrap(
        ui.value_box(
            "Month with maximum rides",
            ui.output_text("max_month"),
        ),
        ui.value_box(
            "Maximum rides",
            ui.output_text("max_rides"),
        ),
        ui.value_box(
            "Month wiht minimum rides",
            ui.output_text("min_month"),
        ),
        ui.value_box(
            "Minimum rides",
            ui.output_text("min_rides"),
        ),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("CTA Rides per Month"),
            ui.output_plot("line_cta"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("CTA Routes"),
            ui.output_data_frame("summary_statistics"),
            full_screen=True,
        )
    )
)


def server(input, output, session):
    # Page 1:
    @reactive.calc
    def filtered_df():
        df = pd.read_csv('cta_plot_seperate.csv')
        selected_routes = input.route.get()
        filt_df = df[df["route"].astype(str).isin(selected_routes)]
        return filt_df

    @render.text
    def max_month():
        df = filtered_df()
        if df.empty:
            return "Please select a route"
        max_rides_index = df['rides'].idxmax()
        max_rides_row = df.loc[max_rides_index]
        month = max_rides_row['month']
        return month
    
    @render.text
    def max_rides():
        df = filtered_df()
        if df.empty:
            return "Please select a route"
        max_rides_index = df['rides'].idxmax()
        max_rides_row = df.loc[max_rides_index]
        route = max_rides_row['rides']
        return route
    
    @render.text
    def min_month():
        df = filtered_df()
        if df.empty:
            return "Please select a route"
        min_rides_index = df['rides'].idxmin()
        min_rides_row = df.loc[min_rides_index]
        month = min_rides_row['month']
        return month
    
    @render.text
    def min_rides():
        df = filtered_df()
        if df.empty:
            return "Please select a route"
        min_rides_index = df['rides'].idxmin()
        min_rides_row = df.loc[min_rides_index]
        rides = min_rides_row['rides']
        return rides
    
    @render.plot
    def line_cta():
        df = filtered_df()
        
        fig = sns.lineplot(data=df, x='month', 
                           y='rides', hue='route', marker='o')

        plt.title('Rides per Month per Route 2018 - 2023')
        plt.xlabel('Month')
        plt.ylabel('Total Rides')
        plt.legend(title='Route')  

        return fig
    
    @render.data_frame
    def summary_statistics():
        df = filtered_df()
        return df


app = App(app_ui, server)
