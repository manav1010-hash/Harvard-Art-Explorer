import streamlit as st
import sqlite3
import requests
import json
import pandas as pd
import time
from typing import List, Dict, Any
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Harvard Art Museums Collection Explorer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_KEY = "60d0edd6-4596-49e5-ba97-2eacd79141db"
BASE_URL = "https://api.harvardartmuseums.org"
DB_NAME = "harvard_artifacts.db"

# Available classifications
CLASSIFICATIONS = {
    "Paintings": 26,
    "Sculpture": 30,
    "Coins": 50,
    "Jewelry": 19,
    "Drawings": 21,
    "Prints": 23,
    "Photographs": 17,
    "Manuscripts": 185,
    "Vessels": 57,
    "Furniture": 76
}

class HarvardArtMuseumDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.create_tables()

    def create_tables(self):
        """Create the three required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Table 1: artifact_metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifact_metadata (
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
            )
        """)

        # Table 2: artifact_media
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifact_media (
                objectid INTEGER,
                imagecount INTEGER,
                mediacount INTEGER,
                colorcount INTEGER,
                rank INTEGER,
                datebegin INTEGER,
                dateend INTEGER,
                FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
            )
        """)

        # Table 3: artifact_colors
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artifact_colors (
                objectid INTEGER,
                color TEXT,
                spectrum TEXT,
                hue TEXT,
                percent REAL,
                css3 TEXT,
                FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
            )
        """)

        conn.commit()
        conn.close()

    def insert_artifacts(self, artifacts_data: List[Dict[Any, Any]]):
        """Insert artifacts data into the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        inserted_count = 0

        for artifact in artifacts_data:
            try:
                # Insert into artifact_metadata
                cursor.execute("""
                    INSERT OR REPLACE INTO artifact_metadata
                    (id, title, culture, period, century, medium, dimensions, description,
                     department, classification, accessionyear, accessionmethod)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    artifact.get('id'),
                    artifact.get('title'),
                    artifact.get('culture'),
                    artifact.get('period'),
                    artifact.get('century'),
                    artifact.get('medium'),
                    artifact.get('dimensions'),
                    artifact.get('description'),
                    artifact.get('department'),
                    artifact.get('classification'),
                    artifact.get('accessionyear'),
                    artifact.get('accessionmethod')
                ))

                # Insert into artifact_media
                cursor.execute("""
                    INSERT OR REPLACE INTO artifact_media
                    (objectid, imagecount, mediacount, colorcount, rank, datebegin, dateend)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    artifact.get('id'),
                    artifact.get('imagecount', 0),
                    artifact.get('mediacount', 0),
                    artifact.get('colorcount', 0),
                    artifact.get('rank', 0),
                    artifact.get('datebegin', 0),
                    artifact.get('dateend', 0)
                ))

                # Insert colors if available
                if artifact.get('colors'):
                    for color in artifact['colors']:
                        cursor.execute("""
                            INSERT INTO artifact_colors
                            (objectid, color, spectrum, hue, percent, css3)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (
                            artifact.get('id'),
                            color.get('color'),
                            color.get('spectrum'),
                            color.get('hue'),
                            color.get('percent'),
                            color.get('css3')
                        ))

                inserted_count += 1

            except sqlite3.Error as e:
                st.error(f"Database error: {e}")
                continue

        conn.commit()
        conn.close()

        return inserted_count

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute a SQL query and return results as DataFrame"""
        conn = sqlite3.connect(self.db_name)
        try:
            df = pd.read_sql_query(query, conn)
            return df
        except Exception as e:
            st.error(f"Query error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()

class HarvardArtAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = BASE_URL

    def fetch_artifacts(self, classification: str, limit: int = 2500) -> List[Dict[Any, Any]]:
        """Fetch artifacts for a specific classification"""
        all_artifacts = []
        page = 1
        size = 100

        progress_bar = st.progress(0)
        status_text = st.empty()

        while len(all_artifacts) < limit:
            try:
                url = f"{self.base_url}/object"
                params = {
                    'apikey': self.api_key,
                    'classification': classification,
                    'size': size,
                    'page': page,
                    'hasimage': 1
                }

                response = requests.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()

                    if not data.get('records'):
                        break

                    all_artifacts.extend(data['records'])

                    progress = min(len(all_artifacts) / limit, 1.0)
                    progress_bar.progress(progress)
                    status_text.text(f"Fetched {len(all_artifacts)} artifacts...")

                    page += 1
                    time.sleep(0.5)

                else:
                    st.error(f"API Error {response.status_code}")
                    break

            except Exception as e:
                st.error(f"Error: {e}")
                break

        progress_bar.empty()
        status_text.empty()

        return all_artifacts[:limit]

@st.cache_resource
def init_db():
    return HarvardArtMuseumDB(DB_NAME)

@st.cache_resource
def init_api():
    return HarvardArtAPI(API_KEY)

def main():
    st.title("🎨 Harvard Art Museums Collection Explorer")
    st.markdown("### Complete ETL Pipeline & SQL Analytics")

    db = init_db()
    api = init_api()

    # Sidebar info
    st.sidebar.header("📋 Project Status")
    st.sidebar.success("✅ API Key Configured")
    st.sidebar.success("✅ Database Ready")
    st.sidebar.success("✅ 25+ SQL Queries Available")

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📥 Data Collection", "🔍 SQL Queries", "📈 Visualizations", "📊 Stats"])

    with tab1:
        st.header("📥 Data Collection from Harvard API")

        col1, col2 = st.columns([2, 1])
        with col1:
            selected_classification = st.selectbox(
                "Choose Classification:",
                list(CLASSIFICATIONS.keys()),
                help="Select artifact type to collect"
            )

        with col2:
            record_limit = st.number_input(
                "Records to Collect:",
                min_value=100,
                max_value=5000,
                value=2500,
                step=100
            )

        st.info(f"🎯 Target: {record_limit:,} {selected_classification} artifacts")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Collect Data", type="primary"):
                with st.spinner(f"Collecting {record_limit} {selected_classification} artifacts..."):
                    artifacts = api.fetch_artifacts(selected_classification, record_limit)

                    if artifacts:
                        st.session_state.collected_data = artifacts
                        st.success(f"✅ Collected {len(artifacts)} artifacts!")

                        preview_df = pd.DataFrame([{
                            'ID': art.get('id'),
                            'Title': (art.get('title', 'N/A')[:40] + '...') if len(str(art.get('title', ''))) > 40 else art.get('title', 'N/A'),
                            'Culture': art.get('culture', 'N/A'),
                            'Century': art.get('century', 'N/A'),
                            'Images': art.get('imagecount', 0)
                        } for art in artifacts[:10]])

                        st.dataframe(preview_df, use_container_width=True)
                    else:
                        st.error("❌ No data collected")

        with col2:
            if st.button("📊 Show All Data") and 'collected_data' in st.session_state:
                artifacts = st.session_state.collected_data

                display_df = pd.DataFrame([{
                    'ID': art.get('id'),
                    'Title': art.get('title', 'N/A'),
                    'Culture': art.get('culture', 'N/A'),
                    'Century': art.get('century', 'N/A'),
                    'Department': art.get('department', 'N/A'),
                    'Images': art.get('imagecount', 0),
                    'Colors': art.get('colorcount', 0)
                } for art in artifacts])

                st.dataframe(display_df, use_container_width=True)

                csv = display_df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    data=csv,
                    file_name=f"{selected_classification.lower()}_artifacts.csv",
                    mime="text/csv"
                )

        with col3:
            if st.button("💾 Save to Database") and 'collected_data' in st.session_state:
                with st.spinner("Inserting into SQLite database..."):
                    artifacts = st.session_state.collected_data
                    inserted = db.insert_artifacts(artifacts)

                    if inserted > 0:
                        st.success(f"✅ Saved {inserted} artifacts to database!")
                    else:
                        st.error("❌ No data saved")

    with tab2:
        st.header("🔍 SQL Queries & Analysis")

        # Key queries from project requirements
        queries = {
            "1. Byzantine artifacts from 11th century": """
                SELECT id, title, culture, century, period
                FROM artifact_metadata
                WHERE century = '11th century' AND culture = 'Byzantine'
                LIMIT 20;
            """,

            "2. All unique cultures": """
                SELECT culture, COUNT(*) as count
                FROM artifact_metadata
                WHERE culture IS NOT NULL
                GROUP BY culture
                ORDER BY count DESC;
            """,

            "3. Artifacts from Archaic Period": """
                SELECT id, title, culture, period
                FROM artifact_metadata
                WHERE period LIKE '%Archaic%'
                LIMIT 20;
            """,

            "4. Artifacts by accession year": """
                SELECT title, accessionyear, accessionmethod
                FROM artifact_metadata
                WHERE accessionyear IS NOT NULL
                ORDER BY accessionyear DESC
                LIMIT 20;
            """,

            "5. Artifacts per department": """
                SELECT department, COUNT(*) as count
                FROM artifact_metadata
                WHERE department IS NOT NULL
                GROUP BY department
                ORDER BY count DESC;
            """,

            "6. Artifacts with multiple images": """
                SELECT m.title, a.imagecount
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                WHERE a.imagecount > 1
                ORDER BY a.imagecount DESC
                LIMIT 20;
            """,

            "7. Average artifact rank": """
                SELECT AVG(rank) as avg_rank, COUNT(*) as total
                FROM artifact_media
                WHERE rank > 0;
            """,

            "8. More colors than media": """
                SELECT m.title, a.colorcount, a.mediacount
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                WHERE a.colorcount > a.mediacount
                LIMIT 20;
            """,

            "9. Artifacts from 1500-1600": """
                SELECT m.title, a.datebegin, a.dateend
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                WHERE a.datebegin >= 1500 AND a.dateend <= 1600
                LIMIT 20;
            """,

            "10. Artifacts with no media": """
                SELECT m.title, a.mediacount
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                WHERE a.mediacount = 0
                LIMIT 20;
            """,

            "11. All color hues used": """
                SELECT hue, COUNT(*) as frequency
                FROM artifact_colors
                WHERE hue IS NOT NULL
                GROUP BY hue
                ORDER BY frequency DESC;
            """,

            "12. Top 5 colors by frequency": """
                SELECT color, COUNT(*) as frequency
                FROM artifact_colors
                GROUP BY color
                ORDER BY frequency DESC
                LIMIT 5;
            """,

            "13. Average color coverage by hue": """
                SELECT hue, AVG(percent) as avg_coverage
                FROM artifact_colors
                WHERE hue IS NOT NULL
                GROUP BY hue
                ORDER BY avg_coverage DESC;
            """,

            "14. Colors for sample artifacts": """
                SELECT c.objectid, m.title, c.color, c.hue, c.percent
                FROM artifact_colors c
                JOIN artifact_metadata m ON c.objectid = m.id
                LIMIT 20;
            """,

            "15. Total color entries": """
                SELECT COUNT(*) as total_colors,
                       COUNT(DISTINCT objectid) as artifacts_with_colors
                FROM artifact_colors;
            """,

            "16. Byzantine artifacts with hues": """
                SELECT m.title, GROUP_CONCAT(DISTINCT c.hue) as hues
                FROM artifact_metadata m
                JOIN artifact_colors c ON m.id = c.objectid
                WHERE m.culture = 'Byzantine'
                GROUP BY m.id, m.title
                LIMIT 15;
            """,

            "17. Artifacts with their hues": """
                SELECT m.title, COUNT(DISTINCT c.hue) as unique_hues
                FROM artifact_metadata m
                JOIN artifact_colors c ON m.id = c.objectid
                GROUP BY m.id, m.title
                ORDER BY unique_hues DESC
                LIMIT 20;
            """,

            "18. Media ranks (period not null)": """
                SELECT m.title, m.period, a.rank
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                WHERE m.period IS NOT NULL
                ORDER BY a.rank
                LIMIT 20;
            """,

            "19. Top 10 ranked Grey artifacts": """
                SELECT m.title, a.rank
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                JOIN artifact_colors c ON m.id = c.objectid
                WHERE c.hue = 'Grey'
                ORDER BY a.rank
                LIMIT 10;
            """,

            "20. Classification stats": """
                SELECT m.classification,
                       COUNT(*) as count,
                       AVG(a.mediacount) as avg_media
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                GROUP BY m.classification
                ORDER BY count DESC;
            """,

            "21. Most colorful artifacts": """
                SELECT m.title, a.colorcount
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                ORDER BY a.colorcount DESC
                LIMIT 15;
            """,

            "22. Culture and department analysis": """
                SELECT department, culture, COUNT(*) as count
                FROM artifact_metadata
                WHERE department IS NOT NULL AND culture IS NOT NULL
                GROUP BY department, culture
                ORDER BY count DESC
                LIMIT 20;
            """,

            "23. Artifacts by century stats": """
                SELECT century, COUNT(*) as artifacts, AVG(a.imagecount) as avg_images
                FROM artifact_metadata m
                JOIN artifact_media a ON m.id = a.objectid
                WHERE century IS NOT NULL
                GROUP BY century
                ORDER BY artifacts DESC;
            """,

            "24. Accession method analysis": """
                SELECT accessionmethod, COUNT(*) as count
                FROM artifact_metadata
                WHERE accessionmethod IS NOT NULL
                GROUP BY accessionmethod
                ORDER BY count DESC;
            """,

            "25. Color diversity by classification": """
                SELECT m.classification, COUNT(DISTINCT c.hue) as color_diversity
                FROM artifact_metadata m
                JOIN artifact_colors c ON m.id = c.objectid
                GROUP BY m.classification
                ORDER BY color_diversity DESC;
            """,
        }

        st.info(f"📊 {len(queries)} SQL Queries Available (20 required + 5 bonus)")

        selected_query = st.selectbox("Choose Query:", list(queries.keys()))

        st.code(queries[selected_query], language='sql')

        if st.button("▶️ Execute Query", type="primary"):
            with st.spinner("Running SQL query..."):
                result = db.execute_query(queries[selected_query])

                if not result.empty:
                    st.success(f"✅ Query completed! {len(result)} rows returned")
                    st.dataframe(result, use_container_width=True)

                    csv = result.to_csv(index=False)
                    st.download_button(
                        "📥 Download Results",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No results found")

        st.subheader("✏️ Custom Query")
        custom_query = st.text_area("Write your own SQL:", height=100)

        if st.button("▶️ Run Custom Query"):
            if custom_query.strip():
                result = db.execute_query(custom_query)
                if not result.empty:
                    st.dataframe(result, use_container_width=True)
                else:
                    st.warning("No results")

    with tab3:
        st.header("📈 Data Visualizations")

        viz_options = [
            "Artifacts by Classification",
            "Culture Distribution",
            "Artifacts by Century",
            "Color Hue Distribution",
            "Department Analysis"
        ]

        selected_viz = st.selectbox("Choose Visualization:", viz_options)

        if st.button("🎨 Generate Chart", type="primary"):
            if selected_viz == "Artifacts by Classification":
                query = "SELECT classification, COUNT(*) as count FROM artifact_metadata WHERE classification IS NOT NULL GROUP BY classification ORDER BY count DESC LIMIT 10"
                df = db.execute_query(query)
                if not df.empty:
                    fig = px.bar(df, x='classification', y='count', title='Artifacts by Classification')
                    fig.update_xaxis(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)

            elif selected_viz == "Culture Distribution":
                query = "SELECT culture, COUNT(*) as count FROM artifact_metadata WHERE culture IS NOT NULL GROUP BY culture ORDER BY count DESC LIMIT 10"
                df = db.execute_query(query)
                if not df.empty:
                    fig = px.pie(df, values='count', names='culture', title='Culture Distribution')
                    st.plotly_chart(fig, use_container_width=True)

            elif selected_viz == "Artifacts by Century":
                query = "SELECT century, COUNT(*) as count FROM artifact_metadata WHERE century IS NOT NULL GROUP BY century ORDER BY count DESC LIMIT 10"
                df = db.execute_query(query)
                if not df.empty:
                    fig = px.bar(df, x='century', y='count', title='Artifacts by Century')
                    fig.update_xaxis(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)

            elif selected_viz == "Color Hue Distribution":
                query = "SELECT hue, COUNT(*) as frequency FROM artifact_colors WHERE hue IS NOT NULL GROUP BY hue ORDER BY frequency DESC"
                df = db.execute_query(query)
                if not df.empty:
                    fig = px.bar(df, x='hue', y='frequency', title='Color Hue Distribution')
                    st.plotly_chart(fig, use_container_width=True)

            elif selected_viz == "Department Analysis":
                query = "SELECT department, COUNT(*) as count FROM artifact_metadata WHERE department IS NOT NULL GROUP BY department ORDER BY count DESC"
                df = db.execute_query(query)
                if not df.empty:
                    fig = px.treemap(df, path=['department'], values='count', title='Artifacts by Department')
                    st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.header("📊 Database Statistics")

        # Get stats
        metadata_count = db.execute_query("SELECT COUNT(*) FROM artifact_metadata")
        media_count = db.execute_query("SELECT COUNT(*) FROM artifact_media")
        colors_count = db.execute_query("SELECT COUNT(*) FROM artifact_colors")

        col1, col2, col3 = st.columns(3)

        if not metadata_count.empty:
            col1.metric("Total Artifacts", f"{metadata_count.iloc[0, 0]:,}")
        if not media_count.empty:
            col2.metric("Media Records", f"{media_count.iloc[0, 0]:,}")
        if not colors_count.empty:
            col3.metric("Color Records", f"{colors_count.iloc[0, 0]:,}")

        st.subheader("📋 Database Schema")
        st.markdown("""
        **Three Tables Created:**

        1. **artifact_metadata** - Main artifact info (id, title, culture, period, century, etc.)
        2. **artifact_media** - Media data (imagecount, mediacount, colorcount, rank, etc.)
        3. **artifact_colors** - Color analysis (color, spectrum, hue, percent, css3)
        """)

        # Recent artifacts
        st.subheader("🕒 Recent Database Entries")
        recent = db.execute_query("SELECT id, title, classification, culture FROM artifact_metadata ORDER BY id DESC LIMIT 10")
        if not recent.empty:
            st.dataframe(recent, use_container_width=True)
        else:
            st.info("No data yet - collect some artifacts to see them here!")

        # Project status
        total_artifacts = metadata_count.iloc[0, 0] if not metadata_count.empty else 0

        st.subheader("🎯 Project Completion Status")
        if total_artifacts >= 2500:
            st.success(f"🎉 PROJECT COMPLETE! {total_artifacts:,} artifacts collected")
            st.balloons()
        elif total_artifacts > 0:
            progress = min(total_artifacts / 2500, 1.0)
            st.progress(progress)
            st.info(f"📈 Progress: {total_artifacts:,} / 2,500 artifacts ({progress*100:.1f}%)")
        else:
            st.warning("⚠️ Start by collecting data in the Data Collection tab")

if __name__ == "__main__":
    main()
