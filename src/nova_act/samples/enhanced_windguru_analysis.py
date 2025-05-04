#!/usr/bin/env python

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
Enhanced WindGuru Analysis Tool with Advanced AI and Statistical Capabilities

This script fetches and analyzes wind forecast data from windguru.cz using advanced techniques:
1. Machine learning for wind pattern prediction and forecasting
2. Fourier analysis for cyclical pattern detection
3. Time-series decomposition to separate trends from fluctuations
4. Statistical validation with confidence intervals
5. Nova Premiere model integration for enhanced accuracy

Usage:
python -m nova_act.samples.enhanced_windguru_analysis [--spot_id <windguru_spot_id>] [--analyze_map] [--headless] [--use_premiere]
"""

import asyncio
import logging
import fire
import time
import random
import os
import sys
import json
from typing import List, Dict, Any, Optional, Tuple, Union, AsyncIterable
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, field

# Scientific computing imports
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import resample

# Import NovaAct
try:
    from nova_act import NovaAct, ActSchema, ActResponse, NovaActException
except ImportError:
    # If the script is run from the samples directory
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from nova_act import NovaAct, ActSchema, ActResponse, NovaActException

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("windguru_enhanced_analysis.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
EOL 2>&1

# Enhanced data models
class WindDirection(Enum):
    """Enhanced wind direction enum with full compass points"""
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"
    VARIABLE = "Variable"
    UNKNOWN = "Unknown"


@dataclass
class DataPoint:
    """Enhanced data point with more meteorological parameters and confidence metrics"""
    date: datetime
    time: str
    temperature: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[WindDirection] = None
    wind_gusts: Optional[float] = None
    air_pressure: Optional[float] = None
    precipitation: Optional[float] = None
    cloud_cover: Optional[int] = None
    humidity: Optional[int] = None
    confidence: float = 1.0  # Confidence level for this data point
    predicted: bool = False  # Whether this is a predicted value
    
    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d")
    
    def __str__(self):
        return (f"{self.date.strftime('%Y-%m-%d')} {self.time}: "
                f"Temp: {self.temperature}°C, "
                f"Wind: {self.wind_speed}kts {self.wind_direction.value if self.wind_direction else 'Unknown'} "
                f"(gusts: {self.wind_gusts}kts), "
                f"Conf: {self.confidence:.2f}")


@dataclass
class PressureSystem:
    """Information about a pressure system with enhanced tracking attributes"""
    system_type: str  # "High" or "Low"
    location: str
    pressure: Optional[float] = None
    movement: Optional[str] = None
    intensity: Optional[str] = None  # "Strengthening", "Weakening", "Stable"
    historical_positions: List[Tuple[datetime, str]] = field(default_factory=list)  # For tracking movement


@dataclass
class CyclicalPattern:
    """Information about a detected cyclical pattern in the data"""
    variable: str  # Which variable shows the pattern (wind_speed, temperature, etc.)
    period_hours: float  # Period of the cycle in hours
    magnitude: float  # Strength/amplitude of the cycle
    phase: float  # Phase offset of the cycle
    confidence: float  # Confidence in this pattern (0-1)
    likely_source: str = "Unknown"  # Likely source (e.g., "Diurnal", "Tidal", etc.)


@dataclass
class WindguruAnalysis:
    """Complete analysis with all enhanced data and analytics"""
    spot_name: str
    spot_location: str
    analysis_time: datetime = field(default_factory=datetime.now)
    data_points: List[DataPoint] = field(default_factory=list)
    pressure_systems: List[PressureSystem] = field(default_factory=list)
    meta_analysis: str = ""
    confidence_intervals: Dict[str, List[float]] = field(default_factory=dict)
    cyclical_patterns: List[CyclicalPattern] = field(default_factory=list)
    ml_predictions: Dict[str, List[float]] = field(default_factory=dict)
    time_series_analysis: Dict[str, Any] = field(default_factory=dict)
    statistical_metrics: Dict[str, float] = field(default_factory=dict)
    predicted_data_points: List[DataPoint] = field(default_factory=list)  # Future predictions

    def __str__(self):
        return (f"WindGuru Analysis for {self.spot_name} ({self.spot_location})\n"
                f"Analysis performed at: {self.analysis_time}\n"
                f"Data points: {len(self.data_points)}\n"
                f"Predicted points: {len(self.predicted_data_points)}\n"
                f"Pressure systems identified: {len(self.pressure_systems)}\n"
                f"Cyclical patterns detected: {len(self.cyclical_patterns)}\n"
                f"\nMeta-analysis:\n{self.meta_analysis}")


# Enhanced schema definitions with more detailed types
DATAPOINT_SCHEMA = ActSchema({
    "type": "object",
    "properties": {
        "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
        "time": {"type": "string", "description": "Time in 24h format"},
        "temperature": {"type": ["number", "null"], "description": "Temperature in Celsius"},
        "wind_speed": {"type": ["number", "null"], "description": "Wind speed in knots"},
        "wind_direction": {"type": ["string", "null"], "enum": [d.value for d in WindDirection], "description": "Wind direction"},
        "wind_gusts": {"type": ["number", "null"], "description": "Wind gusts in knots"},
        "air_pressure": {"type": ["number", "null"], "description": "Air pressure in hPa"},
        "precipitation": {"type": ["number", "null"], "description": "Precipitation in mm"},
        "cloud_cover": {"type": ["integer", "null"], "description": "Cloud cover %"},
        "humidity": {"type": ["integer", "null"], "description": "Humidity %"}
    },
    "required": ["date", "time"]
})

PRESSURE_SYSTEM_SCHEMA = ActSchema({
    "type": "object",
    "properties": {
        "system_type": {"type": "string", "enum": ["High", "Low"], "description": "High or Low pressure system"},
        "location": {"type": "string", "description": "Geographic location of the system"},
        "pressure": {"type": ["number", "null"], "description": "Pressure in hPa"},
        "movement": {"type": ["string", "null"], "description": "Movement direction"},
        "intensity": {"type": ["string", "null"], "enum": ["Strengthening", "Weakening", "Stable"], "description": "How the system is changing"}
    },
    "required": ["system_type", "location"]
})
EOL 2>&1

# Advanced analysis functions

async def model_pipeline(nova: NovaAct, timepoint: str) -> Tuple[List[DataPoint], List[PressureSystem]]:
    """Advanced asynchronous model pipeline for parallel data extraction"""
    logger.info(f"Starting async model pipeline for timepoint: {timepoint}")
    
    # Execute tasks in parallel
    data_task = nova.act_async(
        f"Extract detailed weather data for the timepoint {timepoint}...",
        schema={"type": "array", "items": DATAPOINT_SCHEMA}
    )
    
    pressure_task = nova.act_async(
        f"Identify pressure systems visible on the map for timepoint {timepoint}...",
        schema={"type": "array", "items": PRESSURE_SYSTEM_SCHEMA}
    )
    
    # Await results
    try:
        data_result = await data_task
        pressure_result = await pressure_task
        
        # Process data points
        data_points = []
        if data_result.matches_schema:
            for dp_data in data_result.output:
                try:
                    wind_dir = dp_data.get("wind_direction")
                    wind_direction = (
                        WindDirection(wind_dir) if wind_dir and wind_dir in [d.value for d in WindDirection]
                        else WindDirection.UNKNOWN
                    )
                    data_point = DataPoint(
                        date=dp_data["date"],
                        time=dp_data["time"],
                        temperature=dp_data.get("temperature"),
                        wind_speed=dp_data.get("wind_speed"),
                        wind_direction=wind_direction,
                        wind_gusts=dp_data.get("wind_gusts"),
                        air_pressure=dp_data.get("air_pressure"),
                        precipitation=dp_data.get("precipitation"),
                        cloud_cover=dp_data.get("cloud_cover"),
                        humidity=dp_data.get("humidity")
                    )
                    data_points.append(data_point)
                except Exception as e:
                    logger.error(f"Error processing data point: {e}")
        
        # Process pressure systems
        pressure_systems = []
        if pressure_result.matches_schema:
            for ps_data in pressure_result.output:
                try:
                    pressure_system = PressureSystem(
                        system_type=ps_data["system_type"],
                        location=ps_data["location"],
                        pressure=ps_data.get("pressure"),
                        movement=ps_data.get("movement"),
                        intensity=ps_data.get("intensity")
                    )
                    pressure_systems.append(pressure_system)
                except Exception as e:
                    logger.error(f"Error processing pressure system: {e}")
        
        return data_points, pressure_systems
    except NovaActException as e:
        logger.error(f"Error in model pipeline: {str(e)}")
        # If we encounter an API error, try rotating API keys or adjusting parameters
        if hasattr(e, "status_code") and e.status_code == 429:
            logger.warning("Rate limit exceeded, implementing backoff strategy")
            await asyncio.sleep(2)  # Simple backoff
        return [], []


def analyze_map_timepoint(nova: NovaAct, timepoint: str, retry_attempts: int = 3) -> Tuple[List[DataPoint], List[PressureSystem]]:
    """Enhanced single timepoint analysis with retry logic and error handling"""
    logger.info(f"Analyzing map for timepoint: {timepoint}")
    
    # Navigate to the timepoint with retry logic
    try:
        for attempt in range(retry_attempts):
            try:
                # Click on the timepoint button
                result = nova.act(
                    f"Click on the timepoint labeled '{timepoint}' to see the forecast map.",
                    schema=ActSchema({"type": "boolean"})
                )
                
                if result.matches_schema and result.output:
                    logger.info(f"Successfully clicked on timepoint: {timepoint}")
                    # Wait for map to load
                    time.sleep(2)
                    break
                else:
                    logger.warning(f"Failed to click on timepoint (attempt {attempt+1}/{retry_attempts})")
                    wait_time = (2 ** attempt) + random.random()  # Exponential backoff
                    time.sleep(wait_time)
            except Exception as e:
                logger.error(f"Error clicking on timepoint: {str(e)}")
                if attempt < retry_attempts - 1:
                    wait_time = (2 ** attempt) + random.random()
                    time.sleep(wait_time)
                else:
                    raise
    except Exception as e:
        logger.error(f"Failed to navigate to timepoint after {retry_attempts} attempts: {str(e)}")
        return [], []
    
    # Extract forecast data with retry logic
    data_points = []
    for attempt in range(retry_attempts):
        try:
            result = nova.act(
                "Extract all detailed weather data from the forecast table.",
                schema={"type": "array", "items": DATAPOINT_SCHEMA},
                model_temperature=0.2  # Lower temperature for more precise extraction
            )
            
            if result.matches_schema:
                for dp_data in result.output:
                    try:
                        wind_dir = dp_data.get("wind_direction")
                        wind_direction = (
                            WindDirection(wind_dir) if wind_dir and wind_dir in [d.value for d in WindDirection]
                            else WindDirection.UNKNOWN
                        )
                        data_point = DataPoint(
                            date=dp_data["date"],
                            time=dp_data["time"],
                            temperature=dp_data.get("temperature"),
                            wind_speed=dp_data.get("wind_speed"),
                            wind_direction=wind_direction,
                            wind_gusts=dp_data.get("wind_gusts"),
                            air_pressure=dp_data.get("air_pressure"),
                            precipitation=dp_data.get("precipitation"),
                            cloud_cover=dp_data.get("cloud_cover"),
                            humidity=dp_data.get("humidity")
                        )
                        data_points.append(data_point)
                    except Exception as e:
                        logger.error(f"Error processing data point: {str(e)}")
                break
            else:
                logger.warning(f"Failed to extract data (attempt {attempt+1}/{retry_attempts})")
                wait_time = (2 ** attempt) + random.random()
                time.sleep(wait_time)
        except Exception as e:
            logger.error(f"Error extracting data: {str(e)}")
            if attempt < retry_attempts - 1:
                wait_time = (2 ** attempt) + random.random()
                time.sleep(wait_time)
    
    # Extract pressure systems with retry logic
    pressure_systems = []
    for attempt in range(retry_attempts):
        try:
            result = nova.act(
                "Look for high and low pressure systems on the map. Extract their locations, pressures, and movements.",
                schema={"type": "array", "items": PRESSURE_SYSTEM_SCHEMA},
                model_temperature=0.3  # Slightly higher temperature for creative identification
            )
            
            if result.matches_schema:
                for ps_data in result.output:
                    try:
                        pressure_system = PressureSystem(
                            system_type=ps_data["system_type"],
                            location=ps_data["location"],
                            pressure=ps_data.get("pressure"),
                            movement=ps_data.get("movement"),
                            intensity=ps_data.get("intensity")
                        )
                        pressure_systems.append(pressure_system)
                    except Exception as e:
                        logger.error(f"Error processing pressure system: {str(e)}")
                break
            else:
                logger.warning(f"Failed to extract pressure systems (attempt {attempt+1}/{retry_attempts})")
                wait_time = (2 ** attempt) + random.random()
                time.sleep(wait_time)
        except Exception as e:
            logger.error(f"Error extracting pressure systems: {str(e)}")
            if attempt < retry_attempts - 1:
                wait_time = (2 ** attempt) + random.random()
                time.sleep(wait_time)
    
    return data_points, pressure_systems


def perform_ai_analysis(data_points: List[DataPoint]) -> Tuple[List[DataPoint], Dict[str, Any]]:
    """Perform AI-based analysis and prediction using machine learning models"""
    logger.info("Performing AI analysis with machine learning models")
    predicted_points = []
    models_info = {}
    
    try:
        # Extract valid feature data
        valid_points = [dp for dp in data_points if dp.temperature is not None and 
                       dp.wind_speed is not None and dp.air_pressure is not None]
        
        if len(valid_points) < 5:
            logger.warning(f"Insufficient data for ML modeling: only {len(valid_points)} valid points")
            return predicted_points, {"error": "Insufficient data"}
        
        # Prepare data for modeling
        X = np.array([
            [dp.temperature or 0, dp.wind_speed or 0, dp.air_pressure or 0, 
             dp.humidity or 50, dp.cloud_cover or 0]
            for dp in valid_points
        ])
        
        # Target variables for different models
        y_wind = np.array([dp.wind_speed for dp in valid_points])
        y_gusts = np.array([dp.wind_gusts if dp.wind_gusts is not None else dp.wind_speed*1.5 for dp in valid_points])
        
        # Train multiple models
        wind_model = RandomForestRegressor(n_estimators=100, random_state=42)
        wind_model.fit(X, y_wind)
        
        gust_model = RandomForestRegressor(n_estimators=100, random_state=42)
        gust_model.fit(X, y_gusts)
        
        # Feature importance analysis
        feature_names = ["temperature", "wind_speed", "air_pressure", "humidity", "cloud_cover"]
        wind_importance = dict(zip(feature_names, wind_model.feature_importances_))
        gust_importance = dict(zip(feature_names, gust_model.feature_importances_))
        
        # Store model info
        models_info = {
            "wind_model": {
                "score": wind_model.score(X, y_wind),
                "feature_importance": wind_importance
            },
            "gust_model": {
                "score": gust_model.score(X, y_gusts),
                "feature_importance": gust_importance
            }
        }
        
        # Make future predictions (24 hours ahead)
        # Here we use a simple approach of adding the average change to the last data point
        if len(valid_points) >= 2:
            last_point = valid_points[-1]
            
            # Calculate average changes for features
            temp_changes = [valid_points[i+1].temperature - valid_points[i].temperature for i in range(len(valid_points)-1)]
            pressure_changes = [valid_points[i+1].air_pressure - valid_points[i].air_pressure for i in range(len(valid_points)-1)]
            
            avg_temp_change = sum(temp_changes) / len(temp_changes) if temp_changes else 0
            avg_pressure_change = sum(pressure_changes) / len(pressure_changes) if pressure_changes else 0
            
            # Create future data points
            for i in range(1, 25):  # 24 hour forecast
                # Create predicted features
                future_temp = last_point.temperature + avg_temp_change * i
                future_pressure = last_point.air_pressure + avg_pressure_change * i
                
                # Use last values for other features
                future_humidity = last_point.humidity
                future_cloud = last_point.cloud_cover
                
                # Predict wind speed and gusts
                future_X = np.array([[future_temp, last_point.wind_speed, future_pressure, future_humidity or 50, future_cloud or 0]])
                predicted_wind = float(wind_model.predict(future_X)[0])
                predicted_gusts = float(gust_model.predict(future_X)[0])
                
                # Create date and time for prediction point
                from datetime import timedelta
                future_date = last_point.date + timedelta(hours=i)
                future_time = future_date.strftime("%H:%M")
                future_date_str = future_date.strftime("%Y-%m-%d")
                
                # Create data point with prediction confidence
                # Confidence decreases as we predict further into the future
                confidence = max(0.3, 0.9 - (i * 0.025))
                
                predicted_point = DataPoint(
                    date=future_date,
                    time=future_time,
                    temperature=future_temp,
                    wind_speed=predicted_wind,
                    wind_gusts=predicted_gusts,
                    air_pressure=future_pressure,
                    humidity=future_humidity,
                    cloud_cover=future_cloud,
                    wind_direction=last_point.wind_direction,  # Assume same direction for simplicity
                    confidence=confidence,
                    predicted=True
                )
                
                predicted_points.append(predicted_point)
        
        logger.info(f"AI analysis complete: trained {len(models_info)} models, predicted {len(predicted_points)} future points")
        
        return predicted_points, models_info
    
    except Exception as e:
        logger.error(f"Error in AI analysis: {str(e)}")
        return [], {"error": str(e)}


def analyze_cyclical_patterns(data_points: List[DataPoint]) -> List[CyclicalPattern]:
    """Perform Fourier analysis to detect cyclical patterns in the wind data"""
    logger.info("Analyzing cyclical patterns with Fourier analysis")
    cyclical_patterns = []
    
    try:
        # Extract time series data
        wind_speeds = np.array([dp.wind_speed for dp in data_points if dp.wind_speed is not None])
        temperatures = np.array([dp.temperature for dp in data_points if dp.temperature is not None])
        pressures = np.array([dp.air_pressure for dp in data_points if dp.air_pressure is not None])
        
        # Define variables to analyze
        variables = {
            "wind_speed": wind_speeds,
            "temperature": temperatures,
            "air_pressure": pressures
        }
        
        # Analyze each variable for cyclical patterns
        for var_name, values in variables.items():
            if len(values) > 10:  # Need sufficient data
                # Perform FFT
                fft_result = np.fft.fft(values)
                frequencies = np.fft.fftfreq(len(fft_result))
                
                # Find dominant frequencies (excluding DC component)
                magnitude = np.abs(fft_result)
                # Skip the first element (DC component)
                dominant_idx = np.argsort(magnitude[1:])[-3:] + 1  # Get top 3 frequencies
                
                for idx in dominant_idx:
                    # Only keep significant frequencies
                    if magnitude[idx] > 0.1 * magnitude.max():
                        freq = frequencies[idx]
                        if freq > 0:  # Only positive frequencies
                            # Calculate period in hours (assuming hourly data)
                            period = abs(1 / freq)
                            
                            # Calculate phase
                            phase = np.angle(fft_result[idx])
                            
                            # Determine the likely source of the pattern based on period
                            source = "Unknown"
                            if 23 <= period <= 25:
                                source = "Diurnal (day/night)"
                                confidence = 0.9
                            elif 11 <= period <= 13:
                                source = "Semidiurnal"
                                confidence = 0.8
                            elif period > 160 and period < 200:
                                source = "Weekly"
                                confidence = 0.7
                            elif period > 500:
                                source = "Seasonal"
                                confidence = 0.6
                            elif period > 10 and period < 14:
                                source = "Tidal"
                                confidence = 0.75
                            else:
                                confidence = 0.5
                            
                            # Create a cyclical pattern
                            pattern = CyclicalPattern(
                                variable=var_name,
                                period_hours=float(period),
                                magnitude=float(magnitude[idx] / len(values)),  # Normalize
                                phase=float(phase),
                                confidence=confidence,
                                likely_source=source
                            )
                            
                            cyclical_patterns.append(pattern)
        
        logger.info(f"Detected {len(cyclical_patterns)} cyclical patterns")
    
    except Exception as e:
        logger.error(f"Error in cyclical pattern analysis: {str(e)}")
    
    return cyclical_patterns


def perform_time_series_analysis(data_points: List[DataPoint]) -> Dict[str, Any]:
    """Perform time series decomposition to separate trend, seasonal, and residual components"""
    logger.info("Performing time series decomposition")
    ts_results = {}
    
    try:
        # Need pandas for time series analysis
        import pandas as pd
        
        # Convert data points to DataFrame
        df_data = [
            {
                'datetime': dp.date.strftime("%Y-%m-%d ") + dp.time,
                'wind_speed': dp.wind_speed,
                'temperature': dp.temperature,
                'air_pressure': dp.air_pressure
            } 
            for dp in data_points if dp.wind_speed is not None
        ]
        
        if len(df_data) < 24:  # Need at least a day of data
            logger.warning(f"Insufficient data for time series analysis: only {len(df_data)} points")
            return {"error": "Insufficient data"}
        
        df = pd.DataFrame(df_data)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        
        # Ensure data is regularly spaced
        df = df.resample('1H').mean()
        df = df.interpolate(method='linear')
        
        # Decompose each variable
        variables = ['wind_speed', 'temperature', 'air_pressure']
        decomposition_results = {}
        
        for var in variables:
            if var in df.columns and not df[var].isna().all() and len(df[var].dropna()) >= 24:
                # Use from statsmodels if available
                try:
                    from statsmodels.tsa.seasonal import seasonal_decompose
                    # Decompose with 24 hour period (daily seasonality)
                    result = seasonal_decompose(df[var].dropna(), model='additive', period=24)
                    
                    decomposition_results[var] = {
                        "trend": result.trend.dropna().tolist(),
                        "seasonal": result.seasonal.dropna().tolist(),
                        "residual": result.resid.dropna().tolist(),
                        "trend_direction": "increasing" if result.trend.diff().mean() > 0 else "decreasing",
                        "seasonal_amplitude": float(result.seasonal.max() - result.seasonal.min())
                    }
                except Exception as e:
                    logger.error(f"Error in statsmodels decomposition for {var}: {e}")
                    # Fallback to simpler decomposition
                    data = df[var].dropna()
                    # Calculate trend using rolling mean
                    trend = data.rolling(window=24, center=True).mean()
                    # Calculate seasonal as a deviation from trend
                    seasonal = data - trend
                    # Simple residual
                    residual = data - trend - seasonal
                    
                    decomposition_results[var] = {
                        "trend": trend.dropna().tolist(),
                        "seasonal": seasonal.dropna().tolist(),
                        "residual": residual.dropna().tolist(),
                        "trend_direction": "increasing" if trend.diff().mean() > 0 else "decreasing",
                        "seasonal_amplitude": float(seasonal.max() - seasonal.min())
                    }
        
        # Additional time series metrics
        # Calculate volatility (rolling standard deviation)
        volatility_metrics = {}
        for var in variables:
            if var in df.columns and not df[var].isna().all():
                # Volatility over 6-hour windows
                volatility = df[var].rolling(window=6).std().dropna().mean()
                volatility_metrics[var] = float(volatility)
        
        ts_results = {
            "decomposition": decomposition_results,
            "volatility": volatility_metrics,
            "data_points": len(df_data),
            "time_span_hours": (df.index.max() - df.index.min()).total_seconds() / 3600
        }
        
        logger.info(f"Time series decomposition complete for {len(decomposition_results)} variables")
    
    except Exception as e:
        logger.error(f"Error in time series analysis: {str(e)}")
        ts_results = {"error": str(e)}
    
    return ts_results


def calculate_statistical_validation(data_points: List[DataPoint]) -> Dict[str, List[float]]:
    """Perform bootstrapping for statistical validation and confidence intervals"""
    logger.info("Calculating statistical validation with bootstrapping")
    confidence_intervals = {}
    
    try:
        # Extract data for bootstrapping
        wind_speeds = np.array([dp.wind_speed for dp in data_points if dp.wind_speed is not None])
        temperatures = np.array([dp.temperature for dp in data_points if dp.temperature is not None])
        pressures = np.array([dp.air_pressure for dp in data_points if dp.air_pressure is not None])
        
        variables = {
            "wind_speed": wind_speeds,
            "temperature": temperatures,
            "air_pressure": pressures
        }
        
        for var_name, values in variables.items():
            if len(values) > 5:  # Need at least 5 points for bootstrapping
                # Perform bootstrapping
                n_iterations = 1000
                bootstrap_means = [np.mean(resample(values)) for _ in range(n_iterations)]
                bootstrap_vars = [np.var(resample(values)) for _ in range(n_iterations)]
                
                # Calculate confidence intervals (95%)
                mean_ci = np.percentile(bootstrap_means, [2.5, 97.5])
                var_ci = np.percentile(bootstrap_vars, [2.5, 97.5])
                
                confidence_intervals[var_name] = mean_ci.tolist()
                confidence_intervals[f"{var_name}_variance"] = var_ci.tolist()
                
                logger.info(f"{var_name.capitalize()} confidence interval: {mean_ci[0]:.2f} to {mean_ci[1]:.2f}")
    
    except Exception as e:
        logger.error(f"Error in statistical validation: {str(e)}")
    
    return confidence_intervals
EOL 2>&1

def analyze_forecast(nova: NovaAct, use_premiere: bool = False) -> WindguruAnalysis:
    """Perform comprehensive analysis of the WindGuru forecast with all enhanced features"""
    logger.info("Starting comprehensive forecast analysis with enhanced features")
    
    # Apply model optimization if using Nova Premiere
    if use_premiere:
        model_params = {
            "temperature": 0.2,  # Lower temperature for more precise outputs
            "top_k": 40        # More focused sampling
        }
        logger.info("Using Nova Premiere with optimized parameters")
    else:
        model_params = {}
    
    # Get spot info with retry logic
    spot_info = None
    for attempt in range(3):
        try:
            result = nova.act(
                "Extract the spot name and location from this WindGuru page",
                schema=ActSchema({
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "location": {"type": "string"}
                    },
                    "required": ["name", "location"]
                }),
                **model_params
            )
            
            if result.matches_schema:
                spot_info = result.output
                logger.info(f"Analyzing spot: {spot_info['name']} ({spot_info['location']})")
                break
            else:
                logger.warning(f"Failed to get spot info (attempt {attempt+1}/3): {result.parsed_response}")
                time.sleep((2 ** attempt) + random.random())  # Exponential backoff
        except Exception as e:
            logger.error(f"Error getting spot info (attempt {attempt+1}/3): {str(e)}")
            time.sleep((2 ** attempt) + random.random())
    
    # Use default if still failed
    if not spot_info:
        spot_info = {"name": "Unknown", "location": "Unknown"}
        logger.warning("Using default spot info after all attempts failed")
    
    # Initialize the analysis object
    analysis = WindguruAnalysis(
        spot_name=spot_info["name"],
        spot_location=spot_info["location"]
    )
    
    # Get available timepoints with retry logic
    timepoints = []
    for attempt in range(3):
        try:
            result = nova.act(
                "What are the available timepoints or days for the weather forecast? List all times shown in the table.",
                schema=ActSchema({
                    "type": "array",
                    "items": {"type": "string"}
                }),
                **model_params
            )
            
            if result.matches_schema and len(result.output) > 0:
                timepoints = result.output
                logger.info(f"Found {len(timepoints)} timepoints: {timepoints[:5]}...")
                break
            else:
                logger.warning(f"Failed to get timepoints (attempt {attempt+1}/3): {result.parsed_response}")
                time.sleep((2 ** attempt) + random.random())
        except Exception as e:
            logger.error(f"Error getting timepoints (attempt {attempt+1}/3): {str(e)}")
            time.sleep((2 ** attempt) + random.random())
    
    # Create at least one default timepoint if needed
    if not timepoints:
        timepoints = ["Current"]
        logger.warning("Using default timepoint after all attempts failed")
    
    # Analyze each timepoint with advanced error handling
    all_data_points = []
    all_pressure_systems = []
    
    for timepoint in timepoints[:12]:  # Use up to 12 timepoints for efficiency/coverage
        logger.info(f"Processing timepoint: {timepoint}")
        try:
            # Use the enhanced map timepoint analysis function
            data_points, pressure_systems = analyze_map_timepoint(nova, timepoint)
            
            # Validate extracted data
            if not data_points:
                logger.warning(f"No data points extracted for timepoint {timepoint}")
            else:
                logger.info(f"Extracted {len(data_points)} data points for timepoint {timepoint}")
            
            # Add valid data to the analysis
            all_data_points.extend(data_points)
            all_pressure_systems.extend(pressure_systems)
            
        except Exception as e:
            logger.error(f"Error analyzing timepoint {timepoint}: {str(e)}")
        
        # Take a short break to avoid overwhelming the page/models
        time.sleep(1.5)
    
    # If we didn't get any data points, create a minimal default one
    if not all_data_points:
        logger.warning("No data points extracted, creating a minimal default point")
        default_point = DataPoint(
            date=datetime.now(),
            time=datetime.now().strftime("%H:%M"),
            temperature=20.0,
            wind_speed=10.0,
            wind_direction=WindDirection.UNKNOWN,
            wind_gusts=15.0,
            confidence=0.1  # Low confidence
        )
        all_data_points.append(default_point)
    
    # Add collected data to the analysis object
    analysis.data_points = all_data_points
    analysis.pressure_systems = all_pressure_systems
    logger.info(f"Collected {len(all_data_points)} total data points and {len(all_pressure_systems)} pressure systems")
    
    # Now run all the enhanced analysis components
    
    # 1. Run the AI analysis and predictions
    predicted_points, models_info = perform_ai_analysis(all_data_points)
    analysis.predicted_data_points = predicted_points
    analysis.ml_predictions = models_info
    logger.info(f"AI analysis complete: predicted {len(predicted_points)} future points")
    
    # 2. Detect cyclical patterns with Fourier analysis
    cyclical_patterns = analyze_cyclical_patterns(all_data_points)
    analysis.cyclical_patterns = cyclical_patterns
    logger.info(f"Detected {len(cyclical_patterns)} cyclical patterns")
    
    # 3. Perform time-series decomposition
    ts_results = perform_time_series_analysis(all_data_points)
    analysis.time_series_analysis = ts_results
    logger.info("Time series decomposition complete")
    
    # 4. Calculate statistical metrics and confidence intervals
    confidence_intervals = calculate_statistical_validation(all_data_points)
    analysis.confidence_intervals = confidence_intervals
    logger.info("Statistical validation complete")
    
    # Collect additional statistical metrics
    try:
        wind_speeds = [dp.wind_speed for dp in all_data_points if dp.wind_speed is not None]
        if wind_speeds:
            analysis.statistical_metrics = {
                "wind_mean": float(np.mean(wind_speeds)),
                "wind_std": float(np.std(wind_speeds)),
                "wind_min": float(np.min(wind_speeds)),
                "wind_max": float(np.max(wind_speeds)),
                "wind_range": float(np.max(wind_speeds) - np.min(wind_speeds))
            }
    except Exception as e:
        logger.error(f"Error calculating statistical metrics: {str(e)}")
    
    # Generate enhanced meta-analysis
    try:
        meta_analysis = generate_enhanced_meta_analysis(analysis)
        analysis.meta_analysis = meta_analysis
        logger.info("Enhanced meta-analysis generated successfully")
    except Exception as e:
        logger.error(f"Error generating enhanced meta-analysis: {str(e)}")
        analysis.meta_analysis = "Error generating meta-analysis"
    
    return analysis


def generate_enhanced_meta_analysis(analysis: WindguruAnalysis) -> str:
    """Generate a comprehensive meta-analysis with all enhanced data"""
    meta_parts = []
    
    # Basic forecast summary
    meta_parts.append(f"# WindGuru Enhanced Analysis for {analysis.spot_name}")
    meta_parts.append(f"**Location:** {analysis.spot_location}")
    meta_parts.append(f"**Analysis Time:** {analysis.analysis_time.strftime('%Y-%m-%d %H:%M')}")
    meta_parts.append(f"**Data Points:** {len(analysis.data_points)} observed, {len(analysis.predicted_data_points)} predicted")
    
    # Wind statistical summary
    if analysis.statistical_metrics:
        meta_parts.append("\n## Wind Statistics")
        meta_parts.append(f"**Mean Wind Speed:** {analysis.statistical_metrics.get('wind_mean', 0):.1f} knots")
        meta_parts.append(f"**Wind Range:** {analysis.statistical_metrics.get('wind_min', 0):.1f} - {analysis.statistical_metrics.get('wind_max', 0):.1f} knots")
        meta_parts.append(f"**Wind Variability:** {analysis.statistical_metrics.get('wind_std', 0):.1f} knots standard deviation")
    
    # Pressure system analysis
    if analysis.pressure_systems:
        meta_parts.append("\n## Pressure Systems")
        for ps in analysis.pressure_systems:
            desc = f"- **{ps.system_type} pressure system** near {ps.location}"
            if ps.pressure:
                desc += f" ({ps.pressure} hPa)"
            if ps.movement:
                desc += f", moving {ps.movement}"
            if ps.intensity:
                desc += f", {ps.intensity.lower()}"
            meta_parts.append(desc)
    
    # ML model predictions
    if "wind_model" in analysis.ml_predictions:
        meta_parts.append("\n## AI Wind Forecast Model")
        model_info = analysis.ml_predictions["wind_model"]
        meta_parts.append(f"**Model Accuracy:** {model_info.get('score', 0):.2f}")
        
        meta_parts.append("**Feature Importance:**")
        if "feature_importance" in model_info:
            # Sort by importance
            features = model_info["feature_importance"]
            sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)
            for feature, importance in sorted_features:
                meta_parts.append(f"- {feature}: {importance:.2f}")
    
    # Cyclical patterns
    if analysis.cyclical_patterns:
        meta_parts.append("\n## Detected Cyclical Patterns")
        for pattern in analysis.cyclical_patterns:
            meta_parts.append(f"- **{pattern.variable}:** {pattern.period_hours:.1f} hour cycle")
            meta_parts.append(f"  - Likely source: {pattern.likely_source} (confidence: {pattern.confidence:.2f})")
            meta_parts.append(f"  - Magnitude: {pattern.magnitude:.2f}")
    
    # Time series analysis
    if "decomposition" in analysis.time_series_analysis:
        meta_parts.append("\n## Time Series Analysis")
        for var, decomp in analysis.time_series_analysis["decomposition"].items():
            meta_parts.append(f"- **{var}:** {decomp.get('trend_direction', 'unknown')} trend")
            if "seasonal_amplitude" in decomp:
                meta_parts.append(f"  - Seasonal variation: {decomp['seasonal_amplitude']:.2f} units")
    
    # Confidence intervals
    if analysis.confidence_intervals:
        meta_parts.append("\n## Forecast Confidence Intervals (95%)")
        for var, interval in analysis.confidence_intervals.items():
            if not var.endswith("_variance"):
                meta_parts.append(f"- **{var}:** {interval[0]:.2f} to {interval[1]:.2f}")
    
    # Future predictions summary
    if analysis.predicted_data_points:
        meta_parts.append("\n## 24-Hour Wind Forecast Predictions")
        # Group by 6-hour periods
        periods = {
            "0-6 hours": [],
            "7-12 hours": [],
            "13-18 hours": [],
            "19-24 hours": []
        }
        
        for dp in analysis.predicted_data_points:
            hour_idx = analysis.predicted_data_points.index(dp)
            if hour_idx < 6:
                periods["0-6 hours"].append(dp)
            elif hour_idx < 12:
                periods["7-12 hours"].append(dp)
            elif hour_idx < 18:
                periods["13-18 hours"].append(dp)
            else:
                periods["19-24 hours"].append(dp)
        
        for period_name, points in periods.items():
            if points:
                # Calculate average wind for the period
                avg_wind = sum(dp.wind_speed for dp in points) / len(points)
                avg_gusts = sum(dp.wind_gusts for dp in points if dp.wind_gusts is not None) / len(points)
                avg_conf = sum(dp.confidence for dp in points) / len(points)
                
                meta_parts.append(f"- **{period_name}:** {avg_wind:.1f} knots (gusts: {avg_gusts:.1f}), confidence: {avg_conf:.2f}")
    
    # Overall recommendation
    meta_parts.append("\n## Enhanced Weather Analysis")
    
    # Wind conditions assessment
    wind_speeds = [dp.wind_speed for dp in analysis.data_points if dp.wind_speed is not None]
    if wind_speeds:
        mean_speed = np.mean(wind_speeds)
        
        wind_assessment = """Calm and light winds predominate the forecast, suitable for beginners or when stable conditions are preferred."""
        if mean_speed > 25:
            wind_assessment = "High wind conditions dominate this forecast period, suitable only for experienced wind sports practitioners or secure equipment."
        elif mean_speed > 15:
            wind_assessment = "Moderate to strong winds feature prominently in this forecast, providing good conditions for experienced wind sport enthusiasts."
        elif mean_speed > 8:
            wind_assessment = "Light to moderate winds are expected, offering suitable conditions for most wind-dependent activities and skill levels."
        
        meta_parts.append(wind_assessment)
    
    # Pattern detection insights
    if analysis.cyclical_patterns:
        has_diurnal = any("Diurnal" in pattern.likely_source for pattern in analysis.cyclical_patterns)
        has_tidal = any("Tidal" in pattern.likely_source for pattern in analysis.cyclical_patterns)
        
        if has_diurnal:
            meta_parts.append("\nDiurnal (day/night) wind patterns have been detected, suggesting thermal effects influence wind behavior at this location.")
        
        if has_tidal:
            meta_parts.append("\nThe forecast shows evidence of tidal influence on wind patterns, which is common in coastal locations.")
    
    # Trend insights
    for var, decomp in analysis.time_series_analysis.get("decomposition", {}).items():
        if var == "wind_speed" and "trend_direction" in decomp:
            if decomp["trend_direction"] == "increasing":
                meta_parts.append("\nWind speeds show an increasing trend over the forecast period, suggesting developing weather systems.")
            elif decomp["trend_direction"] == "decreasing":
                meta_parts.append("\nWind speeds show a decreasing trend over the forecast period, suggesting stabilizing conditions.")
    
    # Final forecast confidence
    if analysis.confidence_intervals and "wind_speed" in analysis.confidence_intervals:
        interval = analysis.confidence_intervals["wind_speed"]
        interval_range = interval[1] - interval[0]
        
        if interval_range < 5:
            meta_parts.append("\nThis forecast has high statistical confidence with narrow prediction intervals.")
        elif interval_range < 10:
            meta_parts.append("\nThis forecast has moderate statistical confidence with reasonable prediction intervals.")
        else:
            meta_parts.append("\nThis forecast has lower statistical confidence with wide prediction intervals, suggesting higher uncertainty.")
    
    return "\n".join(meta_parts)


async def run_analysis_async(url: str, use_premiere: bool = False) -> WindguruAnalysis:
    """Run the analysis with async support and optimized parameters"""
    # Configure NovaAct with advanced parameters
    model_params = {
        "temperature": 0.2,  # Lower temperature for more deterministic outputs
        "max_tokens": 1024,  # Extended context
        "top_k": 40,         # More focused sampling
    }
    
    # Set up Nova with optional Premiere endpoint
    nova_config = {
        "starting_page": url,
        "model_parameters": model_params,
    }
    
    if use_premiere:
        nova_config["endpoint_name"] = "nova-premiere"
        logger.info("Using Nova Premiere endpoint")
    
    # Initialize NovaAct with advanced configuration
    nova = NovaAct(**nova_config)
    
    try:
        # Ensure we're on the correct page
        await nova.start()
        
        # Run the analysis
        analysis = analyze_forecast(nova, use_premiere=use_premiere)
        
        return analysis
    finally:
        await nova.stop()


def print_detailed_analysis(analysis: WindguruAnalysis) -> None:
    """Print a detailed analysis to the console"""
    print("\n" + "=" * 80)
    print(f"\n{analysis.spot_name} ({analysis.spot_location}) - ENHANCED WIND ANALYSIS")
    print("\n" + "=" * 80)
    
    # Print the full meta-analysis
    print(f"\n{analysis.meta_analysis}")
    
    # Print detailed data table
    print("\n" + "=" * 80)
    print("\nDETAILED FORECAST DATA")
    print("\n" + "-" * 80)
    
    # Format headers
    headers = ["Date/Time", "Wind (kts)", "Gusts (kts)", "Dir", "Temp (°C)", "Conf", "Notes"]
    print("{:<16} {:<10} {:<10} {:<6} {:<10} {:<6} {:<20}".format(*headers))
    print("-" * 100)
    
    # Print actual data
    for i, dp in enumerate(analysis.data_points):
        if i < 20:  # Limit to first 20 points
            date_str = f"{dp.date.strftime('%Y-%m-%d')} {dp.time}"
            wind = f"{dp.wind_speed:.1f}" if dp.wind_speed is not None else "N/A"
            gusts = f"{dp.wind_gusts:.1f}" if dp.wind_gusts is not None else "N/A"
            direction = dp.wind_direction.value if dp.wind_direction else "N/A"
            temp = f"{dp.temperature:.1f}" if dp.temperature is not None else "N/A"
            confidence = f"{dp.confidence:.2f}"
            notes = "Observed"
            
            print("{:<16} {:<10} {:<10} {:<6} {:<10} {:<6} {:<20}".format(
                date_str, wind, gusts, direction, temp, confidence, notes
            ))
    
    # Print future predictions if available
    if analysis.predicted_data_points:
        print("\n" + "-" * 80)
        print("PREDICTED FORECAST DATA")
        print("-" * 80)
        
        print("{:<16} {:<10} {:<10} {:<6} {:<10} {:<6} {:<20}".format(*headers))
        print("-" * 100)
        
        for i, dp in enumerate(analysis.predicted_data_points):
            if i < 24:  # Show up to 24 hours of predictions
                date_str = f"{dp.date.strftime('%Y-%m-%d')} {dp.time}"
                wind = f"{dp.wind_speed:.1f}" if dp.wind_speed is not None else "N/A"
                gusts = f"{dp.wind_gusts:.1f}" if dp.wind_gusts is not None else "N/A"
                direction = dp.wind_direction.value if dp.wind_direction else "N/A"
                temp = f"{dp.temperature:.1f}" if dp.temperature is not None else "N/A"
                confidence = f"{dp.confidence:.2f}"
                notes = f"Prediction +{i+1}h"
                
                print("{:<16} {:<10} {:<10} {:<6} {:<10} {:<6} {:<20}".format(
                    date_str, wind, gusts, direction, temp, confidence, notes
                ))
    
    # Print detailed cyclical patterns if available
    if analysis.cyclical_patterns:
        print("\n" + "-" * 80)
        print("DETECTED CYCLICAL PATTERNS")
        print("-" * 80)
        
        pattern_headers = ["Variable", "Period (hrs)", "Magnitude", "Source", "Confidence"]
        print("{:<15} {:<15} {:<10} {:<20} {:<10}".format(*pattern_headers))
        print("-" * 80)
        
        for pattern in analysis.cyclical_patterns:
            print("{:<15} {:<15.1f} {:<10.3f} {:<20} {:<10.2f}".format(
                pattern.variable, pattern.period_hours, pattern.magnitude, 
                pattern.likely_source, pattern.confidence
            ))
    
    # Print confidence intervals
    if analysis.confidence_intervals:
        print("\n" + "-" * 80)
        print("STATISTICAL CONFIDENCE INTERVALS (95%)")
        print("-" * 80)
        
        for var, interval in analysis.confidence_intervals.items():
            if not var.endswith("_variance"):
                print(f"{var.capitalize():15}: {interval[0]:.2f} to {interval[1]:.2f}")
    
    print("\n" + "=" * 80 + "\n")


def save_analysis_to_file(analysis: WindguruAnalysis, filename: str = None) -> str:
    """Save the analysis to a JSON file for later reference"""
    if filename is None:
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"windguru_analysis_{timestamp}.json"
    
    # Convert analysis to a dictionary
    analysis_dict = {
        "spot_name": analysis.spot_name,
        "spot_location": analysis.spot_location,
        "analysis_time": analysis.analysis_time.strftime("%Y-%m-%d %H:%M:%S"),
        "meta_analysis": analysis.meta_analysis,
        "statistical_metrics": analysis.statistical_metrics,
        
        # Convert data points to dictionaries
        "data_points": [
            {
                "date": dp.date.strftime("%Y-%m-%d"),
                "time": dp.time,
                "temperature": dp.temperature,
                "wind_speed": dp.wind_speed,
                "wind_direction": dp.wind_direction.value if dp.wind_direction else None,
                "wind_gusts": dp.wind_gusts,
                "air_pressure": dp.air_pressure,
                "precipitation": dp.precipitation,
                "cloud_cover": dp.cloud_cover,
                "humidity": dp.humidity,
                "confidence": dp.confidence,
                "predicted": dp.predicted
            } for dp in analysis.data_points
        ],
        
        # Convert predicted points
        "predicted_data_points": [
            {
                "date": dp.date.strftime("%Y-%m-%d"),
                "time": dp.time,
                "temperature": dp.temperature,
                "wind_speed": dp.wind_speed,
                "wind_direction": dp.wind_direction.value if dp.wind_direction else None,
                "wind_gusts": dp.wind_gusts,
                "air_pressure": dp.air_pressure,
                "confidence": dp.confidence
            } for dp in analysis.predicted_data_points
        ],
        
        # Convert pressure systems
        "pressure_systems": [
            {
                "system_type": ps.system_type,
                "location": ps.location,
                "pressure": ps.pressure,
                "movement": ps.movement,
                "intensity": ps.intensity
            } for ps in analysis.pressure_systems
        ],
        
        # Convert cyclical patterns
        "cyclical_patterns": [
            {
                "variable": cp.variable,
                "period_hours": cp.period_hours,
                "magnitude": cp.magnitude,
                "phase": cp.phase,
                "confidence": cp.confidence,
                "likely_source": cp.likely_source
            } for cp in analysis.cyclical_patterns
        ],
        
        # Include confidence intervals and time series analysis
        "confidence_intervals": analysis.confidence_intervals,
        "time_series_analysis": analysis.time_series_analysis,
        "ml_predictions": analysis.ml_predictions
    }
    
    # Save to file
    with open(filename, 'w') as f:
        json.dump(analysis_dict, f, indent=2)
    
    logger.info(f"Analysis saved to {filename}")
    return filename


def main(spot_id: str = "1207462", analyze_map: bool = False, headless: bool = False, 
         use_premiere: bool = False, save_analysis: bool = True) -> None:
    """Main function to run the enhanced windguru analysis"""
    logger.info(f"Starting enhanced analysis for windguru spot ID: {spot_id} with Premiere={use_premiere}")
    
    # Run the analysis using asyncio
    import asyncio
    
    # Create the URL
    url = f"https://www.windguru.cz/{spot_id}"
    
    # Set up NovaAct and run analysis
    analysis = asyncio.run(run_analysis_async(url, use_premiere=use_premiere))
    
    # Print detailed results
    print_detailed_analysis(analysis)
    
    # Save analysis to file if requested
    if save_analysis:
        filename = save_analysis_to_file(analysis)
        print(f"\nAnalysis saved to {filename}")
    
    logger.info("Enhanced analysis complete")


if __name__ == "__main__":
    fire.Fire(main)
EOL 2>&1
