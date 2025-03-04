import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
import matplotlib.pyplot as plt

# Path to your service account JSON key file
key_file_path = './key.json'  # Update the path if necessary

# Initialize BigQuery client using the service account JSON key file
client = bigquery.Client.from_service_account_json(key_file_path)



# Query the table - here we select all rows
query = f"SELECT * FROM  `pdfemail-452505.nikhil25.nifty50` "

# Run the query and load the result into a Pandas DataFrame
df = client.query(query).to_dataframe()

# Display the resulting DataFrame
df['Date'] = pd.to_datetime(df['Date'])

# Step 2: Plot the Close Price Over Time
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], marker='o', linestyle='-', color='b')
plt.title('Stock Close Price Over Time')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.xticks(rotation=45)  # Rotate dates for better visibility
plt.tight_layout()

# Save the plot as a PDF file locally
pdf_file_path = '/tmp/stock_dashboard.pdf'
plt.savefig(pdf_file_path, format='pdf')

def upload_to_gcs(pdf_file_path, bucket_name, destination_blob_name):
    # Initialize Google Cloud Storage client
    storage_client = storage.Client.from_service_account_json(key_file_path)

    # Specify the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a blob (file object in GCS)
    blob = bucket.blob(destination_blob_name)

    # Upload the file to GCS
    blob.upload_from_filename(pdf_file_path)

    print(f"File uploaded to gs://{bucket_name}/{destination_blob_name}")

# Set your GCS bucket name and the destination file path in GCS
bucket_name = 'pdf_email'  # Replace with your actual bucket name
destination_blob_name = 'stock_dashboard/stock_dashboard.pdf'  # Define the file path in GCS

# Upload the file to GCS
upload_to_gcs(pdf_file_path, bucket_name, destination_blob_name)
