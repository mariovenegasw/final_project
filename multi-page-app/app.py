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
    title="Divvy Rides per Month 2017 - 2023")


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

        return fig

    @render.data_frame
    def data_cta():
        df = pd.read_csv("cta_plot_seperate.csv")
        return df
    # Page 2:
    @reactive.calc
    def divvy_data():
        df_divvy = pd.read_csv("rides_per_month.csv")
        return df_divvy
    
    @render.plot
    def line_divvy():
        df = divvy_data()
        fig = sns.lineplot(data = df, x = 'month', y = 'count')
        plt.title('Monthly Rides 2017 - 2023')
        plt.xlabel('Month')
        plt.ylabel('Number of Rides')
        
        return fig

    @render.data_frame
    def data_divvy():
        df = pd.read_csv("rides_per_month.csv")
        return df



app = App(app_ui, server)
