import streamlit as st
from google.cloud import storage
from datetime import timedelta
from google.oauth2 import service_account

secrets = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(secrets)

def generate_signed_url(blob_name):
    """Generates a signed URL to access a file in GCS."""
    try:
        bucket_name = "chickpea-transcriptome"  # Replace with your bucket name
        client = storage.Client(credentials=credentials)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        if not blob.exists():
            print(f"File {blob_name} does not exist in bucket {bucket_name}")  # Debugging
            return None
        url = blob.generate_signed_url(expiration=timedelta(hours=1), method='GET')
        print(f"Generated signed URL for {blob_name}: {url}")  # Debugging
        return url
    except Exception as e:
        print(f"Error generating signed URL for {blob_name}: {e}")  # Debugging
        return None

st.set_page_config(page_title="MultiClassClassificationInput App", layout="wide")
st.logo(generate_signed_url("pvz.gif"), size="large")
pages = [
    st.Page("Pages/Home_Page.py", title="Home",icon="🏠"),
    st.Page("Pages/Start_Task.py", title="Start Task",icon="🧑🏻‍💻"),
    st.Page("Pages/Meta_Data.py", title="Meta Data",icon="📊"),
    st.Page("Pages/Glossary.py", title="Glossary",icon="📖"),
    st.Page("Pages/Demonstration.py", title="Demonstration",icon="🎬"),
    st.Page("Pages/About.py", title="About",icon="❔"),
]
pg = st.navigation(pages, position="sidebar", expanded=True)

pg.run()