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
python -m nova_act.samples.analyze_winguru [--spot_id <windguru_spot_id>] [--analyze_map] [--headless]
"""

import logging
import fire
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime
import os
from pathlib import Path

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


# Map analysis models
class WindPattern(BaseModel):
    """Information about wind patterns on the map"""
    region: str = Field(..., description="Geographic region affected")
    direction: str = Field(..., description="Wind direction")
    speed_range: str = Field(..., description="Range of wind speeds")
    gust_potential: Optional[str] = Field(None, description="Potential for wind gusts")


class PressureSystem(BaseModel):
    """Information about a high or low pressure system"""
    type: str = Field(..., description="Type of pressure system (high or low)")
    center_location: str = Field(..., description="Geographic location of system center")
    pressure_value: Optional[float] = Field(None, description="Pressure value in hPa/mb if available")
    movement_direction: Optional[str] = Field(None, description="Direction the system is moving")


class MapTimepoint(BaseModel):
    """Forecast data for a specific timepoint on the map"""
    timestamp: str = Field(..., description="Date and time of this forecast map")
    pressure_systems: List[PressureSystem] = Field(default_factory=list, description="Pressure systems visible on map")
    wind_patterns: List[WindPattern] = Field(default_factory=list, description="Major wind patterns visible on map")
    map_url: Optional[str] = Field(None, description="URL or path to map image if saved")


class RegionInfo(BaseModel):
    """Information about the forecast region on the map"""
    name: str = Field(..., description="Name of the region")
    boundaries: str = Field(..., description="Geographic boundaries of the region")


class MapSequence(BaseModel):
    """Collection of forecast maps for a time sequence"""
    region: RegionInfo = Field(..., description="Information about the map region")
    forecast_source: str = Field(..., description="Source of the forecast data")
    forecast_generated: str = Field(..., description="When the forecast was generated")
    timepoints: List[MapTimepoint] = Field(..., description="Collection of forecast maps at different timepoints")


class WindSystemTrack(BaseModel):
    """Track of a wind or pressure system over time"""
    system_type: str = Field(..., description="Type of system (high/low pressure or wind pattern)")
    track_points: List[Tuple[str, str]] = Field(..., description="List of [timepoint, location] pairs")
    intensity_trend: str = Field(..., description="How the system's intensity changes over time")
    impact_regions: List[str] = Field(..., description="Regions impacted by this system")


class MapAnalysis(BaseModel):
    """Complete analysis of the forecast map sequence"""
    raw_data: MapSequence = Field(..., description="Raw map sequence data")
    system_tracks: List[WindSystemTrack] = Field(..., description="Tracks of major systems")
    significant_patterns: List[str] = Field(..., description="Significant weather patterns identified")
    regional_impacts: Dict[str, List[str]] = Field(..., description="Impacts on specific regions")
    overall_synopsis: str = Field(..., description="Overall weather synopsis and forecast")
    saved_images: Optional[List[str]] = Field(None, description="Paths to any saved map images")


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
    
    # First make sure we can see the forecast data table
    nova.act("Make sure the forecast data table is visible, scroll if necessary to see the full table")
    
    # First try to get an overview of the structure
    nova.act("Identify the structure of the forecast data table and its location on the page")
    
    # Extract the data in smaller chunks to avoid overwhelming the model
    # First, identify the dates/times available
    logger.info("Extracting forecast dates and times")
    result = nova.act(
        "Extract just the dates and times for the forecast timepoints shown in the table",
        schema={
            "type": "array",
            "items": {"type": "string"}
        }
    )
    
    if not result.matches_schema or len(result.parsed_response) == 0:
        logger.error(f"Failed to extract forecast dates: {result.parsed_response}")
        logger.info("Attempting alternative extraction approach...")
        
        # Try an alternative approach - extract one sample data point
        result = nova.act(
            "Extract a single sample data point with date, wind speed, wind gusts, wind direction, and temperature",
            schema={
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
        )
        
        if not result.matches_schema:
            logger.error(f"Failed to extract even a single data point: {result.parsed_response}")
            raise ValueError("Could not extract forecast data points")
        
        # Use a minimal dataset with just the one point we found
        data_points = [result.parsed_response]
        logger.info("Using minimal dataset with one data point")
    else:
        # We have the dates, now extract each metric separately
        dates = result.parsed_response
        logger.info(f"Found {len(dates)} forecast timepoints")
        
        # Extract wind speeds
        result = nova.act(
            "Extract the wind speeds (in knots) for each timepoint in the forecast table",
            schema={
                "type": "array",
                "items": {"type": "number"}
            }
        )
        
        if not result.matches_schema or len(result.parsed_response) != len(dates):
            logger.error(f"Failed to extract wind speeds: {result.parsed_response}")
            raise ValueError("Could not extract wind speed data points")
        
        wind_speeds = result.parsed_response
        
        # Extract wind gusts
        result = nova.act(
            "Extract the wind gust speeds (in knots) for each timepoint in the forecast table",
            schema={
                "type": "array",
                "items": {"type": "number"}
            }
        )
        
        if not result.matches_schema or len(result.parsed_response) != len(dates):
            logger.error(f"Failed to extract wind gusts: {result.parsed_response}")
            # Use the wind speeds as fallback for gusts (adding 20%)
            wind_gusts = [round(ws * 1.2, 1) for ws in wind_speeds]
            logger.info("Using calculated wind gusts as fallback")
        else:
            wind_gusts = result.parsed_response
        
        # Extract wind directions
        result = nova.act(
            "Extract the wind directions (e.g., NE, SW) for each timepoint in the forecast table",
            schema={
                "type": "array",
                "items": {"type": "string"}
            }
        )
        
        if not result.matches_schema or len(result.parsed_response) != len(dates):
            logger.error(f"Failed to extract wind directions: {result.parsed_response}")
            # Use a fallback value
            wind_directions = ["Unknown" for _ in dates]
            logger.info("Using placeholder wind directions as fallback")
        else:
            wind_directions = result.parsed_response
        
        # Extract temperatures
        result = nova.act(
            "Extract the temperatures (in Celsius) for each timepoint in the forecast table",
            schema={
                "type": "array",
                "items": {"type": "number"}
            }
        )
        
        if not result.matches_schema or len(result.parsed_response) != len(dates):
            logger.error(f"Failed to extract temperatures: {result.parsed_response}")
            # Use a fallback value
            temperatures = [20.0 for _ in dates]  # Default temperature
            logger.info("Using default temperatures as fallback")
        else:
            temperatures = result.parsed_response
        
        # Combine all data into data points
        data_points = []
        for i in range(len(dates)):
            data_point = {
                "date": dates[i],
                "wind_speed": wind_speeds[i],
                "wind_gusts": wind_gusts[i],
                "wind_direction": wind_directions[i],
                "temperature": temperatures[i],
                "precipitation": None  # Default
            }
            data_points.append(data_point)
        
        logger.info(f"Successfully assembled {len(data_points)} forecast data points")
    
    # data_points is already populated at this point, move directly to combining into raw forecast data
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


def capture_map_screenshot(nova: NovaAct, timepoint_index: int, save_dir: Path) -> str:
    """Capture a screenshot of the map for a specific timepoint"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"windguru_map_{timepoint_index}_{timestamp}.png"
    save_path = save_dir / filename
    
    logger.info(f"Capturing screenshot for timepoint {timepoint_index}")
    nova.screenshot(str(save_path))
    logger.info(f"Screenshot saved to {save_path}")
    
    return str(save_path)


