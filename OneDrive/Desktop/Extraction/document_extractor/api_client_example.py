"""
Example API client script for Document Extraction Platform.
Demonstrates how to interact with the API programmatically.
"""

import json
import time
from pathlib import Path

import requests


class DocumentExtractorClient:
    """Client for interacting with Document Extraction API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize client.

        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"

    def health_check(self) -> bool:
        """
        Check if API server is healthy.

        Returns:
            bool: True if server is healthy
        """
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False

    def upload_document(self, file_path: str) -> dict:
        """
        Upload and process a document.

        Args:
            file_path: Path to document file

        Returns:
            dict: Extraction result or error

        Raises:
            FileNotFoundError: If file doesn't exist
            requests.RequestException: If API call fails
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"Uploading document: {file_path.name}")

        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f)}
            response = requests.post(
                f"{self.api_base}/upload-document",
                files=files,
                timeout=120,
            )

        if response.status_code == 200:
            print("✓ Document processed successfully")
            return response.json()
        else:
            error_detail = response.json().get("detail", "Unknown error")
            print(f"✗ Error: {error_detail}")
            return {"error": error_detail}

    def get_documents(self, skip: int = 0, limit: int = 20) -> dict:
        """
        Get all processed documents.

        Args:
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            dict: List of documents
        """
        print(f"Fetching documents (skip={skip}, limit={limit})...")

        response = requests.get(
            f"{self.api_base}/documents",
            params={"skip": skip, "limit": limit},
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Retrieved {len(data['documents'])} documents")
            return data
        else:
            print(f"✗ Error: {response.json().get('detail')}")
            return {"error": response.json().get("detail")}

    def get_document(self, document_id: int) -> dict:
        """
        Get specific document with full details.

        Args:
            document_id: ID of document

        Returns:
            dict: Document details or error
        """
        print(f"Fetching document {document_id}...")

        response = requests.get(
            f"{self.api_base}/documents/{document_id}",
            timeout=30,
        )

        if response.status_code == 200:
            print(f"✓ Document retrieved")
            return response.json()
        else:
            print(f"✗ Error: {response.json().get('detail')}")
            return {"error": response.json().get("detail")}

    def display_document(self, doc: dict):
        """
        Display document information nicely.

        Args:
            doc: Document dictionary
        """
        if "error" in doc:
            print(f"Error: {doc['error']}")
            return

        print("\n" + "=" * 60)
        print("DOCUMENT DETAILS")
        print("=" * 60)
        print(f"ID: {doc.get('id')}")
        print(f"Filename: {doc.get('original_filename')}")
        print(f"Type: {doc.get('document_type')}")
        print(f"Confidence: {doc.get('confidence_score')}")
        print(f"Created: {doc.get('created_at')}")

        if "extracted_data" in doc:
            print("\nEXTRACTED FIELDS:")
            print("-" * 60)
            for key, value in doc["extracted_data"].items():
                print(f"  {key}: {value}")

        if "raw_text" in doc:
            print("\nRAW OCR TEXT (first 200 chars):")
            print("-" * 60)
            text = doc["raw_text"][:200]
            print(text + "..." if len(doc["raw_text"]) > 200 else text)

        print("=" * 60 + "\n")


def main():
    """Example usage of the API client."""
    print("Document Extraction Platform - API Client Example")
    print("=" * 60)

    # Initialize client
    client = DocumentExtractorClient()

    # Check server health
    print("\n1. Checking server health...")
    if not client.health_check():
        print(
            "✗ API server is not running. "
            "Start it with: uvicorn app.main:app --reload"
        )
        return

    print("✓ API server is running")

    # Get existing documents
    print("\n2. Fetching existing documents...")
    docs_response = client.get_documents(limit=5)
    if "error" not in docs_response:
        print(f"Found {docs_response['total']} total documents")
        if docs_response["documents"]:
            first_doc_id = docs_response["documents"][0]["id"]
            print(f"First document ID: {first_doc_id}")

    # Example: Upload a document
    print("\n3. Example: To upload a document...")
    print("   result = client.upload_document('path/to/document.pdf')")
    print("   client.display_document(result)")

    # Example: Get document details
    print("\n4. Example: To get document details...")
    print("   result = client.get_document(1)")
    print("   client.display_document(result)")

    print("\n" + "=" * 60)
    print("API Client Examples:")
    print("=" * 60)

    print("""
# Upload a document
result = client.upload_document("invoices/sample.pdf")
if "error" not in result:
    document_id = result["id"]
    print(f"Document ID: {document_id}")
    client.display_document(result)

# Get all documents
documents = client.get_documents(skip=0, limit=20)
for doc in documents["documents"]:
    print(f"  - {doc['original_filename']} ({doc['document_type']})")

# Get specific document
doc_details = client.get_document(1)
client.display_document(doc_details)
""")


if __name__ == "__main__":
    main()
