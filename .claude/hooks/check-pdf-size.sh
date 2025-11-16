#!/bin/bash
# PDF Size Check Hook for Claude Code
# Blocks Read operations on PDFs that exceed safe size limits

# Read JSON input from stdin
input=$(cat)

# Extract file_path from JSON
file_path=$(echo "$input" | grep -o '"file_path":"[^"]*"' | cut -d'"' -f4)

# Skip if not a file path (empty or missing)
if [ -z "$file_path" ]; then
  exit 0
fi

# Skip if file doesn't exist (let Read tool handle the error)
if [ ! -f "$file_path" ]; then
  exit 0
fi

# Only check PDF files
if [[ ! "$file_path" =~ \.pdf$ ]]; then
  exit 0
fi

# Get file size in MB
file_size_mb=$(stat -f%z "$file_path" | awk '{print $1/1024/1024}')

# Define size limits (in MB)
SAFE_LIMIT=1
WARN_LIMIT=5
DANGER_LIMIT=10

# Check against limits
if (( $(echo "$file_size_mb > $DANGER_LIMIT" | bc -l) )); then
  # BLOCK: File too large (>10MB)
  echo "❌ PDF TOO LARGE: $(basename "$file_path") is ${file_size_mb}MB (limit: ${DANGER_LIMIT}MB)" >&2
  echo "" >&2
  echo "CONTEXT WINDOW RISK: This file can destroy the conversation history." >&2
  echo "" >&2
  echo "Options:" >&2

  # Check if split pages exist
  pdf_basename=$(basename "$file_path" .pdf)
  split_dir="docs/split_pages/"
  if [ -d "$split_dir" ]; then
    echo "  1. Use split pages: ls -1 $split_dir*/page_*.pdf | head -5" >&2
  fi

  echo "  2. Read ONLY first page with limit parameter: Read(file_path='$file_path', limit=1)" >&2
  echo "  3. Split the PDF first: Use qpdf or similar tool" >&2
  echo "" >&2
  exit 1

elif (( $(echo "$file_size_mb > $WARN_LIMIT" | bc -l) )); then
  # WARN: File large (5-10MB) - suggest page limits
  echo "⚠️  WARNING: $(basename "$file_path") is ${file_size_mb}MB" >&2
  echo "   Recommend reading first 2-3 pages only to preserve context window" >&2
  echo "   Use: Read(file_path='$file_path', limit=2)" >&2
  echo "" >&2
  # Allow but warn
  exit 0

elif (( $(echo "$file_size_mb > $SAFE_LIMIT" | bc -l) )); then
  # INFO: File medium (1-5MB) - gentle reminder
  echo "ℹ️  INFO: $(basename "$file_path") is ${file_size_mb}MB" >&2
  echo "   Consider reading first 3 pages only: Read(file_path='$file_path', limit=3)" >&2
  echo "" >&2
  # Allow
  exit 0
fi

# < 1MB: Allow without warning
exit 0