def analyze_map_timepoint(nova: NovaAct, timepoint_index: int) -> MapTimepoint:
    """Analyze a single map timepoint on windguru"""
    logger.info(f"Analyzing map timepoint {timepoint_index}")
    
    # If there's a timepoint selector, navigate to the specified timepoint
    if timepoint_index > 0:
        nova.act(f"Navigate to timepoint/frame {timepoint_index} on the forecast map")
    
    # Extract timestamp
    result = nova.act(
        "Identify and extract the date and time displayed for this map",
        schema={"type": "string"}
    )
    timestamp = result.parsed_response if result.matches_schema else f"Timepoint {timepoint_index}"
    
    # Extract pressure systems
    result = nova.act(
        "Identify all high and low pressure systems visible on the wind map. For each, extract the type (high/low), "  
        "center location, pressure value if shown, and movement direction if indicated.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "center_location": {"type": "string"},
                    "pressure_value": {"type": "number", "nullable": True},
                    "movement_direction": {"type": "string", "nullable": True}
                },
                "required": ["type", "center_location"]
            }
        }
    )
    pressure_systems = result.parsed_response if result.matches_schema else []
    
    # Extract wind patterns
    result = nova.act(
        "Identify major wind patterns visible on the map. For each, describe the region affected, "  
        "wind direction, and speed range.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "region": {"type": "string"},
                    "direction": {"type": "string"},
                    "speed_range": {"type": "string"},
                    "gust_potential": {"type": "string", "nullable": True}
                },
                "required": ["region", "direction", "speed_range"]
            }
        }
    )
    wind_patterns = result.parsed_response if result.matches_schema else []
    
    logger.info(f"Timepoint analysis complete: found {len(pressure_systems)} pressure systems, "
               f"{len(wind_patterns)} wind patterns")
    
    return MapTimepoint(
        timestamp=timestamp,
        pressure_systems=pressure_systems,
        wind_patterns=wind_patterns
    )


