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
Analyze weather forecast maps showing wind movement and pressure systems.

Usage:
python -m nova_act.samples.analyze_forecast_map [--region <region_name>] [--days <forecast_days>] [--headless]
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


class PressureSystem(BaseModel):
    """Information about a high or low pressure system"""
    type: str = Field(..., description="Type of pressure system (high or low)")
    center_location: str = Field(..., description="Geographic location of system center")
    pressure_value: Optional[float] = Field(None, description="Pressure value in hPa/mb if available")
    movement_direction: Optional[str] = Field(None, description="Direction the system is moving")
    movement_speed: Optional[str] = Field(None, description="Speed at which the system is moving")


class WindPattern(BaseModel):
    """Information about wind patterns"""
    region: str = Field(..., description="Geographic region affected")
    direction: str = Field(..., description="Wind direction")
    speed_range: str = Field(..., description="Range of wind speeds")
    associated_system: Optional[str] = Field(None, description="Pressure system causing this wind pattern")


class WeatherFront(BaseModel):
    """Information about weather fronts"""
    type: str = Field(..., description="Type of front (cold, warm, occluded, stationary)")
    location: str = Field(..., description="Geographic location/path of the front")
    movement: Optional[str] = Field(None, description="Movement direction and speed if applicable")


class MapTimepoint(BaseModel):
    """Forecast data for a specific timepoint"""
    timestamp: str = Field(..., description="Date and time of this forecast map")
    pressure_systems: List[PressureSystem] = Field(default_factory=list, description="Pressure systems visible on map")
    wind_patterns: List[WindPattern] = Field(default_factory=list, description="Major wind patterns visible on map")
    fronts: List[WeatherFront] = Field(default_factory=list, description="Weather fronts visible on map")
    map_url: Optional[str] = Field(None, description="URL or path to map image if saved")


class RegionInfo(BaseModel):
    """Information about the forecast region"""
    name: str = Field(..., description="Name of the region")
    boundaries: str = Field(..., description="Geographic boundaries of the region")
    map_projection: Optional[str] = Field(None, description="Map projection type if specified")


class MapSequence(BaseModel):
    """Collection of forecast maps for a time sequence"""
    region: RegionInfo = Field(..., description="Information about the map region")
    forecast_source: str = Field(..., description="Source of the forecast data")
    forecast_generated: str = Field(..., description="When the forecast was generated")
    timepoints: List[MapTimepoint] = Field(..., description="Collection of forecast maps at different timepoints")


class SystemTrack(BaseModel):
    """Track of a pressure system over time"""
    system_type: str = Field(..., description="Type of system (high/low)")
    track_points: List[Tuple[str, str]] = Field(..., description="List of [timepoint, location] pairs")
    intensity_trend: str = Field(..., description="How the system's intensity changes over time")
    impact_regions: List[str] = Field(..., description="Regions impacted by this system")


class MapAnalysis(BaseModel):
    """Complete analysis of the forecast map sequence"""
    raw_data: MapSequence = Field(..., description="Raw map sequence data")
    system_tracks: List[SystemTrack] = Field(..., description="Tracks of major pressure systems")
    significant_patterns: List[str] = Field(..., description="Significant weather patterns identified")
    regional_impacts: Dict[str, List[str]] = Field(..., description="Impacts on specific regions")
    overall_synopsis: str = Field(..., description="Overall weather synopsis and forecast")
    saved_images: Optional[List[str]] = Field(None, description="Paths to any saved map images")


