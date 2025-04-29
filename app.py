import streamlit as st
import boto3
import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "plant-health-images")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "PlantHealthAlerts")

# Initialize AWS clients
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

st.title("Plant Disease Classifier")

# File uploader for plant images
uploaded_file = st.file_uploader("Upload a plant image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Upload to S3"):
        # Upload the file to S3
        try:
            file_key = uploaded_file.name  # Use the file name directly
            s3_client.put_object(
                Bucket=AWS_S3_BUCKET,
                Key=file_key,
                Body=uploaded_file.getvalue(),
                ContentType=uploaded_file.type,
            )
            st.success(f"File successfully uploaded to S3: {file_key}")

            # Fetch the latest entry from DynamoDB
            response = table.scan(Limit=1)  # Fetch the latest item
            if "Items" in response and len(response["Items"]) > 0:
                latest_entry = response["Items"][-1]  # Get the latest entry
                image_key = latest_entry["image_key"]
                result = latest_entry["result"]

                # Construct the public S3 URL for the image
                s3_url = f"https://{AWS_S3_BUCKET}.s3.amazonaws.com/{image_key}"

                # Display the latest image and analysis details
                st.subheader("Latest Analysis")
                st.image(s3_url, caption="Latest Uploaded Image", use_column_width=True)
                st.json(result)
            else:
                st.warning("No analysis data found in DynamoDB.")
        except Exception as e:
            st.error(f"Error uploading file or fetching data: {str(e)}")