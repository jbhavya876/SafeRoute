"""
SafeRoute Risk Analysis - Sample Data with Safety Zones
Contains Delhi safety zone data with crime and safety metrics
"""

DELHI_SAFETY_DATA = {
    # Central Delhi - High Activity Areas
    "Connaught Place": {
        "latitude": 28.6315,
        "longitude": 77.1895,
        "safety_level": "mid",  # mid - medium safety
        "crime_density": 1.2,
        "lighting_quality": 85,
        "crowd_density": "high",
        "surveillance_coverage": 80,
        "incidents_last_month": 8,
        "police_station": "New Delhi PS",
    },
    
    # South Delhi - Residential Areas
    "Vasant Kunj": {
        "latitude": 28.5244,
        "longitude": 77.1899,
        "safety_level": "high",  # high - good safety
        "crime_density": 0.8,
        "lighting_quality": 90,
        "crowd_density": "medium",
        "surveillance_coverage": 85,
        "incidents_last_month": 2,
        "police_station": "Vasant Kunj PS",
    },
    
    # North Delhi - Institutional Areas
    "IIT Delhi": {
        "latitude": 28.5460,
        "longitude": 77.1938,
        "safety_level": "high",  # high - very safe institutional area
        "crime_density": 0.3,
        "lighting_quality": 92,
        "crowd_density": "medium",
        "surveillance_coverage": 90,
        "incidents_last_month": 1,
        "police_station": "Chhatarpur PS",
    },
    
    # East Delhi - Mixed Areas
    "Vivek Vihar": {
        "latitude": 28.5920,
        "longitude": 77.2870,
        "safety_level": "low",  # low - less safe area
        "crime_density": 2.1,
        "lighting_quality": 70,
        "crowd_density": "high",
        "surveillance_coverage": 65,
        "incidents_last_month": 12,
        "police_station": "Vivek Vihar PS",
    },
    
    # West Delhi - Suburban
    "Rohini": {
        "latitude": 28.7497,
        "longitude": 77.0437,
        "safety_level": "mid",  # mid - moderate safety
        "crime_density": 1.0,
        "lighting_quality": 82,
        "crowd_density": "medium",
        "surveillance_coverage": 75,
        "incidents_last_month": 5,
        "police_station": "Rohini PS",
    },
    
    # Metro Stations - High Security
    "Rajiv Chowk Metro": {
        "latitude": 28.6345,
        "longitude": 77.2200,
        "safety_level": "high",  # high - metro stations well secured
        "crime_density": 0.5,
        "lighting_quality": 95,
        "crowd_density": "high",
        "surveillance_coverage": 95,
        "incidents_last_month": 0,
        "police_station": "New Delhi PS",
    },
    
    # Airport Area - High Security
    "Delhi Airport Metro": {
        "latitude": 28.5631,
        "longitude": 77.0998,
        "safety_level": "high",  # high - airport security
        "crime_density": 0.4,
        "lighting_quality": 94,
        "crowd_density": "high",
        "surveillance_coverage": 92,
        "incidents_last_month": 0,
        "police_station": "IGI Airport PS",
    },
    
    # South Extension - Commercial
    "South Extension": {
        "latitude": 28.5641,
        "longitude": 77.2150,
        "safety_level": "mid",  # mid - commercial area
        "crime_density": 1.5,
        "lighting_quality": 88,
        "crowd_density": "high",
        "surveillance_coverage": 78,
        "incidents_last_month": 6,
        "police_station": "South Extension PS",
    },
    
    # Dwarka - Residential Colony
    "Dwarka": {
        "latitude": 28.5921,
        "longitude": 77.0460,
        "safety_level": "high",  # high - planned residential area
        "crime_density": 0.6,
        "lighting_quality": 91,
        "crowd_density": "low",
        "surveillance_coverage": 87,
        "incidents_last_month": 1,
        "police_station": "Dwarka PS",
    },
    
    # Greater Noida - Outskirts
    "Greater Noida": {
        "latitude": 28.4089,
        "longitude": 77.5197,
        "safety_level": "low",  # low - less populated, poor lighting
        "crime_density": 2.5,
        "lighting_quality": 60,
        "crowd_density": "low",
        "surveillance_coverage": 50,
        "incidents_last_month": 15,
        "police_station": "Greater Noida PS",
    },
    
    # Hauz Khas - Mixed Area
    "Hauz Khas": {
        "latitude": 28.5494,
        "longitude": 77.2001,
        "safety_level": "mid",  # mid - mixed residential/commercial
        "crime_density": 1.3,
        "lighting_quality": 80,
        "crowd_density": "high",
        "surveillance_coverage": 72,
        "incidents_last_month": 7,
        "police_station": "Hauz Khas PS",
    },
    
    # Noida City Center - Commercial Hub
    "Noida City Center": {
        "latitude": 28.5856,
        "longitude": 77.3597,
        "safety_level": "mid",  # mid - commercial hub
        "crime_density": 1.1,
        "lighting_quality": 86,
        "crowd_density": "high",
        "surveillance_coverage": 79,
        "incidents_last_month": 4,
        "police_station": "Noida City PS",
    },
}

# Risk Levels Mapping
RISK_LEVEL_PRIORITY = {
    "high-high": 0,      # CRITICAL - Do not recommend
    "high-mid": 1,       # CRITICAL - Do not recommend
    "high-low": 1,       # CRITICAL - Do not recommend
    "mid-high": 2,       # WARNING - Moderate risk
    "mid-mid": 3,        # ACCEPTABLE - Normal risk
    "low-high": 2,       # WARNING - Moderate risk
    "low-mid": 4,        # GOOD - Low risk
    "low-low": 5,        # EXCELLENT - Very safe
}

# Reverse mapping for display
RISK_LEVELS_DISPLAY = {
    0: "🚨 CRITICAL - Do Not Recommend",
    1: "⚠️  HIGH RISK - Not Recommended",
    2: "⚡ MODERATE RISK - Be Cautious",
    3: "✓ ACCEPTABLE RISK - Recommended",
    4: "✅ GOOD SAFETY - Highly Recommended",
    5: "🟢 EXCELLENT - Very Safe Route",
}

# Safety Level Conversion
SAFETY_TO_LEVEL = {
    "high": 0,  # high safety = low risk (0 is best)
    "mid": 1,   # mid safety = mid risk (1)
    "low": 2,   # low safety = high risk (2)
}