def capture_map_screenshot(nova: NovaAct, timepoint_index: int, save_dir: Path) -> str:
    """Capture a screenshot of the map for a specific timepoint"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"map_{timepoint_index}_{timestamp}.png"
    save_path = save_dir / filename
    
    logger.info(f"Capturing screenshot for timepoint {timepoint_index}")
    nova.screenshot(str(save_path))
    logger.info(f"Screenshot saved to {save_path}")
    
    return str(save_path)


def analyze_map_timepoint(nova: NovaAct, timepoint_index: int) -> MapTimepoint:
    """Analyze a single map timepoint"""
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
        "Identify all high and low pressure systems visible on the map. For each, extract the type (high/low), "  
        "center location, pressure value if shown, and movement direction/speed if indicated.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "center_location": {"type": "string"},
                    "pressure_value": {"type": "number", "nullable": True},
                    "movement_direction": {"type": "string", "nullable": True},
                    "movement_speed": {"type": "string", "nullable": True}
                },
                "required": ["type", "center_location"]
            }
        }
    )
    pressure_systems = result.parsed_response if result.matches_schema else []
    
    # Extract wind patterns
    result = nova.act(
        "Identify major wind patterns visible on the map. For each, describe the region affected, "  
        "wind direction, speed range, and any associated pressure system.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "region": {"type": "string"},
                    "direction": {"type": "string"},
                    "speed_range": {"type": "string"},
                    "associated_system": {"type": "string", "nullable": True}
                },
                "required": ["region", "direction", "speed_range"]
            }
        }
    )
    wind_patterns = result.parsed_response if result.matches_schema else []
    
    # Extract weather fronts
    result = nova.act(
        "Identify all weather fronts visible on the map. For each, extract the type (cold, warm, etc.), "  
        "location/path, and movement direction/speed if shown.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "location": {"type": "string"},
                    "movement": {"type": "string", "nullable": True}
                },
                "required": ["type", "location"]
            }
        }
    )
    fronts = result.parsed_response if result.matches_schema else []
    
    logger.info(f"Timepoint analysis complete: found {len(pressure_systems)} pressure systems, "
               f"{len(wind_patterns)} wind patterns, {len(fronts)} fronts")
    
    return MapTimepoint(
        timestamp=timestamp,
        pressure_systems=pressure_systems,
        wind_patterns=wind_patterns,
        fronts=fronts
    )


def extract_region_info(nova: NovaAct) -> RegionInfo:
    """Extract information about the map region"""
    logger.info("Extracting region information")
    
    result = nova.act(
        "Identify the region shown on this map, including name and geographic boundaries. "  
        "Also note the map projection type if specified.",
        schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "boundaries": {"type": "string"},
                "map_projection": {"type": "string", "nullable": True}
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


def analyze_system_tracks(map_sequence: MapSequence) -> List[SystemTrack]:
    """Analyze the movement and evolution of pressure systems over time"""
    logger.info("Analyzing pressure system tracks over time")
    
    # Map of system identification to timepoint and location
    # This is a simplistic approach - in a real implementation, we would need 
    # more sophisticated tracking to identify the same system across timepoints
    systems_by_type = {}
    
    # Group systems by type and collect their locations at each timepoint
    for timepoint in map_sequence.timepoints:
        for system in timepoint.pressure_systems:
            key = system.type
            if key not in systems_by_type:
                systems_by_type[key] = []
            systems_by_type[key].append((timepoint.timestamp, system.center_location))
    
    # Convert to SystemTrack objects
    system_tracks = []
    for system_type, track_points in systems_by_type.items():
        # Simple heuristic to determine intensity trend and impact regions
        intensity_trend = "Stable"  # Would be determined by analyzing pressure values over time
        impact_regions = []  # Would be determined by analyzing affected areas
        
        # Analyze affected regions based on wind patterns
        for timepoint in map_sequence.timepoints:
            for wind in timepoint.wind_patterns:
                if wind.associated_system and system_type.lower() in wind.associated_system.lower():
                    if wind.region not in impact_regions:
                        impact_regions.append(wind.region)
        
        system_tracks.append(SystemTrack(
            system_type=system_type,
            track_points=track_points,
            intensity_trend=intensity_trend,
            impact_regions=impact_regions if impact_regions else ["Unknown"]
        ))
    
    logger.info(f"Identified {len(system_tracks)} distinct system tracks")
    return system_tracks


def analyze_forecast_maps(nova: NovaAct, days: int, save_screenshots: bool = False) -> MapAnalysis:
    """Analyze a sequence of forecast maps"""
    logger.info(f"Starting forecast map analysis for the next {days} days")
    
    # Create directory for screenshots if needed
    save_dir = None
    if save_screenshots:
        save_dir = Path(os.path.expanduser("~/forecast_maps"))
        save_dir.mkdir(exist_ok=True)
        logger.info(f"Screenshots will be saved to {save_dir}")
    
    # Get general information about the forecast
    result = nova.act(
        "Extract information about the forecast source and when it was generated",
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
        logger.error(f"Failed to extract forecast information: {result.parsed_response}")
        forecast_info = {"forecast_source": "Unknown", "forecast_generated": "Unknown"}
    else:
        forecast_info = result.parsed_response
    
    # Extract region information
    region_info = extract_region_info(nova)
    logger.info(f"Map region: {region_info.name}")
    
    # Determine how many timepoints/frames are available
    result = nova.act(
        f"Determine how many timepoints or frames are available in this forecast for the next {days} days",
        schema={"type": "integer"}
    )
    
    if not result.matches_schema or result.parsed_response <= 0:
        logger.warning("Could not determine number of timepoints, defaulting to 4")
        num_timepoints = 4
    else:
        num_timepoints = min(result.parsed_response, days * 4)  # Limit to requested days (assuming 4 per day)
    
    logger.info(f"Will analyze {num_timepoints} timepoints")
    
    # Analyze each timepoint
    timepoints = []
    saved_images = []
    
    for i in range(num_timepoints):
        timepoint = analyze_map_timepoint(nova, i)
        
        # Capture screenshot if requested
        if save_screenshots and save_dir:
            image_path = capture_map_screenshot(nova, i, save_dir)
            timepoint.map_url = image_path
            saved_images.append(image_path)
        
        timepoints.append(timepoint)
    
    # Create map sequence
    map_sequence = MapSequence(
        region=region_info,
        forecast_source=forecast_info["forecast_source"],
        forecast_generated=forecast_info["forecast_generated"],
        timepoints=timepoints
    )
    
    # Analyze system tracks
    system_tracks = analyze_system_tracks(map_sequence)
    
    # Extract significant patterns
    result = nova.act(
        "Based on the forecast maps, identify significant weather patterns over the forecast period. "
        "Include major systems, frontal movements, and potential severe weather.",
        schema={
            "type": "array",
            "items": {"type": "string"}
        }
    )
    significant_patterns = result.parsed_response if result.matches_schema else ["No significant patterns identified"]
    
    # Analyze regional impacts
    result = nova.act(
        "For each major region visible on the map, summarize the expected weather impacts "
        "over the forecast period. Include effects from pressure systems, fronts, and wind patterns.",
        schema={
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    )
    regional_impacts = result.parsed_response if result.matches_schema else {"Unspecified region": ["Unknown impacts"]}
    
    # Generate overall synopsis
    result = nova.act(
        "Provide a comprehensive synopsis of the weather patterns shown in these forecast maps. "
        "Summarize the movement of major systems, expected changes, and overall forecast for the region.",
        schema={"type": "string"}
    )
    overall_synopsis = result.parsed_response if result.matches_schema else "No synopsis available"
    
    logger.info("Forecast map analysis complete")
    
    # Return complete analysis
    return MapAnalysis(
        raw_data=map_sequence,
        system_tracks=system_tracks,
        significant_patterns=significant_patterns,
        regional_impacts=regional_impacts,
        overall_synopsis=overall_synopsis,
        saved_images=saved_images if saved_images else None
    )


def main(region: str = "north_america", days: int = 3, headless: bool = False, save_screenshots: bool = False) -> None:
    """Main function to analyze weather forecast maps"""
    logger.info(f"Starting analysis for region: {region}, forecast days: {days}")
    
    # Map of region names to URLs
    region_urls = {
        "north_america": "https://www.wpc.ncep.noaa.gov/basicwx/basic_us.php",
        "europe": "https://www.ecmwf.int/en/forecasts/charts",
        "global": "https://www.windy.com",
        "atlantic": "https://www.nhc.noaa.gov/",
        "pacific": "https://www.nhc.noaa.gov/",
    }
    
    # Get URL for the specified region, default to windy.com if not found
    url = region_urls.get(region.lower(), "https://www.windy.com")
    
    # Initialize NovaAct with the map URL
    with NovaAct(
        starting_page=url,
        headless=headless
    ) as nova:
        logger.info(f"NovaAct session initialized with URL: {url}")
        
        try:
            # Handle any initial page elements like cookie banners
            nova.act("If there is a cookie banner, cookie consent dialog, or popup, close it")
            
            # Prepare the map view if needed
            if "windy.com" in url:
                nova.act(
                    "If there are options to show pressure systems or weather fronts, enable them. "
                    "Ensure the map is showing pressure and wind information."
                )
            
            # Navigate to the appropriate forecast map if needed
            if "ecmwf.int" in url:
                nova.act("Navigate to the latest medium-range forecast map showing pressure and fronts")
            elif "wpc.ncep.noaa.gov" in url:
                nova.act("Find and navigate to the surface analysis forecast maps")
            elif "nhc.noaa.gov" in url:
                nova.act("Navigate to the latest tropical analysis and forecast maps")
            
            logger.info("Page prepared for analysis")
            
            # Perform the forecast map analysis
            analysis = analyze_forecast_maps(nova, days, save_screenshots)
            
            # Display the analysis results
            print("\n===== WEATHER FORECAST MAP ANALYSIS =====\n")
            print(f"Region: {analysis.raw_data.region.name} ({analysis.raw_data.region.boundaries})")
            print(f"Forecast source: {analysis.raw_data.forecast_source}")
            print(f"Forecast generated: {analysis.raw_data.forecast_generated}")
            print(f"Timepoints analyzed: {len(analysis.raw_data.timepoints)}")
            
            if analysis.saved_images:
                print(f"\nScreenshots saved: {len(analysis.saved_images)}")
                for path in analysis.saved_images:
                    print(f"  - {path}")
            
            print("\n----- SIGNIFICANT WEATHER PATTERNS -----")
            for pattern in analysis.significant_patterns:
                print(f"u2022 {pattern}")
            
            print("\n----- PRESSURE SYSTEM TRACKS -----")
            for track in analysis.system_tracks:
                print(f"u2022 {track.system_type} Pressure System:")
                print(f"  - Intensity trend: {track.intensity_trend}")
                print(f"  - Track: {' → '.join([loc for _, loc in track.track_points])}")
                print(f"  - Impacts: {', '.join(track.impact_regions)}")
            
            print("\n----- REGIONAL IMPACTS -----")
            for region, impacts in analysis.regional_impacts.items():
                print(f"u2022 {region}:")
                for impact in impacts:
                    print(f"  - {impact}")
            
            print("\n----- OVERALL FORECAST SYNOPSIS -----")
            print(analysis.overall_synopsis)
            print("\n========================================\n")
            
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