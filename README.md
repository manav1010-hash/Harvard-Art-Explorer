# 🏛️ ***Harvard Art Museums Collection Explorer*** :
## Complete ETL, SQL Analytics & Streamlit Application

### 🎯 Project Overview -
This is a complete implementation of the Harvard Art Museums Collection Explorer project as per the requirements. The application provides an end to end ETL pipeline with interactive data exploration through a professional Streamlit interface.

### ✅ Project Requirements Met
- ✅ **API Integration**: Complete Harvard Art Museums API integration
- ✅ **Data Collection**: Fetch minimum 2,500 records per classification
- ✅ **3 SQL Tables**: artifact_metadata, artifact_media, artifact_colors
- ✅ **25+ SQL Queries**: 20 required + 5 bonus queries
- ✅ **Streamlit Interface**: Professional multi-tab interface
- ✅ **SQLite Database**: With proper foreign key relationships
- ✅ **Data Visualization**: 8 different chart types
- ✅ **Export Functionality**: CSV downloads for all data
- ✅ **Google Colab Compatible**: Designed for Colab environment
- ✅ **Beginner Friendly**: Detailed comments and error handling

### 🚀 How to Run in Google Colab

#### Step 1: Install Required Packages
```bash
!pip install streamlit plotly requests pandas sqlite3
```

#### Step 2: Upload the Application File
1. Upload `harvard_art_explorer.py` to your Colab session
2. Or copy the code from the provided file

#### Step 3: Run the Streamlit Application
```bash
# Start the Streamlit app
!streamlit run harvard_art_explorer.py --server.port 8501 &

# Get the public URL (Colab will provide this)
from pyngrok import ngrok
public_url = ngrok.connect(8501)
print(f"Access your app at: {public_url}")
```

#### Alternative Method (Simpler):
```bash
# Install ngrok for public access
!pip install pyngrok

# Run the app with automatic public URL
!streamlit run harvard_art_explorer.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false
```

### 🎨 Application Features

#### 📥 Data Collection Tab
- **Classification Selection**: Choose from 15+ popular classifications
- **Flexible Record Limits**: 100 to 5,000 records (minimum 2,500 recommended)
- **Real-time Progress**: Progress bars and status updates
- **Data Preview**: Immediate preview of collected data
- **CSV Export**: Download collected data

#### 🔍 SQL Queries Tab
- **25 Predefined Queries**: All project requirements covered
- **Custom Query Editor**: Write your own SQL queries
- **Real-time Results**: Instant query execution
- **Export Results**: Download query results as CSV
- **Error Handling**: Clear error messages for debugging

#### 📈 Visualizations Tab
- **8 Chart Types**: Bar charts, pie charts, timelines, treemaps
- **Interactive Charts**: Built with Plotly for interactivity
- **Real-time Data**: Charts update based on current database
- **Professional Design**: Color schemes and responsive layouts

#### 📊 Database Stats Tab
- **Real-time Statistics**: Live database metrics
- **Schema Information**: Complete table structure documentation
- **Recent Additions**: Track newly added artifacts
- **Project Status**: Monitor completion progress

### 🗃️ Database Schema

#### Table 1: artifact_metadata
```sql
CREATE TABLE artifact_metadata (
    id INTEGER PRIMARY KEY,
    title TEXT,
    culture TEXT,
    period TEXT,
    century TEXT,
    medium TEXT,
    dimensions TEXT,
    description TEXT,
    department TEXT,
    classification TEXT,
    accessionyear INTEGER,
    accessionmethod TEXT
);
```

#### Table 2: artifact_media
```sql
CREATE TABLE artifact_media (
    objectid INTEGER,
    imagecount INTEGER,
    mediacount INTEGER,
    colorcount INTEGER,
    rank INTEGER,
    datebegin INTEGER,
    dateend INTEGER,
    FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
);
```

#### Table 3: artifact_colors
```sql
CREATE TABLE artifact_colors (
    objectid INTEGER,
    color TEXT,
    spectrum TEXT,
    hue TEXT,
    percent REAL,
    css3 TEXT,
    FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
);
```

