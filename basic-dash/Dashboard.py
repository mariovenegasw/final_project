from shiny import App, ui, reactive, render
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page 1: CTA Dashboard
page1 = ui.navset_card_underline(
    ui.nav_panel(
        "Plot",
        ui.input_checkbox_group(
            "route", "Select Route", choices=["171", "172"], selected=["171", "172"]
        ),
        ui.output_plot("line_cta"),
    ),
    ui.nav_panel("Table", ui.output_data_frame("data_cta")),
    title="CTA Rides per Month 2018 - 2023",
)

# Page 2: Divvy Dashboard
page2 = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("line_divvy")),
    ui.nav_panel("Table", ui.output_data_frame("data_divvy")),
    title="Divvy Rides per Month 2017 - 2023",
)

# Combine Pages with Value Boxes
app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_panel(
        "Page 1",
        ui.layout_column_wrap(
            ui.value_box("Month with Maximum Rides", ui.output_text("max_month_cta")),
            ui.value_box("Maximum Rides", ui.output_text("max_rides_cta")),
            ui.value_box("Month with Minimum Rides", ui.output_text("min_month_cta")),
            ui.value_box("Minimum Rides", ui.output_text("min_rides_cta")),
            fill=False,
        ),
        page1,
    ),
    ui.nav_panel(
        "Page 2",
        ui.layout_column_wrap(
            ui.value_box("Month with Maximum Rides", ui.output_text("max_month_divvy")),
            ui.value_box("Maximum Rides", ui.output_text("max_rides_divvy")),
            ui.value_box("Month with Minimum Rides", ui.output_text("min_month_divvy")),
            ui.value_box("Minimum Rides", ui.output_text("min_rides_divvy")),
            fill=False,
        ),
        page2,
    ),
    title="Demand on Bus & Bike Rides in Hydepark per Month",
)


def server(input, output, session):
    # CTA 
    @reactive.calc
    def filtered_df():
        df = pd.read_csv('cta_plot_seperate.csv')
        selected_routes = input.route.get()
        filt_df = df[df["route"].astype(str).isin(selected_routes)]
        return filt_df

    @render.text
    def max_month_cta():
        df = filtered_df()
        if df.empty:
            return "Please select a route"
        max_rides_index = df['rides'].idxmax()
        max_rides_row = df.loc[max_rides_index]
        month = max_rides_row['month']
        return month
    
    @render.text
    def max_rides_cta():
        df = filtered_df()
        if df.empty:
            return "Please select a route"
        max_rides_index = df['rides'].idxmax()
        max_rides_row = df.loc[max_rides_index]
        route = max_rides_row['rides']
        return route
    
    @render.text
    def min_month_cta():
        df = filtered_df()
        if df.empty:
            return "Please select a route"
        min_rides_index = df['rides'].idxmin()
        min_rides_row = df.loc[min_rides_index]
        month = min_rides_row['month']
        return month
    
    @render.text
    def min_rides_cta():
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
    def data_cta():
        df = pd.read_csv("cta_plot_seperate.csv")
        return df
    
    # Divvy 
    @reactive.calc
    def divvy_data():
        df = pd.read_csv('rides_per_month.csv')  
        return df

    @render.text
    def max_month_divvy():
        df = divvy_data()
        max_rides_index = df['count'].idxmax()
        return df.loc[max_rides_index]['month']

    @render.text
    def max_rides_divvy():
        df = divvy_data()
        return df['count'].max()

    @render.text
    def min_month_divvy():
        df = divvy_data()
        min_rides_index = df['count'].idxmin()
        return df.loc[min_rides_index]['month']

    @render.text
    def min_rides_divvy():
        df = divvy_data()
        return df['count'].min()

    @render.plot
    def line_divvy():
        df = divvy_data()
        sns.lineplot(data=df, x="month", y="count")
        plt.title("Divvy Monthly Rides")
        plt.xlabel("Month")
        plt.ylabel("Number of Rides")
        return plt.gcf()

    @render.data_frame
    def data_divvy():
        return divvy_data()


# Combine UI and server into the app
app = App(app_ui, server)