def extract_region_info(nova: NovaAct) -> RegionInfo:
    """Extract information about the map region"""
    logger.info("Extracting region information from the windguru map")
    
    result = nova.act(
        "Identify the region shown on this windguru map, including name and geographic boundaries.",
        schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "boundaries": {"type": "string"}
            },
            "required": ["name", "boundaries"]
        }
    )
    
    if not result.matches_schema:
        logger.warning("Could not extract region info, using default values")
        return RegionInfo(
            name="Unknown Region",
            boundaries="Unknown Boundaries"
        )
    
    return RegionInfo(**result.parsed_response)


def analyze_system_tracks(map_sequence: MapSequence) -> List[WindSystemTrack]:
    """Analyze the movement and evolution of pressure systems and wind patterns over time"""
    logger.info("Analyzing pressure system and wind pattern tracks over time")
    
    # Track pressure systems
    systems_by_type = {}
    
    # Group systems by type and collect their locations at each timepoint
    for timepoint in map_sequence.timepoints:
        for system in timepoint.pressure_systems:
            key = system.type
            if key not in systems_by_type:
                systems_by_type[key] = []
            systems_by_type[key].append((timepoint.timestamp, system.center_location))
        
        # Also track major wind patterns
        for wind in timepoint.wind_patterns:
            key = f"Wind_{wind.region}_{wind.direction}"
            if key not in systems_by_type:
                systems_by_type[key] = []
            systems_by_type[key].append((timepoint.timestamp, wind.region))
    
    # Convert to WindSystemTrack objects
    system_tracks = []
    for system_type, track_points in systems_by_type.items():
        # Simple heuristic for intensity trend
        intensity_trend = "Stable"
        
        # Determine if this is a pressure system or wind pattern
        is_pressure_system = not system_type.startswith("Wind_")
        
        # For pressure systems, the impact regions would be nearby areas
        # For wind patterns, the impact region is the region itself
        if is_pressure_system:
            impact_regions = [tp[1] for tp in track_points[:1]]  # Just use the first location as a simple approximation
        else:
            # Extract region from the system_type for wind patterns
            region = system_type.split('_')[1] if len(system_type.split('_')) > 1 else "Unknown"
            impact_regions = [region]
        
        system_tracks.append(WindSystemTrack(
            system_type=system_type,
            track_points=track_points,
            intensity_trend=intensity_trend,
            impact_regions=impact_regions
        ))
    
    logger.info(f"Identified {len(system_tracks)} distinct system tracks")
    return system_tracks


