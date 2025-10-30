from pathlib import Path

import pandas as pd

import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly

# Maing page parameters
ui.page_opts(title = "Demo", fillable = True)
# UI mode
# ui.input_dark_mode() 

# Real csv data loading
@reactive.calc
def dat():
    infile = Path(__file__).parent / "sales/data/sales.csv"
    return pd.read_csv(infile)

# Display DF in a card
with ui.card():
    # Card title
    ui.card_header("Sample Sales Data")
    # Rendering it as DF
    @render.data_frame
    def sample_data():
        return dat().head(30)

# Input asking
ui.input_numeric("n", "Numeric input", 5, min = 2, max = 10) 

@render_plotly
def top_products():
    df = dat().groupby("product")['quantity_ordered'].sum().\
        nlargest(input.n()).reset_index()
    return px.bar(df, x = "product", y = "quantity_ordered", 
                  title = f"Top {input.n()} largest ordered products")

# Input asking
ui.input_selectize( "selectize",
                   "Select an option below:",
                   {"quantity_ordered": "Quantity Ordered",
                    "price_each": "Price Each"} 
                    )  
# @render.text
# def value():
#     return f"{input.selectize()}"
@render_plotly
def plot2():
    df = dat()
    return px.histogram(df, x = input.selectize(), nbins = 10,
                        title = f"Histogram of {input.selectize()}" )
    

 