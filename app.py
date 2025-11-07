# =========================================================
# Directory handling
from pathlib import Path

# Handle data
import pandas as pd
import numpy as np
import calendar

# Visualization frameworks
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Shiny framework
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly

# =========================================================
# Maing page parameters

ui.page_opts(title = "Demo", 
             fillable = False)
# =========================================================
# Dashboars layout and components

# Real csv data loading
@reactive.calc
def dat():
    infile = Path(__file__).parent / "sales/data/sales.csv"
    df =  pd.read_csv(infile)
    df['sale_value'] = df['quantity_ordered'] * df['price_each']
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    df['hour'] = df['order_date'].dt.hour
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
                        color ='Blues',
                        title = f"Sales Over Time -- {input.city()}"
                        )
            return fig 

with ui.layout_column_wrap(columns = 1/2):
    with ui.navset_pill(id = "tab",
                        footer = ui.\
                            input_numeric("n", "Number of products",
                                          5, min = 2, max = 10)): 
        
        with ui.nav_panel("Top Sellers (Q)"):
            with ui.card():
                # Plot 2.1: top products
                @render_plotly
                def top_products_quant():
                    df = dat().groupby("product")['quantity_ordered'].sum().\
                        nlargest(input.n()).reset_index()
                    return px.bar(df, x = "product", y = "quantity_ordered", 
                                title = f"Top {input.n()} largest ordered products")

        with ui.nav_panel("Top Sellers ($)"):
            with ui.card():
                # Plot 2.2: top products
                @render_plotly
                def top_products_val():
                    df = dat().groupby("product")['sale_value'].sum().\
                        nlargest(input.n()).reset_index()
                    return px.bar(df, x = "product", y = "sale_value", 
                                title = f"Top {input.n()} sellers products")
                    
        with ui.nav_panel("Lowest Sellers (Q)"):
            with ui.card():
                # Plot 2.3: top products
                @render_plotly
                def low_products_quant():
                    df = dat().groupby("product")['quantity_ordered'].sum().\
                        nsmallest(input.n()).reset_index()
                    return px.bar(df, x = "product", y = "quantity_ordered", 
                                title = f"Lowesr {input.n()} sellers products")
                    
        with ui.nav_panel("Lowest Sellers ($)"):
            with ui.card():
                # Plot 2.4: top products
                @render_plotly
                def low_products_val():
                    df = dat().groupby("product")['sale_value'].sum().\
                        nsmallest(input.n()).reset_index()
                    return px.bar(df, x = "product", y = "sale_value", 
                                title = f"Lowest {input.n()} sellers products")
    
    with ui.card():
        # Plot 3: Sales by time of day
        ui.card_header('Sales by Time of day')
        @render.plot
        def plot_sales_by_time():
            df = dat()
            sales_by_hour = df['hour'].value_counts().\
                reindex(np.arange(0,24), fill_value = 0).sort_index()
            print(sales_by_hour)

            heatmap_data = sales_by_hour.values.reshape(24,1)
            print(heatmap_data)
            fig = sns.heatmap( heatmap_data, 
                        cmap = "Blues", 
                        cbar = True,
                        xticklabels = ['Sales'],
                        yticklabels = [f'{hour}:00' for hour in range(24)],
                        annot = True
                        )
            plt.ticklabel_format
            return fig

            

# # Display DF in a card
# with ui.card():
#     # Card title
#     ui.card_header("Sample Sales Data")
#     # Rendering it as DF
#     @render.data_frame
#     def sample_data():
#         return dat().head(30)

    

    
    

 