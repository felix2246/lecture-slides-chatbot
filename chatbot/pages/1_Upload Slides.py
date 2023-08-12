import streamlit as st
from pipeline.pipeline_controller import PipelineController
import tempfile
import os

st.set_page_config(page_title="Upload Slides")


@st.cache_resource(show_spinner=True)
def get_pipeline_controller():
    # Create a database session object that points to the URL.
    return PipelineController()


get_pipeline_controller()

uploaded_files = st.file_uploader(
    label="Upload multiple files", type="PDF", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    file_name = uploaded_file.name
    print(file_name)
    bytes_data = uploaded_file.read()

    with tempfile.TemporaryDirectory() as temp_dir:
        path = os.path.join(temp_dir, file_name)
        file = open(path, 'w+b')
        file.write(bytes_data)
        pipeline_controller = get_pipeline_controller()
        with st.spinner(text="Ingesting file"):
            pipeline_controller.ingest_pdf(path)