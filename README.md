# Plant Health End-to-End System

This project is an end-to-end system for analyzing plant health using AWS services and Twilio. The system allows users to upload plant images, analyze them for diseases, and receive notifications via MMS. The analysis results are stored in DynamoDB and displayed in a Streamlit UI.

## Features
- **Image Upload**: Users can upload plant images to an S3 bucket.
- **Automated Analysis**: A Lambda function is triggered upon image upload to analyze the plant's health using Amazon Bedrock.
- **Data Storage**: Analysis results are stored in a DynamoDB table.
- **MMS Notifications**: If the plant is unhealthy, an MMS with the analysis details and image is sent to a specified mobile number using Twilio.
- **Streamlit UI**: Displays the latest uploaded image and its analysis details.

---

## Architecture Overview
1. **S3 Bucket**:
   - Stores uploaded plant images.
   - Triggers the Lambda function upon image upload.

2. **Lambda Function**:
   - Invoked by the S3 event.
   - Analyzes the image using Amazon Bedrock.
   - Stores the analysis results in DynamoDB.
   - Sends an MMS notification via Twilio if the plant is unhealthy.

3. **DynamoDB**:
   - Stores the analysis results, including health status, detected diseases, and recommendations.

4. **Twilio**:
   - Sends MMS notifications with the analysis details and image.

5. **Streamlit UI**:
   - Allows users to upload images.
   - Displays the latest analysis results and image.

---

## Prerequisites
1. **AWS Services**:
   - S3 bucket for storing images.
   - Lambda function with the necessary permissions.
   - DynamoDB table (`PlantHealthAlerts`) for storing analysis results.
   - Amazon Bedrock for image analysis.

2. **Twilio Account**:
   - Twilio credentials (`Account SID`, `Auth Token`, `Twilio Number`).
   - A verified mobile number for receiving MMS (if using a trial account).

3. **Environment Variables**:
   - Set the following environment variables in your Lambda function and Streamlit app:
     ```plaintext
     TWILIO_SID=<your-twilio-account-sid>
     TWILIO_TOKEN=<your-twilio-auth-token>
     TWILIO_NUMBER=<your-twilio-phone-number>
     USER_MOBILE_NUMBER=<recipient-mobile-number>
     ```

---

## How It Works
1. **Image Upload**:
   - Users upload an image via the Streamlit UI.
   - The image is saved to the S3 bucket.

2. **Lambda Function**:
   - Triggered by the S3 event.
   - Analyzes the image using Amazon Bedrock.
   - Stores the analysis results in DynamoDB.
   - Sends an MMS notification via Twilio if the plant is unhealthy.

3. **Streamlit UI**:
   - Fetches the latest analysis results from DynamoDB.
   - Displays the latest uploaded image and its analysis details.

---

## Deployment Instructions

### 1. AWS Setup
- **S3 Bucket**:
  - Create an S3 bucket and enable public access for uploaded images.
- **DynamoDB Table**:
  - Create a DynamoDB table named `PlantHealthAlerts` with the following attributes:
    - `image_key` (Primary Key)
    - `result` (JSON object containing analysis details)
- **Lambda Function**:
  - Deploy the Lambda function with the provided code.
  - Add an S3 trigger for the bucket to invoke the Lambda function on image upload.
  - Ensure the Lambda function has permissions for S3, DynamoDB, and Amazon Bedrock.

### 2. Twilio Setup
- Create a Twilio account and obtain:
  - `Account SID`
  - `Auth Token`
  - Twilio phone number
- Verify the recipient's phone number if using a trial account.

### 3. Streamlit App
- Install dependencies:
  ```bash
  pip install streamlit boto3 python-dotenv
