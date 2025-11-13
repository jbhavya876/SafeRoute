"""
SafeRoute Risk Analyzer - Backend Script
Analyzes source and destination combinations for route safety risk levels
"""

from risk_data import DELHI_SAFETY_DATA, RISK_LEVEL_PRIORITY, RISK_LEVELS_DISPLAY, SAFETY_TO_LEVEL
from datetime import datetime
import json

class RiskAnalyzer:
    """Analyzes safety risks for routes"""
    
    def __init__(self, safety_data=DELHI_SAFETY_DATA):
        """Initialize with safety data"""
        self.safety_data = safety_data
        self.analysis_log = []
    
    def get_location_info(self, location_name):
        """Get safety information for a location"""
        if location_name not in self.safety_data:
            return None
        return self.safety_data[location_name]
    
    def get_safety_level(self, location_name):
        """Get safety level for a location"""
        info = self.get_location_info(location_name)
        if info:
            return info.get("safety_level", "mid")
        return None
    
    def analyze_route(self, source, destination):
        """
        Analyze risk level for a route between source and destination
        
        Returns:
            dict: Analysis result with risk level, priority, and details
        """
        # Get location information
        source_info = self.get_location_info(source)
        dest_info = self.get_location_info(destination)
        
        # Check if locations exist
        if not source_info or not dest_info:
            missing = []
            if not source_info:
                missing.append(source)
            if not dest_info:
                missing.append(destination)
            
            return {
                "status": "error",
                "message": f"Location(s) not found: {', '.join(missing)}",
                "available_locations": list(self.safety_data.keys()),
            }
        
        # Get safety levels
        source_safety = source_info.get("safety_level", "mid")
        dest_safety = dest_info.get("safety_level", "mid")
        
        # Create risk combination key
        risk_key = f"{source_safety}-{dest_safety}"
        
        # Get priority and recommendation
        priority_level = RISK_LEVEL_PRIORITY.get(risk_key, 3)
        risk_description = RISK_LEVELS_DISPLAY.get(priority_level, "Unknown Risk")
        
        # Determine if route is recommended
        is_recommended = priority_level >= 3
        alert_message = None
        
        if not is_recommended:
            if priority_level == 0:
                alert_message = f"🚨 CRITICAL ALERT: Route from {source} to {destination} has VERY HIGH risk. NOT RECOMMENDED."
            elif priority_level == 1:
                alert_message = f"⚠️  HIGH ALERT: Route from {source} to {destination} has HIGH risk. NOT RECOMMENDED."
        
        # Calculate combined risk score (0-100)
        source_risk_score = SAFETY_TO_LEVEL.get(source_safety, 1) * 33
        dest_risk_score = SAFETY_TO_LEVEL.get(dest_safety, 1) * 33
        combined_risk = ((source_risk_score + dest_risk_score) / 2) / 66 * 100
        combined_risk = min(100, max(0, combined_risk))
        
        # Build detailed analysis
        analysis = {
            "status": "success",
            "route": {
                "source": source,
                "destination": destination,
            },
            "risk_analysis": {
                "source_safety_level": source_safety,
                "destination_safety_level": dest_safety,
                "risk_combination": risk_key,
                "priority_level": priority_level,
                "risk_description": risk_description,
                "combined_risk_score": round(combined_risk, 2),
            },
            "recommendation": {
                "is_recommended": is_recommended,
                "alert_message": alert_message,
                "priority_level": priority_level,
            },
            "source_details": {
                "name": source,
                "safety_level": source_safety,
                "crime_density": source_info.get("crime_density"),
                "lighting_quality": source_info.get("lighting_quality"),
                "surveillance_coverage": source_info.get("surveillance_coverage"),
                "recent_incidents": source_info.get("incidents_last_month"),
                "police_station": source_info.get("police_station"),
            },
            "destination_details": {
                "name": destination,
                "safety_level": dest_safety,
                "crime_density": dest_info.get("crime_density"),
                "lighting_quality": dest_info.get("lighting_quality"),
                "surveillance_coverage": dest_info.get("surveillance_coverage"),
                "recent_incidents": dest_info.get("incidents_last_month"),
                "police_station": dest_info.get("police_station"),
            },
            "timestamp": datetime.now().isoformat(),
        }
        
        return analysis
    
    def get_safe_alternatives(self, source, destination):
        """Get alternative routes with better safety"""
        # Get source location
        source_info = self.get_location_info(source)
        if not source_info:
            return []
        
        # Find all high-safety destinations from source
        alternatives = []
        source_safety = source_info.get("safety_level", "mid")
        
        for location_name, location_info in self.safety_data.items():
            if location_name == source or location_name == destination:
                continue
            
            dest_safety = location_info.get("safety_level", "mid")
            risk_key = f"{source_safety}-{dest_safety}"
            priority_level = RISK_LEVEL_PRIORITY.get(risk_key, 3)
            
            # Include if priority is acceptable or better
            if priority_level >= 3:
                alternatives.append({
                    "location": location_name,
                    "safety_level": dest_safety,
                    "priority_level": priority_level,
                    "risk_description": RISK_LEVELS_DISPLAY.get(priority_level),
                    "crime_density": location_info.get("crime_density"),
                    "surveillance_coverage": location_info.get("surveillance_coverage"),
                })
        
        # Sort by priority level (descending)
        alternatives.sort(key=lambda x: x["priority_level"], reverse=True)
        
        return alternatives[:5]  # Return top 5
    
    def batch_analyze(self, routes):
        """Analyze multiple routes at once"""
        results = []
        for source, destination in routes:
            result = self.analyze_route(source, destination)
            results.append(result)
        return results
    
    def get_available_locations(self):
        """Get list of all available locations"""
        return {
            "total": len(self.safety_data),
            "locations": [
                {
                    "name": name,
                    "safety_level": info.get("safety_level"),
                    "crime_density": info.get("crime_density"),
                    "incidents_last_month": info.get("incidents_last_month"),
                }
                for name, info in self.safety_data.items()
            ]
        }
    
    def get_risk_matrix(self):
        """Get risk level matrix for all combinations"""
        locations = list(self.safety_data.keys())
        matrix = {}
        
        for source in locations:
            matrix[source] = {}
            for destination in locations:
                if source == destination:
                    risk_key = "same-location"
                    priority = 5
                else:
                    result = self.analyze_route(source, destination)
                    if result.get("status") == "success":
                        risk_key = result["risk_analysis"]["risk_combination"]
                        priority = result["risk_analysis"]["priority_level"]
                    else:
                        continue
                
                matrix[source][destination] = {
                    "risk_combination": risk_key,
                    "priority_level": priority,
                    "is_recommended": priority >= 3,
                }
        
        return matrix


