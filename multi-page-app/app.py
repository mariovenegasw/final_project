import seaborn as sns
from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt


page1 = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("line_cta")),
    ui.nav_panel("Table", ui.output_data_frame("data_cta")),
    title="CTA Rides per Month 2018 - 2023")

page2 = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("line_divvy")),
    ui.nav_panel("Table", ui.output_data_frame("data_divvy")),
    title="Divvy Rides per Month 2020 - 2023")


app_ui = ui.page_navbar(
    ui.nav_spacer(), 
    ui.nav_panel("Page 1", page1),
    ui.nav_panel("Page 2", page2),
    title="Demand on Bus & Bike rides in Hydepark per month",
)


def server(input, output, session):
    # Page 1:
    @reactive.calc
    def cta_data():
        df_cta = pd.read_csv("cta_plot_seperate.csv")
        return df_cta
    
    @render.plot
    def line_cta():
        df = cta_data()
        
        fig = sns.lineplot(data=df, x='month', 
                           y='rides', hue='route', marker='o')

        plt.title('Rides per Month per Route 2018 - 2023')
        plt.xlabel('Month')
        plt.ylabel('Total Rides')
        plt.legend(title='Route')  
        '''
        # Filter the data for each route
        route_171 = df[df['route'] == '171']
        route_172 = df[df['route'] == '172']

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot each route separately
        plt.plot(route_171['month'], route_171['rides'], marker='o', label='Route 171', color='blue')
        plt.plot(route_172['month'], route_172['rides'], marker='s', label='Route 172', color='green')

        # Add labels, title, and legend
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Rides', fontsize=12)
        plt.title('Rides Per Date by Route', fontsize=14)
        plt.legend()

        plt.tight_layout()
        plt.show()
        '''
        return fig

    @render.data_frame
    def data_cta():
        df = pd.read_csv("cta_plot_seperate.csv")
        return df
    # Page 2:
    @reactive.calc
    def divvy_data():
        df_divvy = pd.read_csv("full_divvy.csv")
        return df_divvy
    
    @render.plot
    def line_divvy():
        df = divvy_data()
        fig = sns.lineplot(data = df, x = 'month', y = 'rides')
        plt.title('Monthly Rides 2020 - 2023')
        plt.xlabel('Month')
        plt.ylabel('Number of Rides')
        
        return fig

    @render.data_frame
    def data_divvy():
        df = pd.read_csv("full_divvy.csv")
        return df



app = App(app_ui, server)
