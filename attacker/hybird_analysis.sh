#!/bin/bash

# Check if argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 directory"
  exit 1
fi

# Check if provided argument is a directory
if [ ! -d "$1" ]; then
  echo "$1 is not a directory"
  exit 1
fi

sha256=
jobid=
# Loop through each file in the directory
for file in "$1"/*
do
  echo $file
  file_path="$file"
  http_status=$(curl -X 'POST' \
    'https://hybrid-analysis.com/api/v2/submit/file' \
    -H 'accept: application/json' \
    -H 'user-agent: Falcon Sandbox' \
    -H 'Content-Type: multipart/form-data' \
    -H 'api-key: zgkyhntfe9b7d81ct1gudndn4973f4f8dehynvey095a6abdabqaoqco9edd39ad' \
    -F "file=@${file_path}" \
    -F 'environment_id=160' \
    -o response.json)

    sha256=$(jq -r '.sha256' response.json)
    jobid=$(jq -r '.job_id' response.json)

    echo $sha256
    echo $jobid
    echo $file "https://hybrid-analysis.com/sample/${sha256}/${jobid}"

done
