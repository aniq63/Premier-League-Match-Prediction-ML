# ⚙️ Setup Guide

Complete setup and configuration guide for the Premier League Match Prediction ML project.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Dependencies Installation](#dependencies-installation)
4. [Database Configuration](#database-configuration)
5. [AWS Configuration (Optional)](#aws-configuration-optional)
6. [Running the ETL Pipeline](#running-the-etl-pipeline)
7. [Running the Training Pipeline](#running-the-training-pipeline)
8. [Starting the API Server](#starting-the-api-server)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 2GB free space
- **Internet Connection**: Required for data extraction

### Required Software

1. **Python 3.8+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation:
     ```bash
     python --version
     # or
     python3 --version
     ```

2. **pip** (Python package manager)
   - Usually comes with Python
   - Verify installation:
     ```bash
     pip --version
     ```

3. **MongoDB**
   - **Option 1**: Local installation
     - Download from [mongodb.com](https://www.mongodb.com/try/download/community)
     - Follow installation instructions for your OS
   
   - **Option 2**: MongoDB Atlas (Cloud)
     - Create free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
     - Create a cluster
     - Get connection string

4. **Git** (for cloning repository)
   - Download from [git-scm.com](https://git-scm.com/)

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aniq63/Premier-League-Match-Prediction-ML.git
cd Premier-League-Match-Prediction-ML
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Verify Virtual Environment

```bash
which python  # macOS/Linux
where python  # Windows
```

Should point to the virtual environment's Python.

---

## Dependencies Installation

### 1. Upgrade pip

```bash
pip install --upgrade pip
```

### 2. Install Project Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **Data Processing**: pandas, numpy, soccerdata
- **ML Libraries**: scikit-learn, imbalanced-learn
- **Web Framework**: fastapi, uvicorn, jinja2
- **Database**: pymongo
- **Cloud Storage**: boto3 (AWS S3)
- **Utilities**: PyYAML, dill, from_root

### 3. Install Package in Editable Mode

```bash
pip install -e .
```

This makes the `src` package importable throughout the project.

### 4. Verify Installation

```bash
python -c "import fastapi; import sklearn; import pandas; print('✅ All dependencies installed!')"
```

---

## Database Configuration

### Option 1: Local MongoDB

#### Start MongoDB Service

**Windows:**
```bash
# If installed as service
net start MongoDB

# Or run manually
mongod --dbpath C:\data\db
```

**macOS:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

#### Verify MongoDB is Running

```bash
mongosh
# or
mongo
```

You should see the MongoDB shell.

#### Configure Connection

Edit `src/configuration/mongo_db_connection.py`:

```python
MONGO_DB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "epl_prediction"
COLLECTION_NAME = "matches"
```

### Option 2: MongoDB Atlas (Cloud)

#### Get Connection String

1. Log in to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string

#### Set Environment Variable

**Windows:**
```bash
set MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/epl_prediction
```

**macOS/Linux:**
```bash
export MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/epl_prediction"
```

Or create a `.env` file:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/epl_prediction
```

#### Update Configuration

Edit `src/configuration/mongo_db_connection.py`:

```python
import os

MONGO_DB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "epl_prediction"
COLLECTION_NAME = "matches"
```

---

## AWS Configuration (Optional)

If you want to store models in AWS S3:

### 1. Create AWS Account

Sign up at [aws.amazon.com](https://aws.amazon.com/)

### 2. Create IAM User

1. Go to IAM Console
2. Create new user with programmatic access
3. Attach policy: `AmazonS3FullAccess`
4. Save Access Key ID and Secret Access Key

### 3. Configure AWS Credentials

**Option 1: AWS CLI**
```bash
pip install awscli
aws configure
```

**Option 2: Environment Variables**
```bash
# Windows
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_REGION=us-east-1

# macOS/Linux
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-east-1
```

**Option 3: .env File**
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=epl-prediction-models
```

### 4. Create S3 Bucket

```bash
aws s3 mb s3://epl-prediction-models
```

### 5. Update Configuration

Edit `src/configuration/aws_connection.py` with your bucket name.

---

## Running the ETL Pipeline

The ETL pipeline extracts Premier League data and loads it into MongoDB.

### 1. Create ETL Script

Create `run_etl.py`:

```python
from ETL.etl_pipeline import ETLPipeline
from src.logger import logging

if __name__ == "__main__":
    try:
        # Specify seasons to extract
        seasons = [2021, 2022, 2023, 2024, 2025]
        
        logging.info(f"Starting ETL pipeline for seasons: {seasons}")
        pipeline = ETLPipeline(seasons=seasons)
        result = pipeline.run()
        
        logging.info("ETL pipeline completed successfully!")
        print("✅ Data loaded to MongoDB")
        
    except Exception as e:
        logging.error(f"ETL pipeline failed: {str(e)}")
        raise e
```

### 2. Run ETL Pipeline

```bash
python run_etl.py
```

**Expected Output:**
```
INFO - Starting ETL pipeline for seasons: [2021, 2022, 2023, 2024, 2025]
INFO - Extracting data for season 2021...
INFO - Transforming data...
INFO - Loading data to MongoDB...
...
INFO - ETL pipeline completed successfully!
✅ Data loaded to MongoDB
```

### 3. Verify Data in MongoDB

```bash
mongosh
```

```javascript
use epl_prediction
db.matches.countDocuments()  // Should show number of matches
db.matches.findOne()         // View a sample document
```

---

## Running the Training Pipeline

The training pipeline trains the ML model using data from MongoDB.

### 1. Verify Data is Loaded

Ensure ETL pipeline has run successfully and data exists in MongoDB.

### 2. Run Training Pipeline

**Option 1: Using demo.py**
```bash
python demo.py
```

**Option 2: Custom script**
```python
from src.pipline.training_pipeline import Training_Piepline
from src.logger import logging

if __name__ == "__main__":
    try:
        logging.info("Starting Training Pipeline")
        pipeline = Training_Piepline()
        pipeline.run_pipeline()
        logging.info("Training completed successfully!")
        
    except Exception as e:
        logging.error(f"Training failed: {str(e)}")
        raise e
```

### 3. Monitor Progress

The pipeline will run through 6 stages:

1. ✅ **Data Ingestion** - Fetch from MongoDB
2. ✅ **Data Validation** - Validate schema
3. ✅ **Data Transformation** - Feature engineering
4. ✅ **Model Training** - Train ML model
5. ✅ **Model Evaluation** - Evaluate performance
6. ✅ **Model Pusher** - Deploy to production

**Expected Output:**
```
================================================================================
Starting the Complete Training Pipeline
================================================================================

================================================================================
Step 1: Data Ingestion
================================================================================
INFO - Data Ingestion completed. Train file: artifact/.../train.csv

================================================================================
Step 2: Data Validation
================================================================================
INFO - Data Validation completed. Status: True

...

================================================================================
Step 6: Model Pusher
================================================================================
INFO - Model Pusher completed. Model pushed: True
INFO - Production model path: saved_models/model.pkl

================================================================================
Training Pipeline Completed Successfully!
================================================================================
```

### 4. Verify Model is Saved

```bash
ls saved_models/
# Should show: model.pkl
```

---

## Starting the API Server

### 1. Verify Model Exists

```bash
ls saved_models/model.pkl
```

If not, run the training pipeline first.

### 2. Start FastAPI Server

**Option 1: Using app.py**
```bash
python app.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. Access the Application

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 4. Test the API

**Using Browser:**
- Go to http://localhost:8000/docs
- Try the `/predict` endpoint

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "home_team": "Arsenal",
    "away_team": "Chelsea",
    "match_date": "2025-01-15"
  }'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "home_team": "Manchester City",
        "away_team": "Liverpool",
        "match_date": "2025-02-01"
    }
)

print(response.json())
```

---

## Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused
```

**Solution:**
- Ensure MongoDB is running: `mongod` or `brew services start mongodb-community`
- Check connection string in configuration
- Verify port 27017 is not blocked by firewall

#### 2. Model Not Found

**Error:**
```
FileNotFoundError: Model file not found at saved_models/model.pkl
```

**Solution:**
- Run the training pipeline first: `python demo.py`
- Verify `saved_models/` directory exists
- Check file permissions

#### 3. Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
- Install package in editable mode: `pip install -e .`
- Verify virtual environment is activated
- Check `setup.py` exists

#### 4. Dependency Conflicts

**Error:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solution:**
- Create fresh virtual environment
- Install dependencies one by one
- Check for version conflicts in `requirements.txt`

#### 5. soccerdata Extraction Fails

**Error:**
```
HTTPError: 403 Forbidden
```

**Solution:**
- Check internet connection
- Try again later (rate limiting)
- Use VPN if blocked in your region

#### 6. Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
- Kill process using port 8000:
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  
  # macOS/Linux
  lsof -ti:8000 | xargs kill -9
  ```
- Or use different port: `uvicorn app:app --port 8001`

#### 7. Insufficient Data for Prediction

**Error:**
```
ValueError: Insufficient match history for team 'NewTeam'
```

**Solution:**
- Ensure team exists in database
- Run ETL pipeline for more seasons
- Check team name spelling (case-sensitive)

---

## Environment Variables Reference

Create a `.env` file in project root:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=epl_prediction
COLLECTION_NAME=matches

# AWS Configuration (Optional)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=epl-prediction-models

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Model Configuration
MODEL_PATH=saved_models/model.pkl
MODEL_ACCEPTANCE_THRESHOLD=0.50
```

---

## Next Steps

After successful setup:

1. ✅ **Explore the API**: Visit http://localhost:8000/docs
2. ✅ **Make Predictions**: Test with different teams and dates
3. ✅ **Review Logs**: Check `logs/` directory for detailed logs
4. ✅ **Customize**: Modify configurations, try different models
5. ✅ **Deploy**: Consider Docker deployment (see `Dockerfile`)

---

## Additional Resources

- **[README](README.md)**: Project overview
- **[API Documentation](API_DOCUMENTATION.md)**: Detailed API reference
- **[Architecture](ARCHITECTURE.md)**: System design and architecture
- **[Model Documentation](MODEL.md)**: Model details and performance

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review logs in `logs/` directory
3. Search existing [GitHub issues](https://github.com/aniq63/Premier-League-Match-Prediction-ML/issues)
4. Open a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version)

---

**Last Updated**: December 2025
