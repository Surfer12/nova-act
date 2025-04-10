fractal-browser/
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── fractal/
│   │   │           ├── browser/
│   │   │           │   ├── core/
│   │   │           │   │   ├── BifurcationPoint.java
│   │   │           │   │   ├── FractalProcessor.java
│   │   │           │   │   └── NovaActClient.java
│   │   │           │   ├── processing/
│   │   │           │   │   ├── MultiScaleProcessor.java
│   │   │           │   │   └── ProcessingLevel.java
│   │   │           │   └── collections/
│   │   │           │       └── FractalHashMap.java
│   │   │   └── resources/
│   │   │       └── application.properties
│   │   └── python/
│   │       ├── nova_act/
│   │       │   ├── __init__.py
│   │       │   ├── core/
│   │       │   │   ├── __init__.py
│   │       │   │   ├── bifurcation.py
│   │       │   │   └── processor.py
│   │       │   ├── processing/
│   │       │   │   ├── __init__.py
│   │       │   │   └── multi_scale.py
│   │       │   └── utils/
│   │       │       ├── __init__.py
│   │       │       └── fractal_map.py
│   └── test/
│       ├── java/
│       │   └── com/
│       │       └── fractal/
│       │           └── browser/
│       │               ├── core/
│       │               └── processing/
│       └── python/
│           └── nova_act/
│               ├── test_bifurcation.py
│               └── test_processor.py
├── build/
├── dist/
├── requirements.txt
├── setup.py
├── pom.xml
└── docs/
    ├── java/
    └── python/
- README.md: Project documentation
- LICENSE: Project license
- .gitignore: Git ignore rules
- pom.xml: Maven build configuration for Java
- requirements.txt: Python dependencies
- setup.py: Python package configuration
src/main/java/: Java source code
src/main/python/: Python source code
src/main/resources/: Configuration files
com.fractal.browser.core: Core interfaces and models
com.fractal.browser.processing: Processing implementations
com.fractal.browser.collections: Custom collections
nova_act/core/: Core functionality
nova_act/processing/: Processing implementations
nova_act/utils/: Utility functions and classes
src/test/java/: Java unit tests
src/test/python/: Python unit tests
mvn clean install  # Build Java components
mvn test          # Run Java tests
pip install -e .  # Install package in development mode
pytest           # Run Python tests
