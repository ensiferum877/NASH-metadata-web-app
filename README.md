# NASH-metadata-web-app

In the era of high-troughput, there's an enormous wealth of biological data available in public repositories such as the Gene Expression Omnibus (GEO). These repositories, often seen as gold mines for researchers, harbor data that can transform our understanding of complex biological phenomena. Yet, a significant barrier exists: their metadata, information containing experiment specifications. This information is frequently unclean and unstructured. These challenges can severely interfere with the understanding of what really is available to perform further processing of this data.  

To address this issue, I queried data directly from GEO and then performed an extensive cleaning using GPT-4, combined with Langchain, proved instrumental. Leveraging GPT-4's unparalleled contextual understanding, I was able to transform the typically unstructured GEO metadata into a coherent and structured format, paving the way for in-depth analysis and visualization.

To illustrate the capabilities of the application of GPT4 on biological data. I have created an Streamlit dashboard visualizing experimental metadata related to NASH (Non-Alcoholic SteatoHepatitis). With the cleaned and structured metadata in hand, the dashboard offers a range of interactive visualizations, allowing users to delve deep into the insights and trends present in the data. From dynamic filtering options to diverse visualizations like word clouds, bar charts, and choropleth maps, the dashboard provides a comprehensive view of the NASH experimental landscape.

# Repository Contents

Data Acquisition and Preprocessing:

**Fetching Data**: Utilizing the GEOparse Python library, data relevant to NASH experiments was retrieved from the GEO database.
**Data Cleaning**: Leveraging the capabilities of GPT-4, combined with Langchain, the initially unstructured metadata was transformed into a structured format. This meticulous cleaning process was vital for extracting meaningful insights from the data.

# Dashboard Features

**Dynamic Filtering**: Users can filter visualizations based on parameters like country, assay, biomaterial category, and year, allowing for tailored insights.
Visualizations:
**Word Cloud**: Offers a visual representation of frequently mentioned terms in the dataset, providing quick insights into prevalent themes.
Bar and Box Charts: Displays distributions and key metrics, giving users a quantitative overview of the data.
**Pie Charts**: Breaks down distributions for categories like assay, biomaterial, and source tissue.
Choropleth Map: An animated geographical representation showing the number of studies by country over the years. This visualization provides a global view of NASH research trends.

# Acknowledgments 
This project relies on  GEOparse and biopython for data acquisition.
The cleaning and structuring of data were made possible by OpenAI's GPT-4 models and their integration with Langchain.
