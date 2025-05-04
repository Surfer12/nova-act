# Enhanced WindGuru Analysis Tool

This tool provides advanced wind forecasting and analysis capabilities using Nova-Act with AI integration and scientific analysis techniques.

## Key Enhanced Features

1. **Nova Premiere Integration**
   - Uses the `nova-premiere` endpoint with optimized parameters
   - Model parameter tuning for optimal extraction (temperature, top_k settings)
   - Enhanced error handling with automatic retry mechanisms

2. **Machine Learning Wind Forecasting**
   - Uses `RandomForestRegressor` models to predict wind patterns
   - Feature importance analysis to understand key weather drivers
   - 24-hour future predictions with confidence scoring
   - Model accuracy metrics and validation

3. **Fourier Analysis for Cyclical Pattern Detection**
   - Identifies natural cycles in wind, temperature, and pressure data
   - Detects diurnal (day/night), tidal, and longer-term patterns
   - Quantifies the magnitude and period of each cycle
   - Assigns confidence scores and likely sources to detected patterns

4. **Time-Series Decomposition**
   - Separates wind data into trend, seasonal, and residual components
   - Identifies overall trend direction (increasing/decreasing)
   - Measures seasonal amplitude and cyclical variations
   - Calculates volatility metrics for wind stability assessment

5. **Statistical Validation with Confidence Intervals**
   - Uses bootstrapping to generate robust confidence intervals
   - Provides precise statistical ranges for forecast reliability
   - Quantifies forecast uncertainty with 95% confidence bounds
   - Includes variance estimation for wind variability analysis

6. **Enhanced Web Automation**
   - Exponential backoff retry logic for robust data extraction
   - Parallel asynchronous data processing with `act_async()`
   - Improved error handling for more reliable web interaction
   - Graceful degradation with sensible defaults when data is missing

7. **Comprehensive Visualization and Reporting**
   - Detailed tabular data presentation
   - Statistical summaries with key metrics
   - Future forecast predictions with confidence scores
   - Cyclical pattern tables and explanations
   - JSON output for further analysis or integration

## Usage

```bash
python -m nova_act.samples.enhanced_windguru_analysis [--spot_id SPOT_ID] [--analyze_map] [--headless] [--use_premiere] [--save_analysis]
```

### Parameters

- `--spot_id`: WindGuru spot ID (default: "1207462")
- `--analyze_map`: Whether to analyze the map view (not fully implemented yet)
- `--headless`: Run in headless browser mode
- `--use_premiere`: Use Nova Premiere endpoint for enhanced analysis
- `--save_analysis`: Save analysis to JSON file (default: True)

## Examples

```bash
# Basic analysis
python -m nova_act.samples.enhanced_windguru_analysis

# Analyze specific spot with Nova Premiere
python -m nova_act.samples.enhanced_windguru_analysis --spot_id=123456 --use_premiere=True

# Run headless without saving analysis file
python -m nova_act.samples.enhanced_windguru_analysis --headless=True --save_analysis=False
```

## Output

The script generates:

1. Detailed console output with tables and analysis
2. A JSON file containing all analysis data (if save_analysis=True)
3. Logging information in windguru_enhanced_analysis.log

## Requirements

- Python 3.8+
- NovaAct library
- Additional libraries:
  - numpy
  - pandas
  - scikit-learn
  - statsmodels (optional)