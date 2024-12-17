# Cloudflare IP Updater

This Python application automatically updates all A records in your Cloudflare DNS whenever your external IP address changes. It runs on an hourly schedule and is designed to run inside a Docker container.

## Features
- Detects external IP changes.
- Updates all A records dynamically via the Cloudflare API.
- Maintains the proxy status of DNS records.
- Runs autonomously with configurable scheduling.

---

## Prerequisites

### 1. Python Dependencies
- Python 3.6 or later
- Required Python libraries: `requests`, `python-dotenv`

Install the dependencies with:
```bash
pip install -r requirements.txt
```

### 2. Cloudflare Account
- An API token with `Zone.DNS` permissions.
- The Zone ID for your Cloudflare DNS zone.

---

## Environment Configuration

### 1. Create a `.env` File
Create a file named `.env` in the project directory with the following content:

```env
# The API token for Cloudflare authentication
CLOUDFLARE_API_TOKEN=your_api_token_here

# The Zone ID of your Cloudflare DNS zone
CLOUDFLARE_ZONE_ID=your_zone_id_here

# (Optional) External IP lookup service URL
IP_LOOKUP_URL=https://api.ipify.org
```

Replace `your_api_token_here` and `your_zone_id_here` with your Cloudflare API token and Zone ID, respectively.

---

## Running the Application

### 1. Docker Setup

#### Create a `Dockerfile`
Use the following Dockerfile to containerize the application:

```Dockerfile
# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]
```

### 2. Build and Run the Container

#### Build the Image
```bash
docker build -t cloudflare-ip-updater .
```

#### Run the Container
```bash
docker run -d --name ip-updater --env-file .env cloudflare-ip-updater
```

---

## Logging
Logs are output to the console and include information about:
- External IP lookup.
- Cloudflare API calls.
- Successful updates and errors.

---

## Troubleshooting

### Common Errors:
1. **Environment Variables Not Found:**
   - Ensure your `.env` file exists and is correctly configured.
   - Verify the `.env` file is passed to Docker using `--env-file`.

2. **Failed External IP Lookup:**
   - Check the connectivity to the IP lookup URL (`IP_LOOKUP_URL`).

3. **Cloudflare API Errors:**
   - Ensure your API token has `Zone.DNS` permissions.
   - Verify the Zone ID is correct.

---

## Sample `.env` File

Here is an example `.env` file:

```env
CLOUDFLARE_API_TOKEN=example_api_token
CLOUDFLARE_ZONE_ID=example_zone_id
IP_LOOKUP_URL=https://api.ipify.org
```

