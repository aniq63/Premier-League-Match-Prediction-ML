from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pydantic import BaseModel, Field, validator
import pickle
import os
from datetime import datetime
from typing import Optional, Dict, List
import logging
from src.utils.prediction_preprocessor import EPLMatchPredictorPreprocessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Premier League Match Prediction API",
    description="API for predicting Premier League match outcomes using machine learning",
    version="1.0.0"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configure CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to cache the model
_cached_model = None
_cached_preprocessor = None


def get_model_path():
    """Get the path to the trained model"""
    model_path = os.path.join('saved_models', 'model.pkl')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    return model_path


def load_model():
    """Load the trained model with caching"""
    global _cached_model
    
    if _cached_model is not None:
        logger.info("Using cached model")
        return _cached_model
    
    try:
        model_path = get_model_path()
        logger.info(f"Loading model from {model_path}")
        
        with open(model_path, 'rb') as file:
            _cached_model = pickle.load(file)
        
        logger.info("Model loaded successfully")
        return _cached_model
    
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load model: {str(e)}"
        )


def get_preprocessor():
    """Get or create the preprocessor with caching"""
    global _cached_preprocessor
    
    if _cached_preprocessor is not None:
        return _cached_preprocessor
    
    try:
        # Initialize preprocessor with historical seasons for data
        _cached_preprocessor = EPLMatchPredictorPreprocessor(
            seasons=['2025']
        )
        _cached_preprocessor.load_data()
        logger.info("Preprocessor initialized and data loaded")
        return _cached_preprocessor
    
    except Exception as e:
        logger.error(f"Error initializing preprocessor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize preprocessor: {str(e)}"
        )


# Pydantic models for request/response
class MatchPredictionRequest(BaseModel):
    home_team: str = Field(..., description="Name of the home team", example="Arsenal")
    away_team: str = Field(..., description="Name of the away team", example="Chelsea")
    match_date: str = Field(..., description="Match date in YYYY-MM-DD format", example="2025-01-15")
    
    @validator('match_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    @validator('home_team', 'away_team')
    def validate_team_names(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Team name cannot be empty')
        return v.strip()


class PredictionResult(BaseModel):
    home_team: str
    away_team: str
    match_date: str
    prediction: str
    probabilities: Dict[str, float]
    confidence: float
    
    class Config:
        schema_extra = {
            "example": {
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
        }


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    preprocessor_loaded: bool
    timestamp: str


# API Endpoints
@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root(request: Request):
    """Root endpoint - serves the prediction UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api", tags=["API Info"])
async def api_info():
    """API information endpoint"""
    return {
        "message": "Premier League Match Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "teams": "/teams",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify API and model status"""
    try:
        model = load_model()
        preprocessor = get_preprocessor()
        
        return HealthResponse(
            status="healthy",
            model_loaded=model is not None,
            preprocessor_loaded=preprocessor is not None,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "model_loaded": False,
                "preprocessor_loaded": False,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
        )


@app.post("/predict", response_model=PredictionResult, tags=["Prediction"])
async def predict_match(data: MatchPredictionRequest):
    """
    Predict the outcome of a Premier League match
    
    Returns probabilities for three outcomes:
    - Home Win
    - Draw
    - Away Win
    """
    try:
        logger.info(f"Prediction request: {data.home_team} vs {data.away_team} on {data.match_date}")
        
        # Load model
        model = load_model()
        
        # Get preprocessor
        preprocessor = get_preprocessor()
        
        # Prepare prediction data
        try:
            df = preprocessor.make_prediction_row(
                home_team=data.home_team,
                away_team=data.away_team,
                match_date=data.match_date
            )
        except ValueError as e:
            logger.warning(f"Preprocessor error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unable to prepare prediction data: {str(e)}. Please ensure the teams have sufficient match history."
            )
        
        # Make prediction
        probabilities = model.predict_proba(df)[0]
        
        # Get class labels (assuming standard order: Away Win, Draw, Home Win)
        # Adjust based on your model's actual class order
        outcome_labels = ["Away Win", "Draw", "Home Win"]
        
        # Create probability dictionary
        prob_dict = {
            outcome_labels[i]: float(round(prob, 4))
            for i, prob in enumerate(probabilities)
        }
        
        # Determine prediction (highest probability)
        max_prob_idx = probabilities.argmax()
        prediction = outcome_labels[max_prob_idx]
        confidence = float(round(probabilities[max_prob_idx], 4))
        
        logger.info(f"Prediction: {prediction} with confidence {confidence}")
        
        result = PredictionResult(
            home_team=data.home_team,
            away_team=data.away_team,
            match_date=data.match_date,
            prediction=prediction,
            probabilities=prob_dict,
            confidence=confidence
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.get("/teams", tags=["Information"])
async def get_available_teams():
    """Get list of teams available for prediction (requires preprocessor to be loaded)"""
    try:
        preprocessor = get_preprocessor()
        
        if preprocessor.df is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Preprocessor data not loaded"
            )
        
        # Get unique teams
        home_teams = set(preprocessor.df['home_team'].unique())
        away_teams = set(preprocessor.df['away_team'].unique())
        all_teams = sorted(list(home_teams.union(away_teams)))
        
        return {
            "teams": all_teams,
            "count": len(all_teams)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching teams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch teams: {str(e)}"
        )


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "error": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