### 📋 Available Classifications
- Paintings (26)
- Sculpture (30)
- Coins (50)
- Jewelry (19)
- Drawings (21)
- Prints (23)
- Photographs (17)
- Manuscripts (185)
- Vessels (57)
- Furniture (76)
- Textile Arts (62)
- Weapons and Ammunition (155)
- Medals and Medallions (105)
- Books (47)
- Musical Instruments (359)

### 🔍 Sample SQL Queries Included

#### Basic Queries (1-10):
1. Artifacts from 11th century (Byzantine culture)
2. Unique cultures represented in artifacts
3. All artifacts from Archaic Period
4. Artifact titles ordered by accession year
5. How many artifacts per department
6. Artifacts with more than 1 image
7. Average rank of all artifacts
8. Artifacts where colorcount > mediacount
9. Artifacts created between 1500-1600
10. How many artifacts have no media files

#### Advanced Queries (11-20):
11. All distinct hues used in dataset
12. Top 5 most used colors by frequency
13. Average coverage percentage for each hue
14. List colors for specific artifacts
15. Total number of color entries
16. Byzantine artifacts with their hues
17. Artifact titles with associated hues
18. Artifacts with media ranks (period not null)
19. Top 10 ranked artifacts with Grey hue
20. Artifacts per classification + avg media count

#### Bonus Queries (21-25):
21. Most valuable artifacts by accession method
22. Color diversity by classification
23. Artifacts by century with comprehensive stats
24. Most colorful artifacts in collection
25. Culture and department distribution analysis

### 🎯 Key Technical Features

#### API Integration
- **Rate Limiting**: Built-in delays to respect API limits
- **Error Handling**: Comprehensive error management
- **Progress Tracking**: Real-time progress indicators
- **Data Validation**: Ensure data integrity

#### Database Management
- **SQLite Integration**: Lightweight, serverless database
- **Foreign Key Relationships**: Proper table relationships
- **Transaction Management**: Safe data insertion
- **Query Optimization**: Efficient query execution

#### User Interface
- **Responsive Design**: Works on all screen sizes
- **Intuitive Navigation**: Clear tab structure
- **Professional Styling**: Modern UI components
- **Help Text**: Tooltips and guidance throughout

### 🔧 Troubleshooting

#### Common Issues:

**1. Module Import Errors**
```bash
# Install missing packages
!pip install streamlit plotly requests pandas
```

**2. API Errors**
- Check API key is correctly configured
- Ensure internet connection is stable
- Verify classification names are correct

**3. Database Issues**
- Check if database file has write permissions
- Ensure sufficient disk space
- Verify SQLite3 is available

**4. Streamlit Port Issues**
```bash
# Use different port if 8501 is busy
!streamlit run harvard_art_explorer.py --server.port 8502
```

### 📞 Support and Customization

The application is designed to be beginner-friendly with:
- Detailed error messages
- Progress indicators
- Help tooltips
- Comprehensive documentation
- Clean, commented code

### 🏆 Project Success Metrics

Upon successful completion, you will have:
- ✅ 12,500+ artifact records (5 classifications × 2,500 each)
- ✅ Complete ETL pipeline
- ✅ Professional data visualization dashboard
- ✅ 25+ working SQL queries
- ✅ Interactive web application
- ✅ Exportable datasets
- ✅ Technical documentation

### 🎓 Learning Outcomes

This project demonstrates proficiency in:
- API integration and data extraction
- Database design and SQL querying
- Data transformation and cleaning
- Web application development
- Data visualization
- Project documentation
- Error handling and debugging

---

**Created for Harvard Art Museums Collection Explorer Project**
**API Key Pre-configured**: 60d0edd6-4596-49e5-ba97-2eacd79141db
**Compatible with**: Google Colab, Local Python environments
**Database**: SQLite (no setup required)
**Interface**: Streamlit web application
