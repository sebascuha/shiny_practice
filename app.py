# =========================================================
# Imports

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
import folium
from folium.plugins import HeatMap

# Shiny framework
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly

# =========================================================
# Page parameters

ui.tags.style(
    """
    .header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem 0;
        }
    .header-text {
        text-align: center;
        width: 100%;
        }
    .header-text h2 {
        margin: 0;
        color: #ffffff; /* optional: adjust to your theme */
        }

    body {
        background-color: #2170B5 /* optional: adjust to your theme */
        }
        
    """
    )


ui.page_opts(window_title = "Sales (Mock) Dashboard", fillable = False)

# Color scheme
colors = list(px.colors.sequential.Blues)[::-1]
color_basis = "#2170B5" # https://htmlcolorcodes.com/
px.defaults.template = "simple_white"

# =========================================================
# Dashboars layout and components


# Page title

with ui.div(class_ = "header-container"):
    with ui.div(class_ = "header-text"):
        ui.h2("Sales Dashboard")

# with ui.div(class_ = "header-container"):
#     ui.h2("Sales Dashboard", style = "text-align:center; margin:0; width:100%; padding:1rem 0; color: #ffffff;")


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
            sales = df.groupby(['city','month'])['quantity_ordered'].\
                sum().reset_index()
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
                        color_discrete_sequence = colors[2::],
                        title = f"Sales Over Time -- {input.city()}",

                        )
            fig.update_layout(xaxis_title = "Month",
                              yaxis_title = "Quantity Ordered")

            return fig 
with ui.card():
    with ui.layout_column_wrap(columns = 1/2):
        with ui.navset_pill(id = "tab",
                            header = ui.input_numeric("n", "Number of products",
                                            5, min = 2, max = 10)): 
            
            with ui.nav_panel("Top Sellers (Q)"):
                with ui.card():
                    # Plot 2.1: top products
                    @render_plotly
                    def top_products_quant():
                        df = dat().groupby("product")['quantity_ordered'].sum().\
                            nlargest(input.n()).reset_index()
                        fig = px.bar(df, x = "product", y = "quantity_ordered", 
                                    title = f"Top {input.n()} largest ordered products")
                        fig.update_traces(marker_color = color_basis)
                        fig.update_layout(xaxis_title = "Product", 
                                          yaxis_title = "Quantity Ordered")

                        return fig

            with ui.nav_panel("Top Sellers ($)"):
                with ui.card():
                    # Plot 2.2: top products
                    @render_plotly
                    def top_products_val():
                        df = dat().groupby("product")['sale_value'].sum().\
                            nlargest(input.n()).reset_index()
                        fig = px.bar(df, x = "product", y = "sale_value", 
                                    title = f"Top {input.n()} sellers products")
                        fig.update_traces(marker_color = color_basis)
                        fig.update_layout(xaxis_title = "Product", 
                                          yaxis_title = "Sales Value($)")
                        return fig
                        
            with ui.nav_panel("Lowest Sellers (Q)"):
                with ui.card():
                    # Plot 2.3: top products
                    @render_plotly
                    def low_products_quant():
                        df = dat().groupby("product")['quantity_ordered'].sum().\
                            nsmallest(input.n()).reset_index()
                        fig = px.bar(df, x = "product", y = "quantity_ordered", 
                                    title = f"Lowesr {input.n()} sellers products")
                        fig.update_traces(marker_color = color_basis)
                        fig.update_layout(xaxis_title = "Product", 
                                          yaxis_title = "Quantity Ordered")
                        return fig
                        
                        
            with ui.nav_panel("Lowest Sellers ($)"):
                with ui.card():
                    # Plot 2.4: top products
                    @render_plotly
                    def low_products_val():
                        df = dat().groupby("product")['sale_value'].sum().\
                            nsmallest(input.n()).reset_index()
                        fig = px.bar(df, x = "product", y = "sale_value", 
                                    title = f"Lowest {input.n()} sellers products")
                        fig.update_traces(marker_color = color_basis)
                        fig.update_layout(xaxis_title = "Product", 
                                          yaxis_title = "Sales Value ($)")
                        return fig
        
        with ui.card():
            # Plot 3: Sales by time of day
            ui.card_header('Sales by Time of day')
            @render.plot
            def plot_sales_by_time():
                df = dat()
                sales_by_hour = df['hour'].value_counts().\
                    reindex(np.arange(0,24), fill_value = 0).sort_index()

                heatmap_data = sales_by_hour.values.reshape(24,1)
        
                fig = sns.heatmap(heatmap_data, 
                            cmap = "Blues", 
                            cbar = True,
                            xticklabels = ['Number of Sales'],
                            yticklabels = [f'{hour}:00' for hour in range(24)],
                            annot = True,
                            fmt = ',d',  # Use comma format for thousands and display as integers
                            annot_kws = {'size': 10}  # Adjust font size for better readability
                            )
                return fig

# Display DF in a card
with ui.card():
    # Card title
    ui.card_header("Sales Amount Location Heatmap")
    @render.ui
    def heatmap_folium():
        df = dat()
        # print(df.dtypes)
        headmap_df = df[['lat', 'long','quantity_ordered']]#.values
        # print(headmap_df)
        m = folium.Map(location = [headmap_df['lat'].mean(), 
                                   headmap_df['long'].mean()], 
                        zoom_start = 4.5)
        # Custom color gradient from lightest to darkest
        gradient = {
            0.0: '#E9F3FB',   # Lightest
            0.1: '#C3DDF4',
            0.2: '#9CC7ED',
            0.3: '#75B1E6',
            0.4: '#4E9BDF',
            0.5: '#2885D7',
            0.6: '#2170B5',
            0.7: '#19558A',
            0.8: '#123D63',
            0.9: '#0B253C',
            1.0: '#040D16'    # Darkest
        }
        HeatMap(data = headmap_df.values,
                gradient = gradient,
                min_opacity = 0.5,
                radius = 20,
                ).add_to(m)
        return m

# Display DF in a card
with ui.card():
    # Card title
    ui.card_header("Sample Sales Data")
    # Rendering it as DF
    @render.data_frame
    def sample_data():
        return render.DataGrid(dat().head(100), filters = True)
