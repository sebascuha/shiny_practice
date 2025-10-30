from pathlib import Path

import pandas as pd
import calendar


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
    df =  pd.read_csv(infile)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    return df

# # Display DF in a card
# with ui.card():
#     # Card title
#     ui.card_header("Sample Sales Data")
#     # Rendering it as DF
#     @render.data_frame
#     def sample_data():
#         return dat().head(30)

# # Input asking
# ui.input_numeric("n", "Numeric input", 5, min = 2, max = 10) 
# @render_plotly
# def top_products():
#     df = dat().groupby("product")['quantity_ordered'].sum().\
#         nlargest(input.n()).reset_index()
#     return px.bar(df, x = "product", y = "quantity_ordered", 
#                   title = f"Top {input.n()} largest ordered products")

# # Input asking
# ui.input_selectize( "selectize",
#                    "Select an option below:",
#                    {"quantity_ordered": "Quantity Ordered",
#                     "price_each": "Price Each"} 
#                     )  
# # @render.text
# # def value():
# #     return f"{input.selectize()}"
# @render_plotly
# def histogram():
#     df = dat()
#     return px.histogram(df, x = input.selectize(), nbins = 10,
#                         title = f"Histogram of {input.selectize()}" )

# Input asking
ui.input_selectize( "selectize",
                    "Select an option below:",
                    {'All':'All',
                     'Atlanta (GA)':'Atlanta (GA)', 
                     'Austin (TX)': 'Austin (TX)', 
                     'Boston (MA)':'Boston (MA)',
                     'Dallas (TX)':'Dallas (TX)',
                     'Los Angeles (CA)':'Los Angeles (CA)',
                     'New York City (NY)':'New York City (NY)', 
                     'Portland (ME)':'Portland (ME)',
                     'Portland (OR)':'Portland (OR)',
                     'San Francisco (CA)':'San Francisco (CA)', 
                     'Seattle (WA)':'Seattle (WA)'},
                      multiple = True,
                      selected = 'All' )  

@render_plotly
def sales_over_time():
    # print(input.selectize())
    df = dat()
    sales = df.groupby(['city','month'])['quantity_ordered'].sum().reset_index()
    month_orders = calendar.month_name[1:]

    if input.selectize() in sales['city'].unique():
        sales = sales[sales['city'] == input.selectize()]
        
    print(list(sales['city'].unique()))
    # print(sales)
    
    fig = px.bar(sales, x = 'month', y = 'quantity_ordered',   
                  category_orders = {'month': month_orders},
                  color ='city',
                  title = f"Sales Over Time in {input.selectize()} region"
                  )
    return fig
    

 