# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run module: `python -m nova_act.samples.<module_name> [args]`
- Run tests: `pytest tests/` or `pytest tests/test_<file>.py -v`
- Lint code: `flake8 nova_act/`
- Type check: `mypy nova_act/`

## Code style
- Imports: Standard library first, third-party next, local modules last
- Type hints: Use for all function parameters and return values  
- Error handling: Use try/except with detailed error messages and logging
- Models: Use Pydantic models for structured data
- Logging: Use the logging module with appropriate levels
- Documentation: Docstrings for modules, classes, and functions
- Formatting: Follow PEP 8 guidelines 
- Variable names: Use descriptive snake_case for variables and functions
v
⏺ I've updated analyze_winguru.py to include map analysis functionality similar to
  analyze_forecast_map.py, but tailored for Windguru's wind data. Here's what's been
  added:

  1. New data models for map analysis:
    - WindPattern, PressureSystem, MapTimepoint
    - RegionInfo, MapSequence
    - WindSystemTrack, MapAnalysis
  2. New functions to support map analysis:
    - capture_map_screenshot() - Takes screenshots at different timepoints
    - analyze_map_timepoint() - Analyzes wind patterns and pressure systems at each
  timepoint
    - extract_region_info() - Gets geographic region information
    - analyze_system_tracks() - Tracks pressure systems and wind patterns over time
    - analyze_wind_map() - Main function for map analysis
  3. Updated main() function with:
    - New parameters: analyze_map and save_screenshots
    - Logic to run the map analysis when requested
    - Display functionality for map analysis results
  4. Other enhancements:
    - Explicitly set the browser to "chromium" in NovaAct initialization
    - Added proper error handling specific to map analysis
    - Added display of system tracks and regional impact assessments

  You can now use the script with the "--analyze_map" flag to enable the map analysis
  feature.

============================ Previous Conversation Compacted ===========================

