
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
Sample script demonstrating how to use NovaAct to analyze wind forecast data from winguru.cz
using a fractal, multi-layered analysis framework.
"""

from nova_act import NovaAct 
def main():
    # Initialize NovaAct with a starting page (can be overridden later)
    nova = NovaAct(starting_page="https://www.windguru.cz")
    
    try:
        # Start the client
        nova.start()
        
        # Analyze winguru.cz content
        print("Analyzing wind forecast data from winguru.cz...")
        result = nova.analyze_winguru()
        
        # Display the analysis results
        print("\nAnalysis Results:")
        print(f"Raw Data: {result.raw_data}")
        print("\nMicro Patterns:")
        for pattern in result.micro_patterns:
            print(f"- {pattern}")
        print("\nMeso Patterns:")
        for pattern in result.meso_patterns:
            print(f"- {pattern}")
        print("\nMacro Patterns:")
        for pattern in result.macro_patterns:
            print(f"- {pattern}")
        print(f"\nMeta Analysis: {result.meta_analysis}")
    
    finally:
        # Ensure the client is stopped
        nova.stop()


if __name__ == "__main__":
    main() 