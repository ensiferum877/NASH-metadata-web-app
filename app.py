import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set the page to wide layout
st.set_page_config(layout="wide")

font_css = """
<style>
    body {
        font-family: Arial, sans-serif !important;
    }
    .stButton>button {
        font-family: Arial, sans-serif !important;
    }
    .stTextInput>div>div>input {
        font-family: Arial, sans-serif !important;
    }
    .stSelectbox>div>div>select {
        font-family: Arial, sans-serif !important;
    }
    /* Add more Streamlit-specific selectors if needed */
</style>
"""

st.markdown(font_css, unsafe_allow_html=True)

# Change the color of the sidebar
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #838b8b;
    }
</style>
""", unsafe_allow_html=True)

# STEP 1 : LOAD DATA
final_df = pd.read_csv('NASH_geo_clean.csv')
final_df['year'] = pd.to_datetime(final_df['submission_date']).dt.year

# STEP 2 : CREATE DROPDOWNS

# Sidebar filters
st.sidebar.header('Filters')

# Dropdown for Countries
countries = ['ALL'] + sorted(final_df['contact_country'].unique().tolist(),reverse=True)
selected_country = st.sidebar.selectbox('Select Country', countries)

# Dropdown for Assays
assays = ['ALL'] + sorted(final_df['Assay'].unique().tolist(),reverse=True)
selected_assay = st.sidebar.selectbox('Select Assay', assays)

# Dropdown for Biomaterial_Category
biomaterials = ['ALL'] + sorted(final_df['Biomaterial_Category'].unique().tolist(),reverse=True)
selected_biomaterial = st.sidebar.selectbox('Select Biomaterial Category', biomaterials)

# Dropdown for year
year = ['ALL'] + sorted(final_df['year'].unique().tolist(),reverse=True)
selected_year = st.sidebar.selectbox('Select year: ', year)

# Filter the dataframe based on all the selected values
filtered_df = final_df.copy()

if selected_country != 'ALL':
    filtered_df = filtered_df[filtered_df['contact_country'] == selected_country]

if selected_assay != 'ALL':
    filtered_df = filtered_df[filtered_df['Assay'] == selected_assay]

if selected_biomaterial != 'ALL':
    filtered_df = filtered_df[filtered_df['Biomaterial_Category'] == selected_biomaterial]

if selected_year != 'ALL':
    filtered_df = filtered_df[filtered_df['year'] == selected_year]

# STEP 3: CREATE THE FIRST ROW CONTAINING IMPORTANT NUMBERS ABOUT THE DATA COLLECTED

unique_counts = {
    "Studies" : filtered_df.shape[0],
    "Samples" : filtered_df['Number_of_samples'].sum(),
    "Countries": filtered_df["contact_country"].nunique(),
    "Model organisms": filtered_df["Organism"].nunique(),
    "Source Tissues": filtered_df["Source_Tissue"].nunique(),
    "Cell profiled": filtered_df["CellType_Name"].nunique(),
    "NGS Assays": filtered_df["Assay"].nunique()
}

def display_kpi_tile(title, value):
    """Display a KPI tile with a title and value."""
    st.markdown(f"""
    <div style="padding:20px; 
                border: 1px solid light grey; 
                border-radius: 10px; 
                height: 200px; 
                width: 210px; 
                display: flex; 
                flex-direction: column; 
                justify-content: space-between; 
                align-items: center;">
        <h3 style="color: grey;">{title}</h3>
        <h1 style="height: 70px; 
        display: flex;
        justify-content: space-between;
        align-items: center;">{value}</h1>
    </div>
    """, unsafe_allow_html=True)

def display_dashboard(unique_counts):
    # Display title
    st.title("NASH GEO experimental metadata")

    # Display all KPI tiles in a single row
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        display_kpi_tile("Studies", unique_counts["Studies"])
    with col2:
        display_kpi_tile("Samples", unique_counts["Samples"])
    with col3:
        display_kpi_tile("Countries", unique_counts["Countries"])
    with col4:
        display_kpi_tile("Model organisms", unique_counts["Model organisms"])
    with col5:
        display_kpi_tile("Source Tissues", unique_counts["Source Tissues"])
    with col6:
        display_kpi_tile("Cell profiled", unique_counts["Cell profiled"])
    with col7:
        display_kpi_tile("NGS Assays", unique_counts["NGS Assays"])
        

display_dashboard(unique_counts)

# Separating line
st.markdown("<hr style='height:2px;border-width:0;color:gray;background-color:gray'>", unsafe_allow_html=True)


# STEP 4: WORD CLOUD
import ast
# Convert the string representation of lists back to actual lists
filtered_df['Experiment_Endpoints'] = filtered_df['Experiment_Endpoints'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
endpoints_strings = [' '.join(map(str, endpoint_list)) for endpoint_list in filtered_df['Experiment_Endpoints'].dropna()]

# Combine all endpoint strings into one large string
text_combined = ' '.join(endpoints_strings)

# Create a figure and axis using matplotlib
fig, ax = plt.subplots(figsize=(10, 7))

# Generate the word cloud
wc = WordCloud(
    width=800, 
    height=600, 
    background_color="white", 
    colormap='viridis', 
    max_words=100
).generate(text_combined)

st.header('Keyword Landscape: A cloud representation of experimental aims')
# Use the axis to create the visualization
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
# Display the word cloud in Streamlit
st.pyplot(fig)

# Separating line
st.markdown("<hr style='height:2px;border-width:0;color:gray;background-color:gray'>", unsafe_allow_html=True)

# STEP 4:

def create_basic_pie_chart(column_name, title):
    fig = px.pie(filtered_df, names=column_name, title=title)

     # Outline the borders of the pie segments
    fig.update_traces(marker=dict(line=dict(color='white', width=2)))
    
    # Adjust the chart layout
    fig.update_layout(
        showlegend=False, 
        width=800, 
        height=600,
        paper_bgcolor="#2F2F2F",          # Background color outside the plot
        plot_bgcolor="white", # Plot background color
        title_font=dict(size=24, family="Arial", color="white"),
        margin=dict(t=50, b=50, l=150, r=150),
        title_x=0,
    )
    
    return fig

# Logic to count studies with and without experimental perturbations
def all_keys_none(row):
    try:
        # Convert the string representation of the dictionary back to an actual dictionary
        perturbations = ast.literal_eval(row['Experimental_perturbation'])
        
        # Check if all values in the dictionary are set to None
        return all(value is None for value in perturbations.values())
    except:
        return False

## STEP 4.1: BOX PLOTS

# Split the layout into 2 columns
st.title('Characteristics and Impact of experiments')
col1, col2, col3 = st.columns([1,1,1])
bg_color = "#2F2F2F" 

with col1:
    st.header('Experimental perturbations')
    # Fig1:
    filtered_df['all_keys_none_adjusted'] = filtered_df.apply(all_keys_none, axis=1)
    values_adjusted = filtered_df['all_keys_none_adjusted'].value_counts().tolist()

    # Plot
    labels_adjusted = ['Has Experimental Perturbation', 'No Experimental Perturbation']

    fig_adjusted = go.Figure(data=[
    go.Bar(x=labels_adjusted, y=values_adjusted, marker_color=['lightblue', 'coral'])
    ])
    
    fig_adjusted.update_layout(
    xaxis_title='Perturbation Status',
    yaxis_title='',
    title = 'Perturbations',
    template="plotly_white",
    width=350,  # Adjust the width to fit within the column
    height=400,  # Adjust the height
    paper_bgcolor = bg_color,
    title_font=dict(family="Arial", size=24, color="white"),
    legend_title_font=dict(family="Arial", size=14),
    legend_font=dict(family="Arial", size=12)
    )


    # Display on Streamlit
    st.plotly_chart(fig_adjusted)

    # Fig2:

    # Filter the DataFrame to only include studies with experimental perturbations
    perturbation_df = filtered_df[~filtered_df.apply(all_keys_none, axis=1)]

    # Extract and tally the perturbations
    perturbation_counts = {}
    for _, row in perturbation_df.iterrows():
        perturbations = ast.literal_eval(row['Experimental_perturbation'])
        for key, value in perturbations.items():
            if value is not None:
                perturbation_counts[key] = perturbation_counts.get(key, 0) + len(value)

    # Convert the perturbation_counts dictionary to a DataFrame
    perturbations_df = pd.DataFrame(list(perturbation_counts.items()), columns=['Perturbation', 'Count'])
    perturbations_df = perturbations_df.sort_values(by='Count', ascending=False)
    # Create the bar plot using Plotly Express
    fig = px.bar(perturbations_df, x='Perturbation', y='Count', title='Occurrences')
    fig.update_layout(width=350,
                      height=400,
                      title_font=dict(family="Arial", size=24, color="white"),
                      legend_title_font=dict(family="Arial", size=14),
                      legend_font=dict(family="Arial", size=12),
                      paper_bgcolor = bg_color,
                      yaxis_title=""
                     )

    # Display the plot in Streamlit
    st.plotly_chart(fig)


# Revised box plot creation inside col1
with col2:
    st.header('Experimental impact')
    
    box_option = st.radio(
        'Choose a Box Plot: ',
        ('Number of samples', 'Impact Factor', 'Citations')
    )
    
    plot_width = 350
    plot_height = 600
    bg_color = "#2F2F2F"  # Dark gray
    
    if box_option == 'Number of samples':
        fig = px.box(filtered_df, y='Number_of_samples', title="Number of Samples")
        
    elif box_option == 'Impact Factor':
        fig = px.box(filtered_df, y='journal_ImpactFactor', title="Impact Factor")
        
    else:
        fig = px.box(filtered_df, y='Citations', title="Citations")
    
    fig.update_layout(
        width=plot_width,
        autosize=False,
        height=plot_height, 
        paper_bgcolor=bg_color,
        title_font=dict(size=24, family="Arial", color="white"),
        yaxis_title="",
        margin=dict(t=50, b=50, l=150, r=150) 
    )
    st.plotly_chart(fig)
    
## STEP 4.2: PIE CHARTS: Display pie charts and radio button option for pie charts

with col3:
    st.header('Technology and biomaterial')

    option = st.radio(
        'Choose a Chart: ',
        ('Assay Distribution', 'Biomaterial Category Distribution', 'Source Tissue Distribution'))

    if option == 'Assay Distribution':
        # Display Assay pie chart
        fig_assay = create_basic_pie_chart('Assay', 'Assay Distribution')
        st.plotly_chart(fig_assay)
    
    elif option == 'Biomaterial Category Distribution':
        # Display Biomaterial Category pie chart
        fig_biomaterial = create_basic_pie_chart('Biomaterial_Category', 'Biomaterial Category Distribution')
        st.plotly_chart(fig_biomaterial)
    
    else:
        # Display Source Tissue pie chart
        fig_source_tissue = create_basic_pie_chart('Source_Tissue', 'Source Tissue Distribution')
        st.plotly_chart(fig_source_tissue)

# Separating line
st.markdown("<hr style='height:2px;border-width:0;color:gray;background-color:gray'>", unsafe_allow_html=True)

## STEP 5: WORLD MAP

# Aggregate the number of studies by country and year
aggregated_data = filtered_df.groupby(['contact_country', 'year']).size().reset_index(name='num_studies')
aggregated_data = aggregated_data.sort_values(by='year', ascending=False)

# Create a choropleth map with a slider for years
fig = px.choropleth(
    aggregated_data,
    locations="contact_country",
    locationmode='country names',
    color="num_studies",
    hover_name="contact_country",
    animation_frame="year",
    title="Number of Studies by Country Over Years",
    color_continuous_scale=px.colors.sequential.Plasma,
    projection="natural earth")

# Adjust the width and height of the figure
fig.update_layout(
    width=1500,     # Adjust width as needed
    height=800,      # Adjust height as needed
    title_font=dict(family="Arial", size=24, color="white"),
                      legend_title_font=dict(family="Arial", size=14),
                      legend_font=dict(family="Arial", size=12)
    )


# Display the choropleth map in full width
st.plotly_chart(fig, use_container_width=True)