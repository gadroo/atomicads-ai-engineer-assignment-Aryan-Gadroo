#!/bin/bash

# Create output directory if it doesn't exist
mkdir -p campaign_outputs

# Get timestamp for filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Run the query and save output to a file
./run_query.sh "$1" 2>&1 | tee "campaign_outputs/campaign_output_${TIMESTAMP}.md"

# Add markdown formatting to the output file
echo -e "\n# Campaign Generation Output\n" | cat - "campaign_outputs/campaign_output_${TIMESTAMP}.md" > temp && mv temp "campaign_outputs/campaign_output_${TIMESTAMP}.md"

echo "Output saved to: campaign_outputs/campaign_output_${TIMESTAMP}.md" 