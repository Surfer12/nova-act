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
Analyze renewable energy forecast data from a weather forecast service.

Usage:
python -m nova_act.samples.renewable_energy_forecast [--region <region_name>] [--days <forecast_days>] [--headless]
"""

import logging
import fire
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
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


class SolarForecast(BaseModel):
    """Solar energy forecast data"""
    timestamp: str = Field(..., description="Date and time of the forecast")
    solar_irradiance: float = Field(..., description="Solar irradiance in W/m²")
    cloud_cover: float = Field(..., description="Cloud cover percentage (0-100)")
    energy_production: Optional[float] = Field(None, description="Estimated energy production in kWh")
    efficiency: Optional[float] = Field(None, description="Estimated panel efficiency percentage")


class WindForecast(BaseModel):
    """Wind energy forecast data"""
    timestamp: str = Field(..., description="Date and time of the forecast")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    wind_direction: str = Field(..., description="Wind direction (e.g., NE, SW)")
    turbulence: Optional[float] = Field(None, description="Turbulence intensity (0-1)")
    energy_production: Optional[float] = Field(None, description="Estimated energy production in kWh")


class HydroForecast(BaseModel):
    """Hydropower forecast data"""
    timestamp: str = Field(..., description="Date and time of the forecast")
    precipitation: float = Field(..., description="Precipitation in mm")
    river_flow: Optional[float] = Field(None, description="River flow rate in m³/s")
    energy_production: Optional[float] = Field(None, description="Estimated energy production in kWh")


class RegionInfo(BaseModel):
    """Information about the forecast region"""
    name: str = Field(..., description="Name of the region")
    coordinates: Tuple[float, float] = Field(..., description="Geographic coordinates (lat, long)")
    capacity: Dict[str, float] = Field(..., description="Installed capacity by energy type (MW)")


class RenewableForecast(BaseModel):
    """Complete renewable energy forecast data"""
    region: RegionInfo = Field(..., description="Information about the region")
    forecast_date: str = Field(..., description="Date when the forecast was generated")
    solar_data: List[SolarForecast] = Field(default_factory=list, description="Solar energy forecast data")
    wind_data: List[WindForecast] = Field(default_factory=list, description="Wind energy forecast data")
    hydro_data: List[HydroForecast] = Field(default_factory=list, description="Hydropower forecast data")


class EnergyProductionSummary(BaseModel):
    """Summary of energy production forecast"""
    total_solar: float = Field(..., description="Total forecasted solar energy (kWh)")
    total_wind: float = Field(..., description="Total forecasted wind energy (kWh)")
    total_hydro: float = Field(..., description="Total forecasted hydro energy (kWh)")
    total_renewable: float = Field(..., description="Total forecasted renewable energy (kWh)")
    peak_production_time: str = Field(..., description="Time of peak production")
    peak_production_value: float = Field(..., description="Value of peak production (kWh)")
    low_production_time: str = Field(..., description="Time of lowest production")
    low_production_value: float = Field(..., description="Value of lowest production (kWh)")


class RenewableEnergyAnalysis(BaseModel):
    """Complete analysis of renewable energy forecast"""
    raw_data: RenewableForecast = Field(..., description="Raw forecast data")
    production_summary: EnergyProductionSummary = Field(..., description="Summary of energy production")
    reliability_rating: float = Field(..., description="Reliability rating of the forecast (0-1)")
    weather_factors: Dict[str, List[str]] = Field(..., description="Key weather factors affecting each energy type")
    recommendations: List[str] = Field(..., description="Recommended actions based on the forecast")


def extract_region_info(nova: NovaAct) -> RegionInfo:
    """Extract information about the forecast region"""
    logger.info("Extracting region information")
    
    result = nova.act(
        "Identify the region shown in this forecast, including name and geographic coordinates. "
        "Also determine the installed renewable energy capacity (MW) for solar, wind, and hydro.",
        schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "coordinates": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2
                },
                "capacity": {
                    "type": "object",
                    "properties": {
                        "solar": {"type": "number"},
                        "wind": {"type": "number"},
                        "hydro": {"type": "number"}
                    },
                    "required": ["solar", "wind", "hydro"]
                }
            },
            "required": ["name", "coordinates", "capacity"]
        }
    )
    
    if not result.matches_schema:
        logger.warning("Could not extract region info, using default values")
        return RegionInfo(
            name="Unknown Region",
            coordinates=(0.0, 0.0),
            capacity={"solar": 100.0, "wind": 100.0, "hydro": 100.0}
        )
    
    return RegionInfo(**result.parsed_response)


def extract_solar_forecast(nova: NovaAct, days: int) -> List[SolarForecast]:
    """Extract solar energy forecast data"""
    logger.info(f"Extracting solar forecast data for {days} days")
    
    result = nova.act(
        f"Extract the solar energy forecast data for the next {days} days. For each time point, "
        "determine the solar irradiance (W/m²), cloud cover percentage, estimated energy production (kWh), "
        "and panel efficiency percentage if available.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string"},
                    "solar_irradiance": {"type": "number"},
                    "cloud_cover": {"type": "number"},
                    "energy_production": {"type": "number", "nullable": True},
                    "efficiency": {"type": "number", "nullable": True}
                },
                "required": ["timestamp", "solar_irradiance", "cloud_cover"]
            }
        }
    )
    
    if not result.matches_schema:
        logger.error(f"Failed to extract solar forecast data: {result.parsed_response}")
        # Generate placeholder data if extraction fails
        solar_data = []
        current_time = datetime.now()
        for i in range(days * 8):  # 8 time points per day
            timestamp = (current_time + timedelta(hours=i*3)).strftime("%Y-%m-%d %H:%M")
            solar_data.append(SolarForecast(
                timestamp=timestamp,
                solar_irradiance=500.0,  # Default value
                cloud_cover=50.0,  # Default value
                energy_production=None,
                efficiency=None
            ))
        return solar_data
    
    return [SolarForecast(**item) for item in result.parsed_response]


def extract_wind_forecast(nova: NovaAct, days: int) -> List[WindForecast]:
    """Extract wind energy forecast data"""
    logger.info(f"Extracting wind forecast data for {days} days")
    
    result = nova.act(
        f"Extract the wind energy forecast data for the next {days} days. For each time point, "
        "determine the wind speed (m/s), wind direction, turbulence intensity if available, "
        "and estimated energy production (kWh) if available.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string"},
                    "wind_speed": {"type": "number"},
                    "wind_direction": {"type": "string"},
                    "turbulence": {"type": "number", "nullable": True},
                    "energy_production": {"type": "number", "nullable": True}
                },
                "required": ["timestamp", "wind_speed", "wind_direction"]
            }
        }
    )
    
    if not result.matches_schema:
        logger.error(f"Failed to extract wind forecast data: {result.parsed_response}")
        # Generate placeholder data if extraction fails
        wind_data = []
        current_time = datetime.now()
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        for i in range(days * 8):  # 8 time points per day
            timestamp = (current_time + timedelta(hours=i*3)).strftime("%Y-%m-%d %H:%M")
            wind_data.append(WindForecast(
                timestamp=timestamp,
                wind_speed=5.0,  # Default value
                wind_direction=directions[i % len(directions)],  # Cycle through directions
                turbulence=None,
                energy_production=None
            ))
        return wind_data
    
    return [WindForecast(**item) for item in result.parsed_response]


def extract_hydro_forecast(nova: NovaAct, days: int) -> List[HydroForecast]:
    """Extract hydropower forecast data"""
    logger.info(f"Extracting hydropower forecast data for {days} days")
    
    result = nova.act(
        f"Extract the hydropower forecast data for the next {days} days. For each time point, "
        "determine the precipitation (mm), river flow rate (m³/s) if available, "
        "and estimated energy production (kWh) if available.",
        schema={
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string"},
                    "precipitation": {"type": "number"},
                    "river_flow": {"type": "number", "nullable": True},
                    "energy_production": {"type": "number", "nullable": True}
                },
                "required": ["timestamp", "precipitation"]
            }
        }
    )
    
    if not result.matches_schema:
        logger.error(f"Failed to extract hydropower forecast data: {result.parsed_response}")
        # Generate placeholder data if extraction fails
        hydro_data = []
        current_time = datetime.now()
        for i in range(days * 8):  # 8 time points per day
            timestamp = (current_time + timedelta(hours=i*3)).strftime("%Y-%m-%d %H:%M")
            hydro_data.append(HydroForecast(
                timestamp=timestamp,
                precipitation=2.0,  # Default value
                river_flow=None,
                energy_production=None
            ))
        return hydro_data
    
    return [HydroForecast(**item) for item in result.parsed_response]


def calculate_production_summary(forecast: RenewableForecast) -> EnergyProductionSummary:
    """Calculate the energy production summary from forecast data"""
    logger.info("Calculating energy production summary")
    
    # Get energy production values or estimate if not available
    solar_values = []
    for data in forecast.solar_data:
        if data.energy_production is not None:
            solar_values.append((data.timestamp, data.energy_production))
        else:
            # Simple estimation based on irradiance and cloud cover
            estimated = data.solar_irradiance * (1 - (data.cloud_cover / 100)) * 0.001
            solar_values.append((data.timestamp, estimated))
    
    wind_values = []
    for data in forecast.wind_data:
        if data.energy_production is not None:
            wind_values.append((data.timestamp, data.energy_production))
        else:
            # Simple estimation based on wind speed (cubic relationship)
            estimated = (data.wind_speed ** 3) * 0.1
            wind_values.append((data.timestamp, estimated))
    
    hydro_values = []
    for data in forecast.hydro_data:
        if data.energy_production is not None:
            hydro_values.append((data.timestamp, data.energy_production))
        else:
            # Simple estimation based on precipitation
            estimated = data.precipitation * 5.0
            hydro_values.append((data.timestamp, estimated))
    
    # Calculate totals
    total_solar = sum(value for _, value in solar_values)
    total_wind = sum(value for _, value in wind_values)
    total_hydro = sum(value for _, value in hydro_values)
    total_renewable = total_solar + total_wind + total_hydro
    
    # Combine all timestamps and values for finding peaks
    all_values = []
    timestamps = set()
    
    for timestamp, value in solar_values + wind_values + hydro_values:
        timestamps.add(timestamp)
    
    # For each unique timestamp, sum the energy production
    for timestamp in timestamps:
        total_at_time = 0
        for data_list in [solar_values, wind_values, hydro_values]:
            for t, value in data_list:
                if t == timestamp:
                    total_at_time += value
        all_values.append((timestamp, total_at_time))
    
    # Sort by value to find peak and lowest
    all_values.sort(key=lambda x: x[1])
    
    low_production_time = all_values[0][0] if all_values else "Unknown"
    low_production_value = all_values[0][1] if all_values else 0
    
    peak_production_time = all_values[-1][0] if all_values else "Unknown"
    peak_production_value = all_values[-1][1] if all_values else 0
    
    return EnergyProductionSummary(
        total_solar=total_solar,
        total_wind=total_wind,
        total_hydro=total_hydro,
        total_renewable=total_renewable,
        peak_production_time=peak_production_time,
        peak_production_value=peak_production_value,
        low_production_time=low_production_time,
        low_production_value=low_production_value
    )


def analyze_weather_factors(nova: NovaAct, forecast: RenewableForecast) -> Dict[str, List[str]]:
    """Analyze key weather factors affecting each energy type"""
    logger.info("Analyzing weather factors")
    
    result = nova.act(
        "Based on the forecast data, identify key weather factors that will affect renewable energy production. "
        "Provide a list of factors for each energy type (solar, wind, hydro).",
        schema={
            "type": "object",
            "properties": {
                "solar": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "wind": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "hydro": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["solar", "wind", "hydro"]
        }
    )
    
    if not result.matches_schema:
        logger.error(f"Failed to analyze weather factors: {result.parsed_response}")
        # Return default values
        return {
            "solar": ["Cloud cover", "Solar irradiance"],
            "wind": ["Wind speed", "Wind direction"],
            "hydro": ["Precipitation", "River flow"]
        }
    
    return result.parsed_response


def generate_recommendations(nova: NovaAct, forecast: RenewableForecast, summary: EnergyProductionSummary) -> List[str]:
    """Generate recommendations based on the forecast"""
    logger.info("Generating recommendations")
    
    result = nova.act(
        "Based on the renewable energy forecast and production summary, provide recommendations "
        "for energy grid management, consumption scheduling, and backup power requirements. "
        "Consider factors like peak production times, low production periods, and weather conditions.",
        schema={
            "type": "array",
            "items": {"type": "string"}
        }
    )
    
    if not result.matches_schema:
        logger.error(f"Failed to generate recommendations: {result.parsed_response}")
        # Return default recommendations
        return [
            f"Schedule high energy activities during peak production at {summary.peak_production_time}",
            f"Prepare backup power sources for low production at {summary.low_production_time}",
            "Monitor weather conditions for unexpected changes"
        ]
    
    return result.parsed_response


def calculate_reliability_rating(forecast: RenewableForecast) -> float:
    """Calculate a reliability rating for the forecast"""
    logger.info("Calculating reliability rating")
    
    # Simple algorithm based on data completeness
    total_points = len(forecast.solar_data) + len(forecast.wind_data) + len(forecast.hydro_data)
    complete_points = 0
    
    for data in forecast.solar_data:
        if data.energy_production is not None and data.efficiency is not None:
            complete_points += 1
    
    for data in forecast.wind_data:
        if data.energy_production is not None and data.turbulence is not None:
            complete_points += 1
    
    for data in forecast.hydro_data:
        if data.energy_production is not None and data.river_flow is not None:
            complete_points += 1
    
    if total_points == 0:
        return 0.5  # Default value
    
    return complete_points / total_points


def analyze_renewable_energy(nova: NovaAct, days: int) -> RenewableEnergyAnalysis:
    """Analyze renewable energy forecast"""
    logger.info(f"Starting renewable energy forecast analysis for the next {days} days")
    
    # Extract basic information
    region_info = extract_region_info(nova)
    logger.info(f"Region: {region_info.name}")
    
    forecast_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Extract forecast data for each energy type
    solar_data = extract_solar_forecast(nova, days)
    logger.info(f"Extracted {len(solar_data)} solar forecast data points")
    
    wind_data = extract_wind_forecast(nova, days)
    logger.info(f"Extracted {len(wind_data)} wind forecast data points")
    
    hydro_data = extract_hydro_forecast(nova, days)
    logger.info(f"Extracted {len(hydro_data)} hydro forecast data points")
    
    # Combine into raw forecast data
    forecast = RenewableForecast(
        region=region_info,
        forecast_date=forecast_date,
        solar_data=solar_data,
        wind_data=wind_data,
        hydro_data=hydro_data
    )
    
    # Calculate production summary
    summary = calculate_production_summary(forecast)
    logger.info(f"Total renewable production: {summary.total_renewable:.2f} kWh")
    
    # Analyze weather factors
    weather_factors = analyze_weather_factors(nova, forecast)
    
    # Calculate reliability rating
    reliability = calculate_reliability_rating(forecast)
    logger.info(f"Reliability rating: {reliability:.2f}")
    
    # Generate recommendations
    recommendations = generate_recommendations(nova, forecast, summary)
    logger.info(f"Generated {len(recommendations)} recommendations")
    
    # Return the complete analysis
    return RenewableEnergyAnalysis(
        raw_data=forecast,
        production_summary=summary,
        reliability_rating=reliability,
        weather_factors=weather_factors,
        recommendations=recommendations
    )


def main(region: str = "california", days: int = 3, headless: bool = False) -> None:
    """Main function to analyze renewable energy forecast"""
    logger.info(f"Starting analysis for region: {region}, forecast days: {days}")
    
    # Map of region names to URLs with renewable energy forecasts
    region_urls = {
        "california": "https://www.caiso.com/todaysoutlook/Pages/supply.html",
        "texas": "https://www.ercot.com/gridmkt/dashboards/renewables",
        "europe": "https://energy-charts.info/",
        "australia": "https://opennem.org.au/",
        "global": "https://www.windy.com",
    }
    
    # Get URL for the specified region, default to a general renewable forecast if not found
    url = region_urls.get(region.lower(), "https://www.windy.com")
    
    # Initialize NovaAct with the forecast URL
    with NovaAct(
        starting_page=url,
        browser="chromium",
        headless=headless
    ) as nova:
        logger.info(f"NovaAct session initialized with URL: {url}")
        
        try:
            # Handle any initial page elements like cookie banners
            nova.act("If there is a cookie banner, cookie consent dialog, or popup, close it")
            
            # Allow page to load fully
            nova.act("Wait for the page to fully load with all renewable energy data visible")
            logger.info("Page prepared for analysis")
            
            # Perform the renewable energy forecast analysis
            analysis = analyze_renewable_energy(nova, days)
            
            # Display the analysis results
            print("\n===== RENEWABLE ENERGY FORECAST ANALYSIS =====\n")
            print(f"Region: {analysis.raw_data.region.name}")
            print(f"Coordinates: {analysis.raw_data.region.coordinates}")
            print(f"Forecast generated: {analysis.raw_data.forecast_date}")
            print(f"Forecast reliability: {analysis.reliability_rating:.2f}")
            
            print("\n----- ENERGY PRODUCTION SUMMARY -----")
            print(f"Total Solar Energy: {analysis.production_summary.total_solar:.2f} kWh")
            print(f"Total Wind Energy: {analysis.production_summary.total_wind:.2f} kWh")
            print(f"Total Hydro Energy: {analysis.production_summary.total_hydro:.2f} kWh")
            print(f"Total Renewable Energy: {analysis.production_summary.total_renewable:.2f} kWh")
            print(f"Peak Production: {analysis.production_summary.peak_production_value:.2f} kWh at {analysis.production_summary.peak_production_time}")
            print(f"Lowest Production: {analysis.production_summary.low_production_value:.2f} kWh at {analysis.production_summary.low_production_time}")
            
            print("\n----- KEY WEATHER FACTORS -----")
            for energy_type, factors in analysis.weather_factors.items():
                print(f"\n{energy_type.capitalize()} Energy:")
                for factor in factors:
                    print(f"• {factor}")
            
            print("\n----- RECOMMENDATIONS -----")
            for recommendation in analysis.recommendations:
                print(f"• {recommendation}")
            
            print("\n============================================\n")
            
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