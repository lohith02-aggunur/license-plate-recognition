#!/usr/bin/env bash

# Install Tesseract OCR (for Linux on Render)
apt-get update && apt-get install -y tesseract-ocr

# Install Python dependencies
pip install -r requirements.txt