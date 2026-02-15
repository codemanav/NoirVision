"""
NoirVision Backend API
FastAPI server with both Backboard AI analysis and TwelveLabs video processing.
"""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# TwelveLabs integration
from app.config import get_settings
from app.routers import videos

# Backboard AI integration
from app.models import AnalysisRequest, WitnessClaim, CredibilityReport
from app.backboard_agent import BackboardAnalyzer
from app.report_generator import ReportGenerator
from app.mock_data import (
    get_mock_video_analysis_supported,
    get_mock_video_analysis_contradicted,
    MOCK_CLAIM_SUPPORTED,
    MOCK_CLAIM_CONTRADICTED
)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate config on startup."""
    try:
        s = get_settings()
        s.require_s3()
        if not s.twelvelabs_mock:
            s.require_twelvelabs()
        logger.info("Config validated (TwelveLabs mock=%s)", s.twelvelabs_mock)
    except Exception as e:
        logger.warning("Config validation issue: %s", e)
    yield


# Initialize FastAPI app
app = FastAPI(
    title="NoirVision API",
    description="Forensic video analysis with TwelveLabs and Backboard AI credibility reporting",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include TwelveLabs video router
app.include_router(videos.router, prefix="/api", tags=["videos"])

# Initialize Backboard analyzer
try:
    analyzer = BackboardAnalyzer()
    logger.info("Backboard analyzer initialized")
except ValueError as e:
    logger.warning("Backboard analyzer not initialized: %s", e)
    analyzer = None


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "NoirVision API",
        "status": "operational",
        "message": "In the city of lies, trust the footage.",
        "version": "1.0.0",
        "features": {
            "twelvelabs": "Video processing and analysis",
            "backboard": "AI-powered credibility verification"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "backboard_configured": analyzer is not None,
        "twelvelabs_configured": not get_settings().twelvelabs_mock
    }


# ============================================================================
# BACKBOARD AI ENDPOINTS
# ============================================================================

@app.post("/analyze", response_model=dict)
async def analyze_claim(request: AnalysisRequest):
    """
    Analyze a witness claim against video evidence using Backboard AI.
    
    Args:
        request: AnalysisRequest containing claim and video analysis
        
    Returns:
        Dictionary with credibility report (both structured and formatted)
    """
    if not analyzer:
        raise HTTPException(
            status_code=500,
            detail="Backboard analyzer not configured. Set BACKBOARD_API_KEY in environment."
        )
    
    try:
        # Run analysis
        report = await analyzer.analyze_claim_vs_video(
            claim=request.claim,
            video_analysis=request.video_analysis
        )
        
        # Generate formatted report
        formatted_report = ReportGenerator.generate_report(report)
        
        return {
            "report": report.model_dump(),
            "formatted_report": formatted_report
        }
    
    except Exception as e:
        logger.error("Analysis failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/analyze/text", response_model=dict)
async def analyze_text_only(claim_text: str):
    """
    Quick analysis endpoint - just provide claim text, uses mock video.
    Useful for testing.
    
    Args:
        claim_text: The witness claim text
        
    Returns:
        Dictionary with credibility report
    """
    if not analyzer:
        raise HTTPException(
            status_code=500,
            detail="Backboard analyzer not configured. Set BACKBOARD_API_KEY in environment."
        )
    
    try:
        # Determine which mock video to use based on claim
        if "blue note" in claim_text.lower() or "jazz club" in claim_text.lower():
            video_analysis = get_mock_video_analysis_contradicted()
        else:
            video_analysis = get_mock_video_analysis_supported()
        
        # Create claim object
        claim = WitnessClaim(claim_text=claim_text)
        
        # Run analysis
        report = await analyzer.analyze_claim_vs_video(
            claim=claim,
            video_analysis=video_analysis
        )
        
        # Generate formatted report
        formatted_report = ReportGenerator.generate_report(report)
        
        return {
            "report": report.model_dump(),
            "formatted_report": formatted_report
        }
    
    except Exception as e:
        logger.error("Analysis failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/demo/supported")
async def demo_supported():
    """
    Demo endpoint: Shows a SUPPORTED claim scenario.
    """
    if not analyzer:
        raise HTTPException(
            status_code=500,
            detail="Backboard analyzer not configured. Set BACKBOARD_API_KEY in environment."
        )
    
    try:
        claim = WitnessClaim(claim_text=MOCK_CLAIM_SUPPORTED)
        video_analysis = get_mock_video_analysis_supported()
        
        report = await analyzer.analyze_claim_vs_video(claim, video_analysis)
        formatted_report = ReportGenerator.generate_report(report)
        
        return {
            "report": report.model_dump(),
            "formatted_report": formatted_report
        }
    
    except Exception as e:
        logger.error("Demo failed: %s", e, exc_info=True)
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Demo failed: {str(e)}"
        )


@app.get("/demo/contradicted")
async def demo_contradicted():
    """
    Demo endpoint: Shows a CONTRADICTED claim scenario.
    """
    if not analyzer:
        raise HTTPException(
            status_code=500,
            detail="Backboard analyzer not configured. Set BACKBOARD_API_KEY in environment."
        )
    
    try:
        claim = WitnessClaim(claim_text=MOCK_CLAIM_CONTRADICTED)
        video_analysis = get_mock_video_analysis_contradicted()
        
        report = await analyzer.analyze_claim_vs_video(claim, video_analysis)
        formatted_report = ReportGenerator.generate_report(report)
        
        return {
            "report": report.model_dump(),
            "formatted_report": formatted_report
        }
    
    except Exception as e:
        logger.error("Demo failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Demo failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug
    )
