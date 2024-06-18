from shiny import App, ui, reactive, render
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the UI for the app
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("file_input", "Choose CSV File"),
            ui.input_slider("year_range", "Select Year Range", min=1941, max=2023, value=(2005, 2015)),
            ui.input_select("station_id", "Select Station ID", choices=[]),
            ui.input_select("index_type", "Select Index", choices=['PRCPTOT', 'annual_temp'])
        ),
        ui.panel_main(
            ui.output_plot("trend_plot"),
            ui.output_plot("forecast_plot")
        )
    )
)

# Define server logic required to draw plots
def server(input, output, session):
    data = reactive.Value(None)  # Use reactive.Value to handle reactive state

    @reactive.Effect
    def _():
        if input.file_input():
            data.set(pd.read_csv(input.file_mod()["tmp_name"]))
            station_ids = data.get()['station_id'].unique()
            session.update_select(input_id="station_id", choices=station_ids)

    @output
    @render.plot
    def trend_plot():
        if data.get() is not None:
            # Filter data based on the UI inputs
            df_filtered = data.get()[(data.get()['year'] >= input.year_range()[0]) & 
                                     (data.get()['year'] <= input.year_range()[1])]
            # Generate plot based on filtered data
            plt.figure()
            sns.lineplot(data=df_filtered, x='year', y=input.index_type())
            plt.title('Trend Over Time')
            return plt.gcf()

    @output
    @render.plot
    def forecast_plot():
        # Example: plot a static forecast plot
        plt.figure()
        plt.plot([1, 2, 3], [4, 5, 6])  # This should be replaced with actual forecasting code
        plt.title('Forecast Plot')
        return plt.gcf()

app = App(app_ui, server)
