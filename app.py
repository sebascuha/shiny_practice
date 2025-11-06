from pathlib import Path

import pandas as pd
import calendar


import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly

# Maing page parameters
ui.page_opts(title = "Demo", 
             fillable = False)

# UI mode
# ui.input_dark_mode() 

# Real csv data loading
@reactive.calc
def dat():
    infile = Path(__file__).parent / "sales/data/sales.csv"
    df =  pd.read_csv(infile)
    df['sale_value'] = df['quantity_ordered'] * df['price_each']
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    return df

with ui.card():  
    ui.card_header("Sales over the time")

    with ui.layout_sidebar():  
        with ui.sidebar(bg = "#f8f8f8", open = "open"):  
            # Input asking
            ui.input_selectize( "city",
                                "Select an option below:",
                                ['Atlanta (GA)', 'Austin (TX)', 
                                 'Boston (MA)', 'Dallas (TX)', 
                                'Los Angeles (CA)','New York City (NY)',
                                'Portland (ME)','Portland (OR)', 
                                'San Francisco (CA)', 'Seattle (WA)'],
                                multiple = True,
                                selected = 'Atlanta (GA)' )    

        # Plot 1: Sales over time
        @render_plotly
        def sales_over_time():
            df = dat()
            sales = df.groupby(['city','month'])['quantity_ordered'].sum().reset_index()
            # print(sales)
            month_orders = calendar.month_name[1:]
            # print(list(input.city()))   
            sales_by_city = sales[sales['city'].isin(input.city())]   
            # print(list(sales_by_city['city'].unique()))
            # print(sales_by_city)
            fig = px.bar(sales_by_city, 
                        x = 'month', 
                        y = 'quantity_ordered',   
                        category_orders = {'month': month_orders},
                        color ='city',
                        title = f"Sales Over Time -- {input.city()}"
                        )
            return fig 


from shiny.express import ui

with ui.navset_pill(id = "tab"): 
     
    with ui.nav_panel("Top Sellers (Q)"):
        with ui.layout_columns(col_widths = [6,6]):
            with ui.card():
                # Input asking
                ui.input_numeric("n1", "Numeric input", 5, min = 2, max = 10) 
                # Plot 2: top products
                @render_plotly
                def top_products_quant():
                    df = dat().groupby("product")['quantity_ordered'].sum().\
                        nlargest(input.n1()).reset_index()
                    return px.bar(df, x = "product", y = "quantity_ordered", 
                                title = f"Top {input.n1()} largest ordered products")
            with ui.card():
                # Input asking
                ui.input_slider("bin1", "Number of bins:",
                                 min = 5, max = 10, value = 10)
              
                # Plot 3: Histogram
                @render_plotly
                def histogram_quant():
                    df = dat()
                    return px.histogram(df, x = "quantity_ordered", nbins = input.bin1(),
                                        title = f"Histogram of quantity ordereed" )

    with ui.nav_panel("Top Sellers ($)"):
        with ui.layout_columns(col_widths = [6,6]):
            with ui.card():
                # Input asking
                ui.input_numeric("n2", "Numeric input", 5, min = 2, max = 10) 
                # Plot 2: top products
                @render_plotly
                def top_products_val():
                    df = dat().groupby("product")['sale_value'].sum().\
                        nlargest(input.n2()).reset_index()
                    return px.bar(df, x = "product", y = "sale_value", 
                                title = f"Top {input.n2()} sellers products")
            with ui.card():
                ui.input_slider("bin2", "Number of bins:",
                                 min = 5, max = 10, value = 10)
                @render_plotly
                def histogram_val():
                    df = dat()
                    return px.histogram(df, x = "sale_value", nbins = input.bin2(),
                                        title = f"Histogram of sales value ($)" )

    with ui.nav_panel("C"):
        "Panel C content"

    with ui.nav_panel("D"):
        "Page D content"

# Display DF in a card
with ui.card():
    # Card title
    ui.card_header("Sample Sales Data")
    # Rendering it as DF
    @render.data_frame
    def sample_data():
        return dat().head(30)

    

    
    

 