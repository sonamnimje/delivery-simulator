"""
Streamlit UI for Document Extraction Platform.
"""

import json
from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
import streamlit as st
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Document Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API Base URL
API_BASE_URL = "http://localhost:8000/api/v1"


def load_css():
    """Load custom CSS styles."""
    st.markdown(
        """
        <style>
        .main {
            padding: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            padding: 10px 20px;
        }
        .success-box {
            background-color: #d4edda;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }
        .error-box {
            background-color: #f8d7da;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
        }
        .info-box {
            background-color: #d1ecf1;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #17a2b8;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def upload_document_tab():
    """Tab for uploading and processing documents."""
    st.header("📤 Upload Document")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Upload File")
        uploaded_file = st.file_uploader(
            "Choose a document (PDF, JPG, PNG)",
            type=["pdf", "jpg", "jpeg", "png"],
            help="Upload a document to extract information from",
        )

    with col2:
        st.subheader("Supported Types")
        st.write("- 📋 Aadhaar Card")
        st.write("- 🚗 Driving License")
        st.write("- 🛂 Passport")
        st.write("- 📑 Invoice")

    if uploaded_file:
        # Display file information
        st.info(f"**File:** {uploaded_file.name} | **Size:** {uploaded_file.size / 1024:.2f} KB")

        # Display preview
        if uploaded_file.type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Document Preview", use_column_width=True)
        elif uploaded_file.type == "application/pdf":
            st.warning("PDF preview requires additional dependencies. Processing will extract text from PDF.")

        # Process button
        if st.button("🔍 Process Document", use_container_width=True):
            with st.spinner("Processing document..."):
                try:
                    # Upload file
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(
                        f"{API_BASE_URL}/upload-document",
                        files=files,
                        timeout=120,
                    )

                    if response.status_code == 200:
                        result = response.json()

                        # Store in session
                        st.session_state.last_result = result

                        # Success message
                        st.markdown(
                            """
                            <div class='success-box'>
                                <strong>✓ Document processed successfully!</strong>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Display results
                        st.subheader("📊 Extraction Results")

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(
                                "Document Type",
                                result.get("document_type", "Unknown"),
                            )
                        with col2:
                            confidence = float(
                                result.get("confidence_score", 0)
                            )
                            st.metric(
                                "Confidence",
                                f"{confidence * 100:.1f}%",
                            )
                        with col3:
                            st.metric("Document ID", result.get("id"))

                        # Display extracted data
                        st.subheader("📋 Extracted Information")
                        extracted_data = result.get("extracted_data", {})

                        if extracted_data:
                            cols = st.columns(2)
                            for idx, (key, value) in enumerate(extracted_data.items()):
                                col = cols[idx % 2]
                                with col:
                                    st.text_input(
                                        key.replace("_", " ").title(),
                                        value=str(value) if value else "",
                                        disabled=True,
                                    )
                        else:
                            st.warning("No data extracted")

                        # Show JSON view
                        with st.expander("📄 View Raw JSON"):
                            st.json(result)

                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.markdown(
                            f"""
                            <div class='error-box'>
                                <strong>✗ Error:</strong> {error_detail}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                except requests.exceptions.ConnectionError:
                    st.markdown(
                        """
                        <div class='error-box'>
                            <strong>✗ Error:</strong> Cannot connect to API server. 
                            Make sure the backend is running on http://localhost:8000
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                except requests.exceptions.Timeout:
                    st.markdown(
                        """
                        <div class='error-box'>
                            <strong>✗ Error:</strong> Request timeout. Document processing took too long.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.markdown(
                        f"""
                        <div class='error-box'>
                            <strong>✗ Error:</strong> {str(e)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def documents_history_tab():
    """Tab for viewing document history."""
    st.header("📚 Document History")

    # Pagination controls
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        skip = st.number_input("Skip", min_value=0, value=0, step=10)
    with col2:
        limit = st.number_input("Limit", min_value=1, max_value=100, value=20)

    try:
        # Fetch documents
        response = requests.get(
            f"{API_BASE_URL}/documents",
            params={"skip": skip, "limit": limit},
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            documents = data.get("documents", [])
            total = data.get("total", 0)

            st.metric("Total Documents", total)

            if documents:
                # Create table
                st.subheader("Documents")
                for doc in documents:
                    with st.expander(
                        f"📄 {doc['original_filename']} - {doc['document_type'].replace('_', ' ').title()}"
                    ):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**ID:** {doc['id']}")
                        with col2:
                            st.write(f"**Confidence:** {doc.get('confidence_score', 'N/A')}")
                        with col3:
                            st.write(
                                f"**Created:** {doc['created_at'][:10]}"
                            )

                        # View details button
                        if st.button(f"View Details", key=f"view_{doc['id']}"):
                            st.session_state.selected_document_id = doc["id"]
                            st.switch_page("pages/document_detail.py")
            else:
                st.info("No documents found")

        else:
            st.error("Failed to fetch documents")

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to API server. Make sure the backend is running."
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")


def about_tab():
    """Tab with application information."""
    st.header("ℹ️ About")

    st.markdown(
        """
        ### Document Extraction Platform
        
        A modern, intelligent document extraction system that leverages cutting-edge OCR 
        and LLM technologies to automatically extract structured information from documents.
        
        #### Features
        - 📄 **Multi-format Support**: PDF, JPG, PNG
        - 📋 **Multiple Document Types**: Aadhaar, Driving License, Passport, Invoice
        - 🤖 **LLM-Powered Extraction**: Uses OpenAI GPT-4 for accurate field extraction
        - 👁️ **Advanced OCR**: PaddleOCR with Tesseract fallback
        - ✅ **Validation**: Ensures data quality and consistency
        - 💾 **Database Storage**: Persists all extracted data
        
        #### Supported Document Types
        
        **1. Aadhaar Card**
        - Full Name
        - Date of Birth
        - Aadhaar Number
        - Address
        
        **2. Driving License**
        - Full Name
        - License Number
        - Date of Birth
        - Expiry Date
        
        **3. Passport**
        - Full Name
        - Passport Number
        - Nationality
        - Expiry Date
        
        **4. Invoice**
        - Invoice Number
        - Vendor Name
        - Invoice Date
        - Total Amount
        
        #### Technology Stack
        - **Backend**: FastAPI
        - **OCR**: PaddleOCR
        - **LLM**: OpenAI API
        - **Database**: PostgreSQL + SQLAlchemy
        - **Frontend**: Streamlit
        - **Logging**: Loguru
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Backend", "FastAPI")
    with col2:
        st.metric("Database", "PostgreSQL")
    with col3:
        st.metric("OCR Engine", "PaddleOCR")


def main():
    """Main Streamlit application."""
    load_css()

    # Sidebar
    st.sidebar.title("📄 Document Extractor")
    st.sidebar.markdown("---")

    # API status check
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api/v1', '')}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✓ API Connected")
        else:
            st.sidebar.error("✗ API Unavailable")
    except:
        st.sidebar.error("✗ API Offline")

    st.sidebar.markdown("---")

    # Initialize session state
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    # Tab selection
    tab1, tab2, tab3 = st.tabs(
        ["📤 Upload Document", "📚 History", "ℹ️ About"]
    )

    with tab1:
        upload_document_tab()

    with tab2:
        documents_history_tab()

    with tab3:
        about_tab()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; font-size: 0.8em; color: gray;'>
            <p>Document Extraction Platform v1.0</p>
            <p>Built with ❤️ using FastAPI & Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
