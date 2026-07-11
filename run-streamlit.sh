#!/bin/bash
echo "🚀 Starting Streamlit Dashboard..."
cd sentiment-pipeline
source venv/bin/activate
streamlit run simple_app.py