# Example usage and testing
if __name__ == "__main__":
    analyzer = RiskAnalyzer()
    
    # Test routes
    test_routes = [
        ("Connaught Place", "Vasant Kunj"),       # mid-high
        ("Vivek Vihar", "Greater Noida"),         # low-low (CRITICAL)
        ("IIT Delhi", "Dwarka"),                  # high-high (EXCELLENT)
        ("Connaught Place", "Vivek Vihar"),       # mid-low (HIGH RISK)
    ]
    
    print("SafeRoute Risk Analysis - Test Results")
    print("=" * 70)
    
    for source, destination in test_routes:
        result = analyzer.analyze_route(source, destination)
        print(f"\n{'='*70}")
        print(f"Route: {source} → {destination}")
        print(f"{'='*70}")
        
        if result["status"] == "success":
            analysis = result["risk_analysis"]
            recommendation = result["recommendation"]
            
            print(f"Risk Combination: {analysis['risk_combination']}")
            print(f"Risk Description: {analysis['risk_description']}")
            print(f"Combined Risk Score: {analysis['combined_risk_score']}/100")
            print(f"Recommended: {'✓ YES' if recommendation['is_recommended'] else '✗ NO'}")
            
            if recommendation['alert_message']:
                print(f"\n{recommendation['alert_message']}")
        else:
            print(f"Error: {result['message']}")