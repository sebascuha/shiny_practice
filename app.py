from pathlib import Path

import pandas as pd

import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly

# UI mode
# ui.input_dark_mode() 

# Real csv data
@reactive.calc
def dat():
    infile = Path(__file__).parent / "shiny-python-projects/sales/data/sales.csv"
    return pd.read_csv(infile)

ui.input_numeric("n", "Numeric input", 5, min = 2, max = 10) 

ui.page_opts(title = "Demo", fillable=True)
with ui.layout_columns():

    # @render.data_frame
    # def data():
    #     return dat()

    @render_plotly
    def plot1():
        df = dat().groupby("product")['quantity_ordered'].sum().\
            nlargest(input.n()).reset_index()
        return px.bar(df, x = "product", y = "quantity_ordered",
                      title = f"Top {input.n()} largest ordered products")

    # @render_plotly
    # def plot2():
    #     return px.histogram(px.data.tips(), y="total_bill")
    

 