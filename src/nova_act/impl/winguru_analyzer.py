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

from typing import Dict, List, Tuple, NamedTuple, Optional, Any

import pandas as pd
import numpy as np
from playwright.sync_api import Page

from nova_act.impl.backend import Backend
from nova_act.util.logging import setup_logging
from nova_act.config import load_config, get_profile

_LOGGER = setup_logging(__name__)


class WindGuruAnalysisResult(NamedTuple):
    """Result of wind forecast analysis.
    
    Attributes:
        raw_data: Raw data extracted from the forecast
        data_frame: Processed data as a pandas DataFrame
        micro_patterns: Short-term patterns (next 24h)
        meso_patterns: Medium-term patterns (24-72h)
        macro_patterns: Long-term patterns (3+ days)
        meta_analysis: Overall analysis and recommendation
        statistics: Statistical analysis of the forecast data
    """
    raw_data: Dict[str, Any]
    data_frame: Optional[pd.DataFrame] = None
    micro_patterns: List[str] = []
    meso_patterns: List[str] = []
    macro_patterns: List[str] = []
    meta_analysis: str = ""
    statistics: Dict[str, Any] = {}


class WinGuruAnalyzer:
    """Analyzer for extracting and interpreting wind forecast data from winguru.cz
    using a fractal, multi-layered analysis framework."""

    def __init__(self, page: Page, backend: Backend, profile_name: str = "base"):
        """Initialize the WinGuruAnalyzer.
        
        Args:
            page: Playwright page object for browser automation
            backend: Backend service for API calls
            profile_name: Name of the configuration profile to use (default: "base")
        """
        self.page = page
        self.backend = backend
        
        # Load configuration from the specified profile
        self.config = get_profile(profile_name)
        _LOGGER.info(f"Initialized WinGuruAnalyzer with profile: {profile_name}")
        
        # Extract key configuration parameters
        self.time_windows = self.config.get("time_windows", {})
        self.analysis_params = self.config.get("analysis", {})
        self.wind_speed_thresholds = self.config.get("wind_speed", {})
        self.gust_factor_thresholds = self.config.get("gust_factor", {})
        
        _LOGGER.debug(f"Using time windows: {self.time_windows}")
        _LOGGER.debug(f"Using analysis parameters: {self.analysis_params}")
        
    def extract_forecast_data(self, url: str = "https://www.windguru.cz") -> Dict[str, Any]:
        """Extract raw forecast data from winguru.cz.
        
        Args:
            url: URL of the windguru forecast page
            
        Returns:
            Dictionary containing raw forecast data
        """
        _LOGGER.info(f"Navigating to {url} for data extraction")
        self.page.goto(url, wait_until="networkidle")
        
        # Extract data using page evaluation - this would target specific DOM elements
        # containing wind forecast information
        raw_data = self.page.evaluate("""
            () => {
                const data = {};
                // This is a placeholder for actual DOM scraping logic
                // Would target specific elements containing wind speed, direction, etc.
                data['forecast'] = document.body.innerText.includes('forecast') ? 'Sample forecast data' : 'No forecast found';
                
                // Extract timestamp information
                const now = new Date();
                data['timestamp'] = now.toISOString();
                
                // Extract any available forecast data
                const forecastData = [];
                
                // Sample data for demonstration
                for (let i = 0; i < 24; i++) {
                    const hour = new Date(now);
                    hour.setHours(hour.getHours() + i);
                    
                    forecastData.push({
                        time: hour.toISOString(),
                        wind_speed: 5 + Math.random() * 10,
                        wind_direction: ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'][Math.floor(Math.random() * 8)],
                        temperature: 15 + Math.random() * 10,
                        precipitation: Math.random() < 0.3 ? Math.random() * 5 : 0
                    });
                }
                
                data['forecast_data'] = forecastData;
                return data;
            }
        """)
        
        _LOGGER.info(f"Extracted raw data with {len(raw_data.get('forecast_data', []))} data points")
        return raw_data

    def analyze_fractal_patterns(self, data: Dict[str, Any]) -> Tuple[List[str], List[str], List[str]]:
        """Analyze data using fractal framework at micro, meso, and macro levels.
        
        Args:
            data: Raw forecast data
            
        Returns:
            Tuple of (micro_patterns, meso_patterns, macro_patterns)
        """
        # Use time windows from configuration
        micro_hours = self.time_windows.get("micro", {}).get("hours", 24)
        meso_hours = self.time_windows.get("meso", {}).get("hours", 72)
        macro_hours = self.time_windows.get("macro", {}).get("hours", 168)
        
        _LOGGER.info(f"Analyzing patterns with time windows: micro={micro_hours}h, meso={meso_hours}h, macro={macro_hours}h")
        
        micro_patterns = self._extract_patterns(data, scale='micro', hours=micro_hours)
        meso_patterns = self._extract_patterns(data, scale='meso', hours=meso_hours)
        macro_patterns = self._extract_patterns(data, scale='macro', hours=macro_hours)
        
        return micro_patterns, meso_patterns, macro_patterns

    def _extract_patterns(self, data: Dict[str, Any], scale: str, hours: int) -> List[str]:
        """Extract patterns at specified scale.
        
        Args:
            data: Raw forecast data
            scale: Analysis scale ('micro', 'meso', or 'macro')
            hours: Time window in hours
            
        Returns:
            List of pattern descriptions
        """
        patterns = []
        forecast_data = data.get('forecast_data', [])
        
        if not forecast_data:
            patterns.append(f"{scale.capitalize()}-level analysis: Insufficient data")
            return patterns
            
        # Filter data points within the time window
        # In a real implementation, this would filter based on the timestamp
        filtered_data = forecast_data[:min(len(forecast_data), hours // 3)]  # Approximate 3-hour intervals
        
        if not filtered_data:
            patterns.append(f"{scale.capitalize()}-level analysis: No data points in the {hours}h window")
            return patterns
            
        # Extract wind speeds and directions
        wind_speeds = [point.get('wind_speed', 0) for point in filtered_data]
        wind_directions = [point.get('wind_direction', '') for point in filtered_data]
        
        # Calculate basic statistics
        if wind_speeds:
            avg_speed = sum(wind_speeds) / len(wind_speeds)
            max_speed = max(wind_speeds)
            min_speed = min(wind_speeds)
            speed_range = max_speed - min_speed
            
            # Categorize wind speed based on thresholds from configuration
            category = "unknown"
            for cat_name, cat_range in self.wind_speed_thresholds.items():
                cat_min = cat_range.get("min", 0)
                cat_max = cat_range.get("max", float('inf'))
                if cat_min <= avg_speed < cat_max:
                    category = cat_name
                    break
            
            # Detect trends
            change_threshold = self.analysis_params.get("trend_detection", {}).get("change_threshold", 20)
            min_absolute_change = self.analysis_params.get("trend_detection", {}).get("min_absolute_change", 2.0)
            
            if len(wind_speeds) > 1:
                first_half = wind_speeds[:len(wind_speeds)//2]
                second_half = wind_speeds[len(wind_speeds)//2:]
                
                if first_half and second_half:
                    avg_first = sum(first_half) / len(first_half)
                    avg_second = sum(second_half) / len(second_half)
                    
                    percent_change = ((avg_second - avg_first) / avg_first * 100) if avg_first > 0 else 0
                    absolute_change = avg_second - avg_first
                    
                    if percent_change > change_threshold and absolute_change > min_absolute_change:
                        trend = "increasing"
                    elif percent_change < -change_threshold and absolute_change < -min_absolute_change:
                        trend = "decreasing"
                    else:
                        trend = "steady"
                        
                    patterns.append(f"{scale.capitalize()}-level wind trend: {trend.capitalize()}")
            
            # Add pattern descriptions based on the scale
            if scale == 'micro':
                patterns.append(f"Short-term ({hours}h) wind speed: {avg_speed:.1f} knots ({category})")
                if speed_range > self.analysis_params.get("variability", {}).get("high_variability", 10.0):
                    patterns.append(f"High wind variability in the next {hours} hours (range: {speed_range:.1f} knots)")
            elif scale == 'meso':
                patterns.append(f"Medium-term ({hours}h) average wind: {avg_speed:.1f} knots with peaks to {max_speed:.1f} knots")
                
                # Check for direction consistency
                if len(set(wind_directions)) <= 2:
                    patterns.append(f"Consistent wind direction from {wind_directions[0]} over the {hours}h period")
                else:
                    patterns.append(f"Variable wind directions over the {hours}h period")
            else:  # macro
                patterns.append(f"Long-term ({hours}h) wind pattern: {category.capitalize()} winds averaging {avg_speed:.1f} knots")
                
                # Check for cyclic patterns (simplified)
                if len(wind_speeds) > 6:
                    day_night_diff = abs(sum(wind_speeds[::2]) / len(wind_speeds[::2]) - 
                                        sum(wind_speeds[1::2]) / len(wind_speeds[1::2]))
                    if day_night_diff > min_absolute_change:
                        patterns.append(f"Possible diurnal pattern detected with {day_night_diff:.1f} knots variation")
        
        return patterns

    def generate_meta_analysis(self, micro: List[str], meso: List[str], macro: List[str], data: Dict[str, Any]) -> str:
        """Generate meta-analysis across scales.
        
        Args:
            micro: Micro-level patterns
            meso: Meso-level patterns
            macro: Macro-level patterns
            data: Raw forecast data
            
        Returns:
            Meta-analysis text
        """
        forecast_data = data.get('forecast_data', [])
        
        if not forecast_data:
            return "Insufficient data for meta-analysis"
            
        # Extract wind speeds
        wind_speeds = [point.get('wind_speed', 0) for point in forecast_data]
        
        if not wind_speeds:
            return "No wind data available for meta-analysis"
            
        # Calculate statistics
        avg_speed = sum(wind_speeds) / len(wind_speeds)
        max_speed = max(wind_speeds)
        min_speed = min(wind_speeds)
        speed_range = max_speed - min_speed
        
        # Categorize overall wind conditions
        category = "unknown"
        for cat_name, cat_range in self.wind_speed_thresholds.items():
            cat_min = cat_range.get("min", 0)
            cat_max = cat_range.get("max", float('inf'))
            if cat_min <= avg_speed < cat_max:
                category = cat_name
                break
                
        # Determine variability
        high_variability = self.analysis_params.get("variability", {}).get("high_variability", 10.0)
        low_variability = self.analysis_params.get("variability", {}).get("low_variability", 5.0)
        
        if speed_range > high_variability:
            variability = "highly variable"
        elif speed_range < low_variability:
            variability = "stable"
        else:
            variability = "moderately variable"
            
        # Check for gustiness
        if len(forecast_data) > 1 and all('wind_speed' in point for point in forecast_data):
            # Calculate gust factor if available
            if any('gust' in point for point in forecast_data):
                gust_factors = []
                for point in forecast_data:
                    if 'gust' in point and point.get('wind_speed', 0) > 0:
                        gust_factors.append(point['gust'] / point['wind_speed'])
                
                if gust_factors:
                    avg_gust_factor = sum(gust_factors) / len(gust_factors)
                    
                    # Categorize gustiness
                    gust_category = "unknown"
                    for cat_name, cat_range in self.gust_factor_thresholds.items():
                        cat_min = cat_range.get("min", 0)
                        cat_max = cat_range.get("max", float('inf'))
                        if cat_min <= avg_gust_factor < cat_max:
                            gust_category = cat_name
                            break
                            
                    gustiness = f"{gust_category} (gust factor: {avg_gust_factor:.2f})"
                else:
                    gustiness = "unknown"
            else:
                gustiness = "data not available"
        else:
            gustiness = "unknown"
            
        # Generate the meta-analysis
        analysis = [
            f"Overall forecast shows {category} winds averaging {avg_speed:.1f} knots.",
            f"Wind conditions are {variability} with a range of {speed_range:.1f} knots.",
            f"Gust conditions: {gustiness}."
        ]
        
        # Add recommendations based on patterns
        if any("increasing" in pattern.lower() for pattern in micro + meso + macro):
            analysis.append("Wind is expected to strengthen during the forecast period.")
        elif any("decreasing" in pattern.lower() for pattern in micro + meso + macro):
            analysis.append("Wind is expected to weaken during the forecast period.")
        else:
            analysis.append("Wind strength is expected to remain relatively steady.")
            
        if any("variable wind direction" in pattern.lower() for pattern in micro + meso + macro):
            analysis.append("Expect shifting wind directions, which may require adjustments for wind-dependent activities.")
        elif any("consistent wind direction" in pattern.lower() for pattern in micro + meso + macro):
            analysis.append("Wind direction is expected to remain consistent, favorable for planning wind-dependent activities.")
            
        # Add activity recommendations based on wind category
        if category in ["light", "moderate"]:
            analysis.append("Conditions may be suitable for a range of wind-dependent activities.")
        elif category in ["strong", "gale"]:
            analysis.append("Exercise caution with wind-dependent activities; conditions may be challenging.")
        elif category in ["storm", "hurricane"]:
            analysis.append("Dangerous wind conditions expected; avoid wind-dependent activities.")
            
        return " ".join(analysis)

    def _process_data_to_dataframe(self, data: Dict[str, Any]) -> Optional[pd.DataFrame]:
        """Convert raw forecast data to a pandas DataFrame.
        
        Args:
            data: Raw forecast data
            
        Returns:
            DataFrame containing processed forecast data, or None if data is insufficient
        """
        forecast_data = data.get('forecast_data', [])
        
        if not forecast_data:
            return None
            
        # Convert to DataFrame
        df = pd.DataFrame(forecast_data)
        
        # Convert time strings to datetime objects if possible
        if 'time' in df.columns:
            try:
                df['time'] = pd.to_datetime(df['time'])
                df.set_index('time', inplace=True)
            except Exception as e:
                _LOGGER.warning(f"Could not convert time to datetime: {e}")
                
        return df

    def _calculate_statistics(self, df: Optional[pd.DataFrame]) -> Dict[str, Any]:
        """Calculate statistics from the forecast data.
        
        Args:
            df: DataFrame containing forecast data
            
        Returns:
            Dictionary of statistics
        """
        stats = {}
        
        if df is None or df.empty:
            return stats
            
        # Calculate basic statistics for wind speed
        if 'wind_speed' in df.columns:
            stats['wind_speed'] = {
                'mean': df['wind_speed'].mean(),
                'median': df['wind_speed'].median(),
                'min': df['wind_speed'].min(),
                'max': df['wind_speed'].max(),
                'std': df['wind_speed'].std()
            }
            
        # Calculate direction statistics if available
        if 'wind_direction' in df.columns:
            direction_counts = df['wind_direction'].value_counts()
            stats['wind_direction'] = {
                'most_common': direction_counts.index[0] if not direction_counts.empty else 'unknown',
                'distribution': direction_counts.to_dict()
            }
            
        # Calculate temperature statistics if available
        if 'temperature' in df.columns:
            stats['temperature'] = {
                'mean': df['temperature'].mean(),
                'min': df['temperature'].min(),
                'max': df['temperature'].max()
            }
            
        return stats

    def analyze(self, url: str = "https://www.windguru.cz") -> WindGuruAnalysisResult:
        """Perform complete fractal analysis on winguru.cz content.
        
        Args:
            url: URL of the windguru forecast page
            
        Returns:
            WindGuruAnalysisResult containing analysis results
        """
        # Extract raw data
        raw_data = self.extract_forecast_data(url)
        
        # Convert to DataFrame for easier analysis
        df = self._process_data_to_dataframe(raw_data)
        
        # Calculate statistics
        statistics = self._calculate_statistics(df)
        
        # Analyze patterns at different scales
        micro, meso, macro = self.analyze_fractal_patterns(raw_data)
        
        # Generate meta-analysis
        meta_analysis = self.generate_meta_analysis(micro, meso, macro, raw_data)
        
        _LOGGER.info(f"Analysis complete: {len(micro)} micro patterns, {len(meso)} meso patterns, {len(macro)} macro patterns")
        
        return WindGuruAnalysisResult(
            raw_data=raw_data,
            data_frame=df,
            micro_patterns=micro,
            meso_patterns=meso,
            macro_patterns=macro,
            meta_analysis=meta_analysis,
            statistics=statistics
        )