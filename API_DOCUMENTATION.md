# 📡 API Documentation

Complete API reference for the Premier League Match Prediction API.

---

## Base URL

```
http://localhost:8000
```

For production deployments, replace with your actual domain.

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
   - [Root](#root)
   - [API Info](#api-info)
   - [Health Check](#health-check)
   - [Get Teams](#get-teams)
   - [Predict Match](#predict-match)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)

---

## Overview

The Premier League Match Prediction API is built with **FastAPI** and provides endpoints for:
- Predicting match outcomes
- Retrieving available teams
- Health monitoring
- Interactive documentation

### Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Authentication

Currently, the API does not require authentication. For production deployments, consider implementing:
- API Key authentication
- OAuth2
- JWT tokens

---

## Endpoints

### Root

**GET** `/`

Returns the web interface for making predictions.

#### Response
- **Type**: HTML page
- **Description**: Interactive web UI for match predictions

#### Example
```bash
curl http://localhost:8000/
```

---

### API Info

**GET** `/api`

Returns basic API information and available endpoints.

#### Response

```json
{
  "message": "Premier League Match Prediction API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "predict": "/predict",
    "teams": "/teams",
    "docs": "/docs"
  }
}
```

#### Example

**cURL:**
```bash
curl http://localhost:8000/api
```

**Python:**
```python
import requests

response = requests.get("http://localhost:8000/api")
print(response.json())
```

---

### Health Check

**GET** `/health`

Check the health status of the API and verify that the model and preprocessor are loaded.

#### Response Model

```json
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true,
  "timestamp": "2025-01-15T10:30:00.123456"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Health status: "healthy" or "unhealthy" |
| `model_loaded` | boolean | Whether the ML model is loaded |
| `preprocessor_loaded` | boolean | Whether the preprocessor is loaded |
| `timestamp` | string | ISO 8601 timestamp |

#### Status Codes

- **200 OK**: Service is healthy
- **503 Service Unavailable**: Service is unhealthy

#### Examples

**cURL:**
```bash
curl http://localhost:8000/health
```

**Python:**
```python
import requests

response = requests.get("http://localhost:8000/health")
health = response.json()

if health["status"] == "healthy":
    print("✅ API is ready!")
else:
    print("❌ API is not ready")
```

**Response (Success):**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true,
  "timestamp": "2025-01-15T10:30:00.123456"
}
```

**Response (Error):**
```json
{
  "status": "unhealthy",
  "model_loaded": false,
  "preprocessor_loaded": false,
  "timestamp": "2025-01-15T10:30:00.123456",
  "error": "Model file not found at saved_models/model.pkl"
}
```

---

### Get Teams

**GET** `/teams`

Retrieve a list of all teams available for prediction.

#### Response Model

```json
{
  "teams": ["Arsenal", "Chelsea", "Liverpool", "..."],
  "count": 20
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `teams` | array[string] | Sorted list of team names |
| `count` | integer | Total number of teams |

#### Status Codes

- **200 OK**: Successfully retrieved teams
- **503 Service Unavailable**: Preprocessor data not loaded
- **500 Internal Server Error**: Server error

#### Examples

**cURL:**
```bash
curl http://localhost:8000/teams
```

**Python:**
```python
import requests

response = requests.get("http://localhost:8000/teams")
data = response.json()

print(f"Available teams ({data['count']}):")
for team in data['teams']:
    print(f"  - {team}")
```

**Response:**
```json
{
  "teams": [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brentford",
    "Brighton",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Fulham",
    "Liverpool",
    "Luton Town",
    "Manchester City",
    "Manchester United",
    "Newcastle United",
    "Nottingham Forest",
    "Sheffield United",
    "Tottenham",
    "West Ham",
    "Wolves"
  ],
  "count": 19
}
```

---

### Predict Match

**POST** `/predict`

Predict the outcome of a Premier League match.

#### Request Body

```json
{
  "home_team": "Arsenal",
  "away_team": "Chelsea",
  "match_date": "2025-01-15"
}
```

#### Request Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `home_team` | string | ✅ Yes | Name of the home team | "Arsenal" |
| `away_team` | string | ✅ Yes | Name of the away team | "Chelsea" |
| `match_date` | string | ✅ Yes | Match date (YYYY-MM-DD) | "2025-01-15" |

#### Validation Rules

- **home_team**: Cannot be empty, must be a valid team name
- **away_team**: Cannot be empty, must be a valid team name
- **match_date**: Must be in `YYYY-MM-DD` format

#### Response Model

```json
{
  "home_team": "Arsenal",
  "away_team": "Chelsea",
  "match_date": "2025-01-15",
  "prediction": "Home Win",
  "probabilities": {
    "Away Win": 0.25,
    "Draw": 0.30,
    "Home Win": 0.45
  },
  "confidence": 0.45
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `home_team` | string | Home team name (echoed from request) |
| `away_team` | string | Away team name (echoed from request) |
| `match_date` | string | Match date (echoed from request) |
| `prediction` | string | Predicted outcome: "Home Win", "Draw", or "Away Win" |
| `probabilities` | object | Probability for each outcome (0.0 to 1.0) |
| `confidence` | float | Confidence score (highest probability) |

#### Status Codes

- **200 OK**: Prediction successful
- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: Prediction failed

#### Examples

**cURL:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "home_team": "Manchester City",
    "away_team": "Liverpool",
    "match_date": "2025-02-01"
  }'
```

**Python:**
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "home_team": "Manchester United",
    "away_team": "Tottenham",
    "match_date": "2025-03-10"
}

response = requests.post(url, json=data)
result = response.json()

print(f"🏠 {result['home_team']} vs {result['away_team']} 🛫")
print(f"📅 Date: {result['match_date']}")
print(f"🎯 Prediction: {result['prediction']}")
print(f"📊 Confidence: {result['confidence']:.1%}")
print("\nProbabilities:")
for outcome, prob in result['probabilities'].items():
    print(f"  {outcome}: {prob:.1%}")
```

**Response (Success):**
```json
{
  "home_team": "Manchester City",
  "away_team": "Liverpool",
  "match_date": "2025-02-01",
  "prediction": "Home Win",
  "probabilities": {
    "Away Win": 0.28,
    "Draw": 0.25,
    "Home Win": 0.47
  },
  "confidence": 0.47
}
```

**Response (Error - Invalid Date):**
```json
{
  "detail": [
    {
      "loc": ["body", "match_date"],
      "msg": "Date must be in YYYY-MM-DD format",
      "type": "value_error"
    }
  ]
}
```

**Response (Error - Insufficient Data):**
```json
{
  "detail": "Unable to prepare prediction data: Insufficient match history for team 'NewTeam'. Please ensure the teams have sufficient match history."
}
```

---

## Data Models

### MatchPredictionRequest

Request model for match predictions.

```python
{
  "home_team": str,      # Required, non-empty
  "away_team": str,      # Required, non-empty
  "match_date": str      # Required, format: YYYY-MM-DD
}
```

**Validation:**
- Team names cannot be empty
- Date must be valid and in YYYY-MM-DD format

### PredictionResult

Response model for predictions.

```python
{
  "home_team": str,
  "away_team": str,
  "match_date": str,
  "prediction": str,              # "Home Win", "Draw", or "Away Win"
  "probabilities": {
    "Away Win": float,            # 0.0 to 1.0
    "Draw": float,                # 0.0 to 1.0
    "Home Win": float             # 0.0 to 1.0
  },
  "confidence": float             # 0.0 to 1.0 (max probability)
}
```

### HealthResponse

Response model for health checks.

```python
{
  "status": str,                  # "healthy" or "unhealthy"
  "model_loaded": bool,
  "preprocessor_loaded": bool,
  "timestamp": str                # ISO 8601 format
}
```

---

## Error Handling

The API uses standard HTTP status codes and returns detailed error messages.

### Common Error Responses

#### 400 Bad Request

Invalid input data or validation error.

```json
{
  "detail": "Date must be in YYYY-MM-DD format"
}
```

#### 404 Not Found

Endpoint does not exist.

```json
{
  "detail": "Not Found"
}
```

#### 500 Internal Server Error

Server-side error during processing.

```json
{
  "detail": "Prediction failed: Model not loaded",
  "error": "FileNotFoundError: Model file not found"
}
```

#### 503 Service Unavailable

Service is temporarily unavailable.

```json
{
  "status": "unhealthy",
  "model_loaded": false,
  "preprocessor_loaded": false,
  "timestamp": "2025-01-15T10:30:00.123456",
  "error": "Preprocessor data not loaded"
}
```

### Error Handling Best Practices

1. **Check health endpoint** before making predictions
2. **Validate input** on client side before sending requests
3. **Handle errors gracefully** with appropriate user feedback
4. **Retry logic** for transient errors (503)
5. **Log errors** for debugging

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production deployments, consider:

- **Request throttling**: Limit requests per IP/API key
- **Concurrent request limits**: Prevent resource exhaustion
- **Usage quotas**: Daily/monthly limits per user

**Recommended libraries:**
- `slowapi` - Rate limiting for FastAPI
- `redis` - Distributed rate limiting

---

## CORS Configuration

The API currently allows all origins (`*`). For production:

```python
origins = [
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

Update the CORS middleware in `app.py` to restrict access.

---

## Example Integration

### JavaScript (Fetch API)

```javascript
async function predictMatch(homeTeam, awayTeam, matchDate) {
  const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      home_team: homeTeam,
      away_team: awayTeam,
      match_date: matchDate
    })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

// Usage
predictMatch('Arsenal', 'Chelsea', '2025-01-15')
  .then(result => console.log(result))
  .catch(error => console.error('Error:', error));
```

### Python (requests)

```python
import requests
from typing import Dict, Any

class EPLPredictionClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_teams(self) -> list:
        """Get available teams"""
        response = requests.get(f"{self.base_url}/teams")
        response.raise_for_status()
        return response.json()["teams"]
    
    def predict(self, home_team: str, away_team: str, 
                match_date: str) -> Dict[str, Any]:
        """Predict match outcome"""
        data = {
            "home_team": home_team,
            "away_team": away_team,
            "match_date": match_date
        }
        response = requests.post(f"{self.base_url}/predict", json=data)
        response.raise_for_status()
        return response.json()

# Usage
client = EPLPredictionClient()

# Check health
health = client.health_check()
print(f"API Status: {health['status']}")

# Get teams
teams = client.get_teams()
print(f"Available teams: {len(teams)}")

# Make prediction
result = client.predict("Arsenal", "Chelsea", "2025-01-15")
print(f"Prediction: {result['prediction']} ({result['confidence']:.1%})")
```

---

## Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Get teams
curl http://localhost:8000/teams

# Predict match
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"home_team":"Arsenal","away_team":"Chelsea","match_date":"2025-01-15"}'
```

### Using HTTPie

```bash
# Install httpie
pip install httpie

# Health check
http GET localhost:8000/health

# Get teams
http GET localhost:8000/teams

# Predict match
http POST localhost:8000/predict \
  home_team="Arsenal" \
  away_team="Chelsea" \
  match_date="2025-01-15"
```

---

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/aniq63/Premier-League-Match-Prediction-ML/issues)
- Check the [main documentation](README.md)
- Review the [interactive API docs](http://localhost:8000/docs)

---

**Last Updated**: December 2025