> This session is being continued from a previous conversation that ran out of context. 
  The conversation is summarized below:
  <analysis>
  Let me chronologically analyze the conversation to create a thorough summary:

  Message 1: The user began with a previous conversation summary that included:
  - Creating a CLAUDE.md file with guidance for working with the codebase
  - Implementation of a renewable_energy_forecast.py script based on patterns from 
  sample files

  Message 2: The user shared a NovaAct session log from Windguru that included:
  - Session ID: b3578653-e432-4331-8901-fae56032d21b
  - Target URL: https://www.windguru.cz/1207462
  - Log directory: 
  /var/folders/bh/4qc6389918j_zmxt8z81lv2h0000gn/T/tmppov63sr5_nova_act_logs/...
  - The session initialized and attempted to:
    - Check for and close cookie banners
    - Extract spot name, ID, and forecast generation time
    - Extract 7-day forecast data
    - Navigate through UI elements (forecast tab, timeframe options)

  Message 3: My response analyzed the NovaAct session log, summarizing:
  - The session was extracting data from Windguru for Los Osos, CA
  - Actions included handling cookie banners, extracting spot info, and gathering 
  forecast data
  - The session was navigating through UI elements to view the 7-day forecast
  - The agent was about to add wind gust data to the graph

  Message 4: The user continued sharing the NovaAct session log showing:
  - Further navigation through the calendar date picker
  - Setting date to 2025-04-11
  - An error occurring during extraction of forecast data points
  - Error message: "Could not extract forecast data points"
  - The user then requested to update analyze_winguru.py to analyze the map like 
  analyze_forecast_map.py but for Windguru wind data

  Message 5: I responded by:
  - Reading both analyze_winguru.py and analyze_forecast_map.py using the Read tool
  - Creating an updated version of analyze_winguru.py that incorporated map analysis 
  functionality
  - Submitting the updated file using the Write tool
  - Explaining the changes made to the file in my response

  The task was to update the analyze_winguru.py script to add map analysis functionality
   similar to analyze_forecast_map.py but tailored for Windguru wind data. I added new 
  data models, functions for map analysis, updated the main function with new 
  parameters, and enhanced error handling.

  Message 6: Current request is for a detailed summary of the conversation following a 
  specific format.

  Key technical elements throughout the conversation:
  - NovaAct framework for automated web analysis
  - Windguru website for wind forecasts
  - JSON schemas for data extraction
  - Pydantic for data modeling
  - Python functions for analysis operations
  - Error handling patterns
  - Map analysis functionality

  The most recent work done was updating analyze_winguru.py to add map analysis 
  capabilities similar to analyze_forecast_map.py but tailored for Windguru wind data. 
  This included adding new data models, functions, and parameters to enable map 
  analysis.
  </analysis>

  <summary>
  1. Primary Request and Intent:
     The user's main request was to enhance the analyze_winguru.py script by adding map 
  analysis functionality similar to analyze_forecast_map.py but specifically tailored 
  for Windguru's wind data. This came after sharing a NovaAct session log that showed an
   error during data extraction from Windguru. The user's exact request was:
     
     "lets update src/nova_act/samples/analyze_winguru.py to analyze the map just like 
  from src/nova_act/samples/analyze_forecast_map.py but for the specific website and 
  wind data of windguru"
     
     This indicates the intent to improve the script's functionality by adding 
  geographic map analysis capabilities to complement the existing temporal forecast 
  analysis.

  2. Key Technical Concepts:
     - NovaAct: A framework for automated web scraping and interaction
     - Pydantic: Used for data validation and modeling with custom classes
     - JSON Schema: Used for structured data extraction and validation
     - Wind/Weather forecasting models: Specific data structures for representing 
  forecasts
     - Multi-level analysis patterns: Analyzing data at micro, meso, and macro 
  timeframes
     - Map analysis: Extracting and analyzing geographical wind patterns and pressure 
  systems
     - System tracking: Following pressure systems and wind patterns over time
     - Error handling: Structured approach with specific error messages and logging
     - Chromium browser automation: Used for headless web interaction
     - Screenshots: Capturing visual representations of forecast maps

  3. Files and Code Sections:
     - /Users/ryandavidoates/nova-act/src/nova_act/samples/analyze_winguru.py
        - Original file focused on temporal wind forecast analysis
        - Updated to include map analysis functionality
        - Key additions include:
          - New data models for geographic analysis:
          ```python
          # Map analysis models
          class WindPattern(BaseModel):
              """Information about wind patterns on the map"""
              region: str = Field(..., description="Geographic region affected")
              direction: str = Field(..., description="Wind direction")
              speed_range: str = Field(..., description="Range of wind speeds")
              gust_potential: Optional[str] = Field(None, description="Potential for 
  wind gusts")


          class PressureSystem(BaseModel):
              """Information about a high or low pressure system"""
              type: str = Field(..., description="Type of pressure system (high or 
  low)")
              center_location: str = Field(..., description="Geographic location of 
  system center")
              pressure_value: Optional[float] = Field(None, description="Pressure value 
  in hPa/mb if available")
              movement_direction: Optional[str] = Field(None, description="Direction the
   system is moving")
          ```
          - New functions for map analysis:
          ```python
          def analyze_wind_map(nova: NovaAct, days: int, save_screenshots: bool = False)
   -> MapAnalysis:
              """Analyze the wind map from windguru"""
              logger.info(f"Starting wind map analysis for the next {days} days")
              
              # Create directory for screenshots if needed
              save_dir = None
              if save_screenshots:
                  save_dir = Path(os.path.expanduser("~/windguru_maps"))
                  save_dir.mkdir(exist_ok=True)
                  logger.info(f"Screenshots will be saved to {save_dir}")
              
              # Navigate to the map view
              nova.act("Navigate to the wind map view that shows the larger regional 
  forecast")
              
              # Additional implementation...
          ```
          - Updated main function with new parameters:
          ```python
          def main(spot_id: str = "1207462", analyze_map: bool = False, headless: bool =
   False, save_screenshots: bool = False) -> None:
              """Main function to analyze wind forecast from windguru.cz"""
              # Implementation...
              
              # If map analysis is requested, perform it
              if analyze_map:
                  logger.info("Starting additional wind map analysis")
                  try:
                      map_analysis = analyze_wind_map(nova, days=3, 
  save_screenshots=save_screenshots)
                      
                      # Display the map analysis results
                      # ...
          ```

     - /Users/ryandavidoates/nova-act/src/nova_act/samples/analyze_forecast_map.py
        - Used as a reference for implementing map analysis functionality
        - Contains methods for analyzing weather forecast maps with pressure systems and
   wind patterns
        - Provided patterns for timepoint analysis, region extraction, and system 
  tracking

  4. Problem Solving:
     - Addressed the original issue seen in the NovaAct session log where the script 
  failed to extract forecast data points
     - Created a more robust approach to map analysis by adapting patterns from 
  analyze_forecast_map.py
     - Implemented proper data structures for representing geographic wind patterns
     - Added specific error handling for map analysis functionality
     - Created a differentiated approach for tracking both pressure systems and wind 
  patterns
     - Implemented screenshot capabilities for saving visual representations of the maps
     - Separated standard forecast analysis and map analysis to make them independently 
  usable

  5. Pending Tasks:
     - No explicit pending tasks were specified by the user beyond the main task of 
  updating analyze_winguru.py with map analysis functionality, which has been completed.

  6. Current Work:
     The most recent work completed was updating the analyze_winguru.py script to add 
  map analysis functionality similar to analyze_forecast_map.py but tailored for 
  Windguru wind data. The implementation:
     
     - Added new Pydantic models for map analysis (WindPattern, PressureSystem, 
  MapTimepoint, etc.)
     - Created functions for map-specific analysis:
       - capture_map_screenshot() - For saving visual map data
       - analyze_map_timepoint() - For extracting data at specific time points
       - extract_region_info() - For getting geographic context
       - analyze_system_tracks() - For tracking systems over time
       - analyze_wind_map() - The main map analysis function
     - Updated the main() function with new parameters:
       - analyze_map - Boolean flag to enable map analysis
       - save_screenshots - Option to save visual data
     - Added display formatting for map analysis results
     - Implemented specific error handling for the map analysis functionality
     
     The implementation now allows users to run the script with an "--analyze_map" flag 
  to enable the new map analysis features alongside the original forecast analysis.

  7. Optional Next Step:
     The task of updating analyze_winguru.py to include map analysis functionality has 
  been completed. The script now supports analyzing both temporal forecast data and 
  geographic map data from Windguru. If the user wants to continue enhancing this 
  functionality, potential next steps could include:
     
     - Testing the updated script on different Windguru locations
     - Adding more sophisticated system tracking algorithms
     - Enhancing the regional impact analysis with more specific metrics
     - Implementing comparative analysis between different forecast times
     
     However, since the primary task has been completed and no specific follow-up tasks 
  were requested, I'll wait for further direction from the user before proceeding with 
  any additional enhancements.