def analyze_wind_map(nova: NovaAct, days: int, save_screenshots: bool = False) -> MapAnalysis:
    """Analyze the wind map from windguru"""
    logger.info(f"Starting wind map analysis for the next {days} days")
    
    # Create directory for screenshots if needed
    save_dir = None
    if save_screenshots:
        save_dir = Path(os.path.expanduser("~/windguru_maps"))
        save_dir.mkdir(exist_ok=True)
        logger.info(f"Screenshots will be saved to {save_dir}")
    
    # Navigate to the map view with explicit steps and verification
    try:
        # Try first approach - look for a specific map link
        logger.info("Attempting to navigate to wind map view")
        nova.act("Look for and click on a link or button that would show the wind map or weather map view")
        
        # Verify we're on a map view
        result = nova.act(
            "Verify if you are now on a page showing a wind or weather map. Respond with yes or no.",
            schema={"type": "boolean"}
        )
        
        if not result.matches_schema or not result.parsed_response:
            logger.warning("First navigation attempt failed, trying alternative approach")
            # Try second approach - direct navigation if URL pattern is known
            nova.act("Navigate to the wind map tab or section that shows a geographical wind forecast")
            
            # Verify again
            result = nova.act(
                "Verify if you can now see a wind or weather map. Respond with yes or no.",
                schema={"type": "boolean"}
            )
            
            if not result.matches_schema or not result.parsed_response:
                logger.warning("Both navigation attempts failed, proceeding with current view")
    except Exception as e:
        logger.error(f"Error navigating to map view: {str(e)}")
        logger.warning("Will attempt to continue with current view")
    
    # Ensure map is fully visible by scrolling if needed
    nova.act("Make sure the wind map is fully visible, scroll if necessary")
    
    # Get general information about the forecast
    logger.info("Extracting forecast information")
    result = nova.act(
        "Extract information about the forecast source (model name) and when it was generated",
        schema={
            "type": "object",
            "properties": {
                "forecast_source": {"type": "string"},
                "forecast_generated": {"type": "string"}
            },
            "required": ["forecast_source", "forecast_generated"]
        }
    )
    
    if not result.matches_schema:
        logger.warning(f"Failed to extract forecast information: {result.parsed_response}")
        forecast_info = {"forecast_source": "Windguru", "forecast_generated": "Unknown"}
    else:
        forecast_info = result.parsed_response
    
    # Extract region information
    region_info = extract_region_info(nova)
    logger.info(f"Map region: {region_info.name}")
    
    # Capture an initial screenshot regardless of settings
    # This helps us debug if something goes wrong
    initial_screenshot_path = None
    if save_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"windguru_map_initial_{timestamp}.png"
        initial_screenshot_path = save_dir / filename
        try:
            nova.screenshot(str(initial_screenshot_path))
            logger.info(f"Initial map screenshot saved to {initial_screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to capture initial screenshot: {str(e)}")
    
    # Determine how many timepoints/frames are available with improved error handling
    try:
        # First check if there are time controls visible
        result = nova.act(
            "Can you see any time controls, timeline, or date/time selectors for the map? Respond with yes or no.",
            schema={"type": "boolean"}
        )
        
        if not result.matches_schema or not result.parsed_response:
            logger.warning("No timeline controls detected, assuming single timepoint")
            num_timepoints = 1
        else:
            # Try to count timepoints
            result = nova.act(
                f"Determine how many timepoints or frames are available in this wind map forecast for the next {days} days",
                schema={"type": "integer"}
            )
            
            if not result.matches_schema or result.parsed_response <= 0:
                logger.warning("Could not determine number of timepoints, defaulting to 3")
                num_timepoints = 3
            else:
                num_timepoints = min(result.parsed_response, days * 4)  # Limit to requested days (assuming 4 per day)
    except Exception as e:
        logger.error(f"Error determining timepoints: {str(e)}")
        num_timepoints = 1  # Conservative fallback
    
    logger.info(f"Will analyze {num_timepoints} timepoints")
    
    # Analyze each timepoint with better error handling
    timepoints = []
    saved_images = []
    
    # Add the initial screenshot if we took one
    if initial_screenshot_path:
        saved_images.append(str(initial_screenshot_path))
    
    for i in range(num_timepoints):
        try:
            logger.info(f"Analyzing timepoint {i+1} of {num_timepoints}")
            timepoint = analyze_map_timepoint(nova, i)
            
            # Capture screenshot if requested
            if save_screenshots and save_dir:
                try:
                    image_path = capture_map_screenshot(nova, i, save_dir)
                    timepoint.map_url = image_path
                    saved_images.append(image_path)
                except Exception as e:
                    logger.error(f"Failed to capture screenshot for timepoint {i}: {str(e)}")
            
            timepoints.append(timepoint)
            
        except Exception as e:
            logger.error(f"Error analyzing timepoint {i}: {str(e)}")
            # Create a minimal timepoint with error information
            timepoints.append(MapTimepoint(
                timestamp=f"Timepoint {i}",
                pressure_systems=[],
                wind_patterns=[WindPattern(
                    region="Unknown",
                    direction="Unknown",
                    speed_range="Unknown"
                )]
            ))
    
    # If we couldn't get any valid timepoints, create a dummy timepoint to avoid failures
    if len(timepoints) == 0:
        timepoints.append(MapTimepoint(
            timestamp="Current",
            pressure_systems=[],
            wind_patterns=[]
        ))
    
    # Create map sequence
    map_sequence = MapSequence(
        region=region_info,
        forecast_source=forecast_info["forecast_source"],
        forecast_generated=forecast_info["forecast_generated"],
        timepoints=timepoints
    )
    
    # Analyze system tracks with error handling
    try:
        system_tracks = analyze_system_tracks(map_sequence)
    except Exception as e:
        logger.error(f"Error analyzing system tracks: {str(e)}")
        # Create a minimal system track to avoid failures
        system_tracks = [WindSystemTrack(
            system_type="Unknown",
            track_points=[("Unknown", "Unknown")],
            intensity_trend="Unknown",
            impact_regions=["Unknown"]
        )]
    
    # Extract significant patterns with improved prompting
    try:
        result = nova.act(
            "Look at the wind map and identify 2-4 significant wind patterns or weather features visible on the map. "
            "These could include high/low pressure systems, fronts, wind flow patterns, or areas of strong winds. "
            "Describe each pattern briefly in one sentence.",
            schema={
                "type": "array",
                "items": {"type": "string"}
            }
        )
        significant_patterns = result.parsed_response if result.matches_schema else ["No significant patterns identified"]
    except Exception as e:
        logger.error(f"Error extracting significant patterns: {str(e)}")
        significant_patterns = ["Error identifying patterns", "Check screenshots for visual reference"]
    
    # Analyze regional impacts with simpler approach
    try:
        # First identify regions
        result = nova.act(
            "Identify 2-3 main geographic regions visible on this wind map",
            schema={
                "type": "array",
                "items": {"type": "string"}
            }
        )
        
        if not result.matches_schema or len(result.parsed_response) == 0:
            regions = ["Main Region"]
        else:
            regions = result.parsed_response
        
        # Then get impacts for each region
        regional_impacts = {}
        for region in regions:
            try:
                result = nova.act(
                    f"For the {region} region on the wind map, briefly describe the expected wind conditions in 1-2 sentences",
                    schema={
                        "type": "array",
                        "items": {"type": "string"}
                    }
                )
                regional_impacts[region] = result.parsed_response if result.matches_schema else ["Unknown impacts"]
            except Exception as e:
                logger.error(f"Error getting impacts for {region}: {str(e)}")
                regional_impacts[region] = ["Error analyzing this region"]
    except Exception as e:
        logger.error(f"Error analyzing regional impacts: {str(e)}")
        regional_impacts = {"Visible Region": ["Unable to analyze regional impacts"]}
    
    # Generate overall synopsis with simplified approach
    try:
        result = nova.act(
            "Based on the wind map you can see, provide a brief 2-3 sentence synopsis of the overall wind pattern",
            schema={"type": "string"}
        )
        overall_synopsis = result.parsed_response if result.matches_schema else "No synopsis available"
    except Exception as e:
        logger.error(f"Error generating synopsis: {str(e)}")
        overall_synopsis = "Unable to generate synopsis due to data extraction issues"
    
    logger.info("Wind map analysis complete")
    
    # Return complete analysis
    return MapAnalysis(
        raw_data=map_sequence,
        system_tracks=system_tracks,
        significant_patterns=significant_patterns,
        regional_impacts=regional_impacts,
        overall_synopsis=overall_synopsis,
        saved_images=saved_images if saved_images else None
    )


