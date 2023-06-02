import streamlit as st
#import pandas as pd
from streamlit_folium import folium_static
import folium
import altair as alt
import geopandas as gpd
from PIL import Image
import branca.colormap as cm
import json
from PIL import Image, ImageOps, ImageDraw
# import boto3


# Set page configuration
st.set_page_config(
    page_title="Fiber Competitive Intensity",
    page_icon=":earth_asia:",
    layout="wide",
    initial_sidebar_state="auto",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

# Add title to app
st.markdown(
    f"""
    <div style="style="position: relative; top: 0px; left: 1000px;;">
        <h1 style='font-size: 36px;'>Fiber Competitive Intensity</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Create sidebar menu
menu = ["Home", "About", "Contact Us"]
selection = st.sidebar.radio("Go to", menu)

    # Add submenu to Home menu
if selection == "Home":
    Home_menu = ["Map", "Graph"]
    sub_selection = st.sidebar.radio("Select an option", Home_menu)

    # Add content to Map
    if sub_selection == "Map":
        st.markdown(
            f"""
            <div style="overflow-y: scroll; top: 1; right: 10;">            
                <h1 style='font-size: 20px;'>Current Uptake Rate</h1>
                <p style='font-size: 16px;'>Map showing the current uptake rate of fiber in Malaysia</p>
            </div>
            """,
    unsafe_allow_html=True,
)
               
        # Read GeoJSON file
        gdf = gpd.read_file('../src/data/dun.simulated_uptake_rate.geojson')

        # Create map centered on GeoJSON data
        center_lat = gdf.centroid.y.mean()
        center_lon = gdf.centroid.x.mean()
        
        # Create a color gradient using linear colormap
        colormap = cm.linear.YlOrRd_09.scale(0, 1800) 
        
        # Load the data GeoJSON fiber data
        def style_function(feature):
            data_value = feature['properties']['fiber_tests']
            return {'fillColor': colormap(data_value)}

        def highlight_boundary(feature):
            return {
                'fillColor': '#98abc5',
                'fillOpacity': 0.5,
                'color': '#000000',
                'weight': 0.01
            }

        with open('../src/data/dun.simulated_uptake_rate.geojson') as f:
            data_geojson = json.load(f)

        tooltip_fields = ['dun', 'population', 'fiber_tests',
                          'uptake_rate']
        data_layer = folium.GeoJson(
            data_geojson,
            name='Data',
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_fields,
                localize=True
            )
        )

        # Load the boundaries GeoJSON boundaries data
        with open('../src/data/dun.simulated_uptake_rate.geojson') as f:
            boundaries_geojson = json.load(f)

        boundaries_layer = folium.GeoJson(
            boundaries_geojson,
            name='Boundaries',
            style_function=lambda x: {'fillColor': 'white',
                                      'color': 'black', 
                                      'weight': 0.5, 
                                      'fillOpacity': 0.1},
            highlight_function=highlight_boundary,
        )
       
        m = folium.Map(location=[center_lat, center_lon], zoom_start=6.5,
                       tiles="cartodbpositron_nolabels", attr="CartoDB")
        m.add_child(boundaries_layer)
        m.add_child(data_layer)

        folium.LayerControl().add_to(m)
        
        # Set map width and height
        map_width, map_height = st.columns([1, 10])
        with map_width:
            st.write("")
        with map_height:
            folium_static(m, width=1600, height=700)
            
        st.markdown(
            f"""
             <div style="overflow-y: scroll; top: 1; right: 10;">
                <h1 style='font-size: 20px;'>Predicted Uptake Rate</h1>
                <p style='font-size: 16px;'>Map showing the predicted uptake rate of fiber in Malaysia</p>
            </div>
        """,
    unsafe_allow_html=True,
)
       
        # Create a color gradient using linear colormap
        colormap = cm.linear.YlOrRd_09.scale(0,0.99) 
        
        # Load the data GeoJSON fiber data

        def style_function(feature):
            data_value = feature['properties']['simulated_uptake_rate']
            return {'fillColor': colormap(data_value)}

        def highlight_boundary(feature):
            return {
                'fillColor': '#98abc5',
                'fillOpacity': 0.5,
                'color': '#000000',
                'weight': 0.5
            }

        with open('../src/data/dun.simulated_uptake_rate.geojson') as f:
            data_geojson = json.load(f)

        tooltip_fields = ['dun','simulated_uptake_rate']
        data_layer = folium.GeoJson(
            data_geojson,
            name='Data',
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=tooltip_fields,
                aliases=tooltip_fields,
                localize=True
            )
        )

        # Load the boundaries GeoJSON boundaries data
        with open('../src/data/dun.simulated_uptake_rate.geojson') as f:
            boundaries_geojson = json.load(f)

        boundaries_layer = folium.GeoJson(
            boundaries_geojson,
            name='Boundaries',
            style_function=lambda x: {'fillColor': 'white',
                                      'color': 'black', 
                                      'weight': 0.1, 
                                      'fillOpacity': 0.01},
            highlight_function=highlight_boundary,
        )
       
        m = folium.Map(location=[center_lat, center_lon], zoom_start=6.5,
                       tiles="cartodbpositron_nolabels", attr="CartoDB")
        m.add_child(boundaries_layer)
        m.add_child(data_layer)

        folium.LayerControl().add_to(m)
        
        # Set map width and height
        map_width, map_height = st.columns([1, 10])
        with map_width:
            st.write("")
        with map_height:
            folium_static(m, width=1600, height=700)
  

        # Add content to Uptake Rate Graphs
    elif sub_selection == "Graph":
        Graph_menu = ["Current Uptake Rate", "Predicted Uptake Rate" ]
        sub_selection_2 = st.sidebar.radio("Select an option", Graph_menu)
        
        # Add submenu to Graph menu
        
        if sub_selection_2 == "Current Uptake Rate":
        
            st.markdown(
        f"""
        <div style="overflow-y: scroll; top: 1; right: 10;">
            <h1 style='font-size: 16px;'>Uptake Rate</h1>
            <p style='font-size: 16px;'>Graph showing average uptake rate of fiber in Malaysia</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
            # Load the GeoDataFrame
            gdf = gpd.read_file('../src/data/dun.simulated_uptake_rate.geojson')
            
            # Drop the 'geometry' column
            filtered_gdf = gdf.drop('geometry', axis=1)
            
            # Sort the GeoDataFrame based on a certain metric
            sorted_gdf = filtered_gdf.sort_values(by='uptake_rate', ascending=False)

            # Select the top ten rows
            top_ten = sorted_gdf.head(10)
                
            # Create a bar graph using Altair
            bar_chart = alt.Chart(top_ten).mark_bar().encode(
            x=alt.X('dun',  sort='-y'),
                y='uptake_rate',
                color=alt.Color('uptake_rate', scale=alt.Scale(scheme='greens')),
                tooltip=['dun', 'uptake_rate']
            ).properties(
                width=1, # Adjust the width of the bars
                height=600
            )

            # Display the bar graph on Streamlit
            st.altair_chart(bar_chart, use_container_width=True)
            
            # Select the bottom ten rows
            bottom_ten = sorted_gdf.tail(10)
                
            # Create a bar graph showing the lowest uptake rates
            bar_chart = alt.Chart(bottom_ten).mark_bar().encode(
                x=alt.X('dun',  sort='-y'),
                y='uptake_rate',
                color=alt.Color('uptake_rate', scale=alt.Scale(scheme='reds')),
                tooltip=['dun', 'uptake_rate']
            ).properties(
                width=alt.Step(10), # Adjust the width of the bars
                height=600
            )
            # Display the bar graph on Streamlit
            st.altair_chart(bar_chart, use_container_width=True)
                            
            # Create a bar graph showing the current uptake rate
            bar_chart = alt.Chart(filtered_gdf).mark_bar().encode(
                x=alt.X('dun',  sort='-y'),
                y='uptake_rate',
                color=alt.value('steelblue'),  # Set a constant color for all bars,
                tooltip=['dun', 'uptake_rate']
            ).properties(
                width=2, # Adjust the width of the bars
                height=750 # Adjust the height of the bars
            )     

            # Display the bar graph on Streamlit
            st.altair_chart(bar_chart, use_container_width=True)
            
        elif sub_selection_2 == "Predicted Uptake Rate":       
            st.markdown(
        f"""
        <div style="overflow-y: scroll; top: 1; right: 10;">
            <h1 style='font-size: 16px;'>Predicted Uptake Rate</h1>
            <p style='font-size: 16px;'>Graph showing average predicted uptake rate of fiber in Malaysia</p>
        </div>
        """,
        unsafe_allow_html=True,
    )       
            # Load the GeoDataFrame
            gdf = gpd.read_file('../src/data/dun.simulated_uptake_rate.geojson')
            
            # Drop the 'geometry' column
            filtered_gdf = gdf.drop('geometry', axis=1)
                
            # Sort the GeoDataFrame based on a certain metric
            sorted_gdf = filtered_gdf.sort_values(by='simulated_uptake_rate', ascending=False)

            # Select the top ten rows
            top_ten = sorted_gdf.head(10)
                
            # Create a bar graph using Altair
            bar_chart = alt.Chart(top_ten).mark_bar().encode(
            x=alt.X('dun',  sort='-y'),
                y='simulated_uptake_rate',
                color=alt.Color('simulated_uptake_rate', scale=alt.Scale(scheme='greens')),
                tooltip=['dun', 'simulated_uptake_rate']
            ).properties(
                width=1, # Adjust the width of the bars
                height=600
            )

            # Display the bar graph on Streamlit
            st.altair_chart(bar_chart, use_container_width=True)
            
            # Select the bottom ten rows
            bottom_ten = sorted_gdf.tail(10)
                
            # Create a bar graph showing the lowest uptake rates
            bar_chart = alt.Chart(bottom_ten).mark_bar().encode(
                x=alt.X('dun',  sort='-y'),
                y='simulated_uptake_rate',
                color=alt.Color('simulated_uptake_rate', scale=alt.Scale(scheme='reds')),
                tooltip=['dun', 'simulated_uptake_rate']
            ).properties(
                width=alt.Step(10), # Adjust the width of the bars
                height=600
            )
            # Display the bar graph on Streamlit
            st.altair_chart(bar_chart, use_container_width=True)
                            
            # Create a bar graph showing the current uptake rate
            bar_chart = alt.Chart(filtered_gdf).mark_bar().encode(
                x=alt.X('dun',  sort='-y'),
                y='simulated_uptake_rate',
                color=alt.value('steelblue'),  # Set a constant color for all bars,
                tooltip=['dun', 'simulated_uptake_rate']
            ).properties(
                width=2, # Adjust the width of the bars
                height=750 # Adjust the height of the bars
            )     

            # Display the bar graph on Streamlit
            st.altair_chart(bar_chart, use_container_width=True)
            
                      
# Add content to About menu
elif selection == "About":
    About_menu = ["The Team", "The Project" ]
    sub_selection = st.sidebar.radio("Select an option", About_menu)
       # Add submenu to About menu
    if sub_selection == "The Team":
        st.markdown(
    f"""
    <div style="overflow-y: scroll; top: 1; right: 10;">
      <h1 style='font-size: 16px;'>Meet the Team</h1>
      <p style='font-size: 16px;'>Below is a list of the Brilliant Minds behind the Project</p>
    </div>
    """,
    unsafe_allow_html=True,
)   
        # Open the JPEG image file        
        image = Image.open('../src/data/member_pictures/Gracious.jpeg')

        # Display the image in Streamlit
        
        # Resize the image to a square shape
        size = (256, 256)  # Replace with your desired size
        resized_image = ImageOps.fit(image, size, Image.ANTIALIAS).convert("RGBA")

        # Create a circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        # Apply the circular mask to the resized image
        masked_image = Image.alpha_composite(Image.new("RGBA", resized_image.size), resized_image)
        masked_image.putalpha(mask)
        
        # Add text to the right of the image
        st.markdown(
            """
            <div style="position: absolute; top: 120px; left: 500px; padding: 0;">
                <p>The complex way the internet works would be science fiction to people 100 years ago. Today it's something we take for granted.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.image(masked_image, caption='Gracious Ngetich | Data Engineer | Team Lead')
        
        # Open the JPEG image file
        image = Image.open('../src/data/member_pictures/John.jpeg')

        # Display the image in Streamlit
        
        # Resize the image to a square shape
        size = (256, 256)  # Replace with your desired size
        resized_image = ImageOps.fit(image, size, Image.ANTIALIAS).convert("RGBA")

        # Create a circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        # Apply the circular mask to the resized image
        masked_image = Image.alpha_composite(Image.new("RGBA", resized_image.size), resized_image)
        masked_image.putalpha(mask)

        # Add text to the right of the image
        st.markdown(
            """
            <div style="position: absolute; top: 120px; left: 500px; padding: 0;">
                <p>In the pursuit of wisdom, we must release the shackles of our own preconceptions.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.image(masked_image, caption='John Chukwuebuka | Data Scientist')
        
        # Open the JPEG image file
        image = Image.open('../src/data/member_pictures/Yusuf.jpeg')

        # Display the image in Streamlit
        
        # Resize the image to a square shape
        size = (256, 256)  # Replace with your desired size
        resized_image = ImageOps.fit(image, size, Image.ANTIALIAS).convert("RGBA")

        # Create a circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        # Apply the circular mask to the resized image
        masked_image = Image.alpha_composite(Image.new("RGBA", resized_image.size), resized_image)
        masked_image.putalpha(mask)
        
        # Add text to the right of the image
        st.markdown(
            """
            <div style="position: absolute; top: 120px; left: 500px; padding: 0;">
                <p>Embrace the boundless possibilities of growth, where every unknown becomes an opportunity to expand our horizons.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.image(masked_image, caption='Yusuf Kebande | Data Engineer')
        
                
        # Open the JPEG image file
        image = Image.open('../src/data/member_pictures/Tebogo.jpeg')

        # Display the image in Streamlit
        
        # Resize the image to a square shape
        size = (256, 256)  # Replace with your desired size
        resized_image = ImageOps.fit(image, size, Image.ANTIALIAS).convert("RGBA")

        # Create a circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        # Apply the circular mask to the resized image
        masked_image = Image.alpha_composite(Image.new("RGBA", resized_image.size), resized_image)
        masked_image.putalpha(mask)

        # Add text to the right of the image
        st.markdown(
            """
            <div style="position: absolute; top: 120px; left: 500px; padding: 0;">
                <p>Transforming the extraordinary into the everyday, one innovation at a time.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.image(masked_image, caption='Tebogo Mngoma | Data Scientist')
        
        # Open the JPEG image file
        image = Image.open('../src/data/member_pictures/Kabelo.jpg')

        # Display the image in Streamlit
        
        # Resize the image to a square shape
        size = (256, 256)  # Replace with your desired size
        resized_image = ImageOps.fit(image, size, Image.ANTIALIAS).convert("RGBA")

        # Create a circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        # Apply the circular mask to the resized image
        masked_image = Image.alpha_composite(Image.new("RGBA", resized_image.size), resized_image)
        masked_image.putalpha(mask)
        
        # Add text to the right of the image
        st.markdown(
            """
            <div style="position: absolute; top: 120px; left: 500px; padding: 0;">
                <p>You cannot learn what you already know.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.image(masked_image, caption='Kabelo Tladi| Data Scientist')
        
        
    elif sub_selection == "The Project" :
        st.title("The Project")
        st.markdown(
    f"""
    <div style="overflow-y: scroll; top: 1; right: 10;">
        <h1 style='font-size: 16px;'>Introduction</h1>
        <p style='font-size: 14px;'>Fibre roll-out is a process that involves deploying fibre optic cables across a geographical region to provide faster and more reliable internet access to more people, which can improve economic opportunities and quality of life. With the increasing demand for online activities such as video conferencing, companies encouraging work from home, and cloud computing, having a fast and reliable internet connection is becoming more and more essential.</p>
        <h1 style='font-size: 16px;'>Problem Statement</h1>
        <p style='font-size: 14px;'>In many emerging markets, telecommunication companies face challenges in expanding their fibre network due to limited data-driven tools to support their revenue-driven expansion plans. Traditional SaaS solutions mainly focus on advanced cost calculations, which fail to support possible expansion areas from an ROI point of view. In order to solve this problem, we propose to create a tool that can predict revenue across geographies based on publicly available information, as highly detailed as possible.</p>
        <h1 style='font-size: 16px;'>Proposed Solution</h1>
        <p style='font-size: 14px;'>This tool will predict revenue based on household uptake rates and competitive roll-outs across geographies. The output of the tool will consist of a visual map showing the most attractive fibre roll-out areas, including a dashboard showing the underlying units for that area such as the relative wealth index.</p>
        <p style='font-size: 14px;'>The underlying scalable algorithm and database will be based on free open-source data. We aim to identify households geospatially and provide metadata for this location such as expected people per household, income, and demographic information in Malaysia.</p>
    </div>
    """,
    unsafe_allow_html=True,
)       

# Add content to Contact Us menu
elif selection == "Contact Us":
    
        st.markdown(
    f"""
    <div style="overflow-y: scroll; top: 1; right: 10;">
      <h1 style='font-size: 20px;'>Contact Us</h1>
      <p style='font-size: 14px;'>Email the team behind the project through: team16@explore.ai</p>
      <h1 style='font-size: 16px;'>You can also reach out to individual members through their personal emails</h1>
      <p style='font-size: 14px;'>graciousngetich7712@protonmail.com</p>
      <p style='font-size: 14px;'>johnchukwuebukaj@gmail.com</p>
      <p style='font-size: 14px;'>yusufkebande@gmail.com</p>
      <p style='font-size: 14px;'>tebogo.mngoma@live.com</p>
      <p style='font-size: 14px;'>kabelo.tladi@gmail.com</p>
    </div>
    """,
    unsafe_allow_html=True,
)   