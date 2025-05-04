# Copyright 2025 Amazon Inc

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Analyze wind forecast data from windguru.cz using a multi-layered analysis framework.

Usage:
python -m nova_act.samples.analyze_winguru [--spot_id <windguru_spot_id>] [--headless]
"""

import logging
import fire
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from nova_act import NovaAct

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class WindData(BaseModel):
    """Weather data for a specific time point"""
    date: str = Field(..., description="Date and time of the forecast")
    wind_speed: float = Field(..., description="Wind speed in knots")
    wind_gusts: float = Field(..., description="Wind gust speed in knots")
    wind_direction: str = Field(..., description="Wind direction (e.g., NE, SW)")
    temperature: float = Field(..., description="Temperature in Celsius")
    precipitation: Optional[float] = Field(None, description="Precipitation amount in mm")


class ForecastData(BaseModel):
    """Collection of forecast data points"""
    spot_name: str = Field(..., description="Name of the windguru spot")
    spot_id: str = Field(..., description="ID of the windguru spot")
    forecast_generated: str = Field(..., description="When the forecast was generated")
    data_points: List[WindData] = Field(..., description="Collection of forecast data points")


class ForecastAnalysis(BaseModel):
    """Analysis of the forecast data at multiple levels"""
    raw_data: ForecastData = Field(..., description="Raw forecast data")
    micro_patterns: List[str] = Field(..., description="Short-term patterns (next 24h)")
    meso_patterns: List[str] = Field(..., description="Medium-term patterns (24-72h)")
    macro_patterns: List[str] = Field(..., description="Long-term patterns (3+ days)")
    meta_analysis: str = Field(..., description="Overall analysis and recommendation")


def analyze_forecast(nova: NovaAct) -> ForecastAnalysis:
    """Extract and analyze forecast data from windguru"""
    logger.info("Extracting forecast data from page")
    
    # Extract basic spot information
    result = nova.act(
        "Extract the spot name, spot ID, and when the forecast was generated",
        schema={
            "type": "object",
            "properties": {
                "spot_name": {"type": "string"},
                "spot_id": {"type": "string"},
                "forecast_generated": {"type": "string"}
            },
            "required": ["spot_name", "spot_id", "forecast_generated"]
        }
    )
    
    if not result.matches_schema:
        logger.error(f"Failed to extract spot information: {result.parsed_response}")
        raise ValueError("Could not extract spot information")
    
    spot_info = result.parsed_response
    logger.info(f"Extracted spot info: {spot_info['spot_name']} (ID: {spot_info['spot_id']})")
    
    # Extract forecast data points
    logger.info("Extracting detailed forecast data points")
    result = nova.act(
        "Extract the forecast data for the next 7 days including date, wind speed, wind gusts, "
        "wind direction, temperature, and precipitation for each time point",
        schema={
            "type": "object",
            "properties": {
                "data_points": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string"},
                            "wind_speed": {"type": "number"},
                            "wind_gusts": {"type": "number"},
                            "wind_direction": {"type": "string"},
                            "temperature": {"type": "number"},
                            "precipitation": {"type": "number", "nullable": True}
                        },
                        "required": ["date", "wind_speed", "wind_gusts", "wind_direction", "temperature"]
                    }
                }
            },
            "required": ["data_points"]
        }
    )
    
    if not result.matches_schema:
        logger.error(f"Failed to extract forecast data points: {result.parsed_response}")
        raise ValueError("Could not extract forecast data points")
    
    data_points = result.parsed_response["data_points"]
    logger.info(f"Extracted {len(data_points)} forecast data points")
    
    # Combine into raw forecast data
    raw_data = ForecastData(
        spot_name=spot_info["spot_name"],
        spot_id=spot_info["spot_id"],
        forecast_generated=spot_info["forecast_generated"],
        data_points=data_points
    )
    
    # Analyze the data at different time scales
    logger.info("Analyzing forecast patterns")
    
    # Micro patterns (next 24h)
    result = nova.act(
        "Analyze the wind forecast for the next 24 hours. Identify micro patterns such as "
        "wind shifts, gusts, or temperature changes. Return a list of key observations.",
        schema={
            "type": "array",
            "items": {"type": "string"}
        }
    )
    micro_patterns = result.parsed_response if result.matches_schema else ["Failed to analyze micro patterns"]
    logger.info(f"Identified {len(micro_patterns)} micro patterns")
    
    # Meso patterns (24-72h)
    result = nova.act(
        "Analyze the wind forecast for the 24-72 hour period. Identify medium-term patterns "
        "such as weather system changes or day/night variations. Return a list of key observations.",
        schema={
            "type": "array",
            "items": {"type": "string"}
        }
    )
    meso_patterns = result.parsed_response if result.matches_schema else ["Failed to analyze meso patterns"]
    logger.info(f"Identified {len(meso_patterns)} meso patterns")
    
    # Macro patterns (3+ days)
    result = nova.act(
        "Analyze the wind forecast for the period beyond 72 hours. Identify long-term patterns "
        "such as weather system changes or seasonal trends. Return a list of key observations.",
        schema={
            "type": "array",
            "items": {"type": "string"}
        }
    )
    macro_patterns = result.parsed_response if result.matches_schema else ["Failed to analyze macro patterns"]
    logger.info(f"Identified {len(macro_patterns)} macro patterns")
    
    # Meta analysis
    result = nova.act(
        "Based on all the forecast data, provide an overall analysis and recommendation for "
        "wind-dependent activities (sailing, kiteboarding, etc.). Consider factors like wind trends, "
        "consistency, and optimal conditions.",
        schema={"type": "string"}
    )
    meta_analysis = result.parsed_response if result.matches_schema else "Failed to generate meta analysis"
    logger.info("Completed meta analysis")
    
    # Return the complete analysis
    return ForecastAnalysis(
        raw_data=raw_data,
        micro_patterns=micro_patterns,
        meso_patterns=meso_patterns,
        macro_patterns=macro_patterns,
        meta_analysis=meta_analysis
    )


def main(spot_id: str = "1207462", headless: bool = False) -> None:
    """Main function to analyze wind forecast from windguru.cz"""
    logger.info(f"Starting analysis for windguru spot ID: {spot_id}")
    
    # Initialize NovaAct with the specified spot ID
    with NovaAct(
        starting_page=f"https://www.windguru.cz/{spot_id}",
        headless=headless
    ) as nova:
        logger.info("NovaAct session initialized")
        
        try:
            # Handle any initial page elements like cookie banners
            nova.act("If there is a cookie banner or popup, close it")
            logger.info("Page prepared for analysis")
            
            # Perform the forecast analysis
            analysis = analyze_forecast(nova)
            
            # Display the analysis results
            print("\n===== WIND FORECAST ANALYSIS =====\n")
            print(f"Spot: {analysis.raw_data.spot_name} (ID: {analysis.raw_data.spot_id})")
            print(f"Forecast generated: {analysis.raw_data.forecast_generated}")
            print(f"Data points analyzed: {len(analysis.raw_data.data_points)}")
            
            print("\n----- NEXT 24 HOURS (MICRO PATTERNS) -----")
            for pattern in analysis.micro_patterns:
                print(f"• {pattern}")
                
            print("\n----- 24-72 HOURS (MESO PATTERNS) -----")
            for pattern in analysis.meso_patterns:
                print(f"• {pattern}")
                
            print("\n----- 3+ DAYS (MACRO PATTERNS) -----")
            for pattern in analysis.macro_patterns:
                print(f"• {pattern}")
                
            print("\n----- OVERALL RECOMMENDATION -----")
            print(analysis.meta_analysis)
            print("\n====================================\n")
            
            logger.info("Analysis complete and results displayed")
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}", exc_info=True)
            print(f"\nAn error occurred during analysis: {str(e)}")
            
            # Provide more specific error information
            if "timeout" in str(e).lower():
                print("Timeout error: The page took too long to load or an operation timed out.")
                print("Consider checking your internet connection or increasing timeouts.")
            elif "network" in str(e).lower():
                print("Network error: There might be an issue with your connection or the website.")
            elif "schema" in str(e).lower():
                print("Schema error: The data extracted from the page did not match the expected format.")
            else:
                print("Unexpected error. Check the log for details.")


if __name__ == "__main__":
    fire.Fire(main)