def main(spot_id: str = "1207462", analyze_map: bool = False, headless: bool = False, save_screenshots: bool = False) -> None:
    """Main function to analyze wind forecast from windguru.cz"""
    logger.info(f"Starting analysis for windguru spot ID: {spot_id}")
    
    # Initialize NovaAct with the specified spot ID
    with NovaAct(
        starting_page=f"https://www.windguru.cz/{spot_id}",
        chrome_channel="chrome",
        headless=headless
    ) as nova:
        logger.info("NovaAct session initialized")
        
        try:
            # Handle any initial page elements like cookie banners
            nova.act("If there is a cookie banner or popup, close it")
            logger.info("Page prepared for analysis")
            
            # Perform the standard forecast analysis
            analysis = analyze_forecast(nova)
            
            # Display the standard analysis results
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
            
            logger.info("Standard analysis complete and results displayed")
            
            # If map analysis is requested, perform it
            if analyze_map:
                logger.info("Starting additional wind map analysis")
                try:
                    map_analysis = analyze_wind_map(nova, days=3, save_screenshots=save_screenshots)
                    
                    # Display the map analysis results
                    print("\n===== WIND MAP ANALYSIS =====\n")
                    print(f"Region: {map_analysis.raw_data.region.name} ({map_analysis.raw_data.region.boundaries})")
                    print(f"Forecast source: {map_analysis.raw_data.forecast_source}")
                    print(f"Forecast generated: {map_analysis.raw_data.forecast_generated}")
                    print(f"Timepoints analyzed: {len(map_analysis.raw_data.timepoints)}")
                    
                    if map_analysis.saved_images:
                        print(f"\nScreenshots saved: {len(map_analysis.saved_images)}")
                        for path in map_analysis.saved_images:
                            print(f"  - {path}")
                    
                    print("\n----- SIGNIFICANT WIND PATTERNS -----")
                    for pattern in map_analysis.significant_patterns:
                        print(f"• {pattern}")
                    
                    print("\n----- SYSTEM TRACKS -----")
                    for track in map_analysis.system_tracks:
                        print(f"• {track.system_type} System:")
                        print(f"  - Intensity trend: {track.intensity_trend}")
                        print(f"  - Track: {' → '.join([loc for _, loc in track.track_points])}")
                        print(f"  - Impacts: {', '.join(track.impact_regions)}")
                    
                    print("\n----- REGIONAL IMPACTS -----")
                    for region, impacts in map_analysis.regional_impacts.items():
                        print(f"• {region}:")
                        for impact in impacts:
                            print(f"  - {impact}")
                    
                    print("\n----- OVERALL WIND MAP SYNOPSIS -----")
                    print(map_analysis.overall_synopsis)
                    print("\n====================================\n")
                    
                    logger.info("Map analysis complete and results displayed")
                    
                except Exception as e:
                    logger.error(f"Error during map analysis: {str(e)}", exc_info=True)
                    print(f"\nAn error occurred during map analysis: {str(e)}")
            
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