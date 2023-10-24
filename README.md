# NASH-metadata-web-app

In the age of high-throughput technologies, vast amounts of biological data are continually accumulated in public repositories, notably the Gene Expression Omnibus (GEO). These repositories are seen as "gold mines" for researcher because they possess data that holds the potential to improve our comprehension of intricate biological phenomena. However, a formidable obstacle looms: the metadata. This metadata, essential in detailing experimental specifications, is often riddled with inconsistencies, and its unstructured nature poses a daunting challenge. Such impediments can critically hinder a researcher's ability to discern the available data's true potential and utility for further analysis.

To overcome this challenge, I queried data from GEO. Following this, a rigorous cleaning process was executed where the synergy of GPT-4 and Langchain emerged as definetely game-changer. By leveraging GPT-4, I transformed the traditionally chaotic GEO metadata into a clear, structured format, setting the stage for deeper analyses and visualization. Notably, to optimize costs, I've limited this processing to 50 records.

To showcase the transformative power of applying GPT-4 to biological data, I've developed a Streamlit dashboard that illustrate the experimental metadata pertinent Non-Alcoholic SteatoHepatitis (NASH).Equipped with this meticulously cleaned and organized metadata, the dashboard unfurls an array of interactive visualizations. Users can immerse themselves in rich insights and detect prevailing trends in the data. With features ranging from dynamic filters to a medley of visual representations such as word clouds, bar charts, and choropleth maps, this dashboard presents an exhaustive panorama of the NASH experimental domain.

## 🧬 Repository Contents

📥 Data Acquisition and Preprocessing:

**Fetching Data**: Utilizing the GEOparse Python library, data relevant to NASH experiments was retrieved from the GEO database.

**Data Cleaning**: Leveraging the capabilities of GPT-4, combined with Langchain, the initially unstructured metadata was transformed into a structured format. This meticulous cleaning process was vital for extracting meaningful insights from the data.

## 🖥️ Dashboard Features

**🔍Dynamic Filtering**: Users can filter visualizations based on parameters like country, assay, biomaterial category, and year, allowing for tailored insights.

### Visualizations:

**☁️Word Cloud**: Offers a visual representation of frequently mentioned terms in the dataset, providing quick insights into prevalent themes.

**📊Bar and Box Charts**: Displays distributions and key metrics, giving users a quantitative overview of the data.

**🥧 Pie Charts**: Breaks down distributions for categories like assay, biomaterial, and source tissue.

**🌍Choropleth Map**: An animated geographical representation showing the number of studies by country over the years. This visualization provides a global view of NASH research trends.

# Acknowledgments 

This project relies on  GEOparse and biopython for data acquisition.
The cleaning and structuring of data were made possible by OpenAI's GPT-4 models and their integration with Langchain.
