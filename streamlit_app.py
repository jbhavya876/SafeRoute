"""
SafeRoute - Streamlit UI for Route Safety Analysis
Interactive dashboard for analyzing route safety risks
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from risk_analyzer import RiskAnalyzer
from risk_data import DELHI_SAFETY_DATA, RISK_LEVELS_DISPLAY
import json

# Page configuration
st.set_page_config(
    page_title="SafeRoute - Route Safety Analyzer",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = RiskAnalyzer()

if 'last_analysis' not in st.session_state:
    st.session_state.last_analysis = None

# Custom CSS styling
st.markdown("""
    <style>
    .critical-alert {
        background-color: #ff4444;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        font-weight: bold;
    }
    .high-risk {
        background-color: #ff8800;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .moderate-risk {
        background-color: #ffaa00;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .acceptable {
        background-color: #00cc44;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .good {
        background-color: #00aa44;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .excellent {
        background-color: #00cc44;
        color: white;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🛣️ SafeRoute - Route Safety Risk Analyzer")
st.markdown("**Intelligent Route Safety Analysis for Women Commuters in Delhi**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📍 Navigation")
    page = st.radio(
        "Select a page:",
        ["🔍 Analyze Route", "📊 Safety Dashboard", "📋 Available Locations", "⚙️ Settings"]
    )

# Get locations list
locations = list(st.session_state.analyzer.safety_data.keys())

# PAGE 1: Analyze Route
if page == "🔍 Analyze Route":
    st.header("Analyze Route Safety Risk")
    st.markdown("Enter source and destination to get a detailed safety risk analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source = st.selectbox(
            "📍 Select Source Location",
            locations,
            key="source_select"
        )
    
    with col2:
        destination = st.selectbox(
            "📍 Select Destination Location",
            locations,
            key="dest_select",
            index=1 if len(locations) > 1 else 0
        )
    
    # Analyze button
    if st.button("🔍 Analyze Route", use_container_width=True, type="primary"):
        if source == destination:
            st.warning("⚠️ Source and destination are the same!")
        else:
            with st.spinner("Analyzing route safety..."):
                result = st.session_state.analyzer.analyze_route(source, destination)
                st.session_state.last_analysis = result
    
    # Display results
    if st.session_state.last_analysis:
        result = st.session_state.last_analysis
        
        if result["status"] == "success":
            st.divider()
            
            # Risk Alert Section
            risk_analysis = result["risk_analysis"]
            recommendation = result["recommendation"]
            priority_level = risk_analysis["priority_level"]
            
            # Display alert with appropriate styling
            if priority_level == 0:
                st.markdown("""
                    <div class="critical-alert">
                    🚨 CRITICAL ALERT<br>
                    This route combination has VERY HIGH risk. NOT RECOMMENDED.
                    </div>
                """, unsafe_allow_html=True)
            elif priority_level == 1:
                st.markdown("""
                    <div class="high-risk">
                    ⚠️ HIGH RISK ALERT<br>
                    This route has HIGH risk. NOT RECOMMENDED.
                    </div>
                """, unsafe_allow_html=True)
            elif priority_level == 2:
                st.markdown("""
                    <div class="moderate-risk">
                    ⚡ MODERATE RISK<br>
                    This route has moderate risk. Be cautious.
                    </div>
                """, unsafe_allow_html=True)
            elif priority_level == 3:
                st.markdown("""
                    <div class="acceptable">
                    ✓ ACCEPTABLE RISK<br>
                    This route has acceptable risk. Recommended.
                    </div>
                """, unsafe_allow_html=True)
            elif priority_level == 4:
                st.markdown("""
                    <div class="good">
                    ✅ GOOD SAFETY<br>
                    This route is highly safe. Recommended.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="excellent">
                    🟢 EXCELLENT SAFETY<br>
                    This is an excellent safe route. Highly recommended.
                    </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Risk Analysis Details
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Risk Combination",
                    risk_analysis["risk_combination"].upper(),
                    f"Level {priority_level}"
                )
            
            with col2:
                st.metric(
                    "Combined Risk Score",
                    f"{risk_analysis['combined_risk_score']:.1f}",
                    "out of 100"
                )
            
            with col3:
                st.metric(
                    "Source Safety",
                    risk_analysis["source_safety_level"].upper()
                )
            
            with col4:
                st.metric(
                    "Destination Safety",
                    risk_analysis["destination_safety_level"].upper()
                )
            
            st.divider()
            
            # Detailed Information
            st.subheader("📊 Detailed Route Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"📍 Source: {source}")
                source_details = result["source_details"]
                st.info(f"""
                **Safety Level:** {source_details['safety_level'].upper()}
                
                **Crime Density:** {source_details['crime_density']} per sq km
                
                **Lighting Quality:** {source_details['lighting_quality']}/100
                
                **Surveillance Coverage:** {source_details['surveillance_coverage']}%
                
                **Recent Incidents (Last Month):** {source_details['recent_incidents']}
                
                **Nearest Police Station:** {source_details['police_station']}
                """)
            
            with col2:
                st.subheader(f"📍 Destination: {destination}")
                dest_details = result["destination_details"]
                st.info(f"""
                **Safety Level:** {dest_details['safety_level'].upper()}
                
                **Crime Density:** {dest_details['crime_density']} per sq km
                
                **Lighting Quality:** {dest_details['lighting_quality']}/100
                
                **Surveillance Coverage:** {dest_details['surveillance_coverage']}%
                
                **Recent Incidents (Last Month):** {dest_details['recent_incidents']}
                
                **Nearest Police Station:** {dest_details['police_station']}
                """)
            
            st.divider()
            
            # Risk Recommendation
            st.subheader("🎯 Route Recommendation")
            if recommendation["is_recommended"]:
                st.success(f"✅ This route is **RECOMMENDED**")
            else:
                st.error(f"❌ This route is **NOT RECOMMENDED**")
                if recommendation["alert_message"]:
                    st.error(recommendation["alert_message"])
            
            # Alternative Routes
            st.divider()
            st.subheader("🔄 Safer Alternative Routes")
            
            alternatives = st.session_state.analyzer.get_safe_alternatives(source, destination)
            
            if alternatives:
                for idx, alt in enumerate(alternatives, 1):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Option {idx}: {alt['location']}**")
                    with col2:
                        st.write(f"Safety: {alt['safety_level'].upper()}")
                    with col3:
                        st.write(f"{alt['risk_description']}")
            else:
                st.info("No safer alternatives found. Consider other routes or times of travel.")
        
        else:
            st.error(f"Error: {result['message']}")
            st.info("Available locations:")
            st.write(result.get("available_locations", []))

# PAGE 2: Safety Dashboard
elif page == "📊 Safety Dashboard":
    st.header("Safety Overview Dashboard")
    
    # Location Safety Statistics
    st.subheader("📍 Location Safety Statistics")
    
    # Create safety data dataframe
    locations_data = []
    for name, info in st.session_state.analyzer.safety_data.items():
        locations_data.append({
            "Location": name,
            "Safety Level": info["safety_level"].upper(),
            "Crime Density": info["crime_density"],
            "Lighting Quality": info["lighting_quality"],
            "Surveillance": info["surveillance_coverage"],
            "Recent Incidents": info["incidents_last_month"],
        })
    
    df = pd.DataFrame(locations_data)
    
    # Display as table
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Safety Level Distribution
        safety_counts = df["Safety Level"].value_counts()
        fig1 = px.pie(
            values=safety_counts.values,
            names=safety_counts.index,
            title="Location Safety Distribution",
            color_discrete_map={"HIGH": "#00cc44", "MID": "#ffaa00", "LOW": "#ff4444"}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Crime Density Comparison
        fig2 = px.bar(
            df.sort_values("Crime Density", ascending=False),
            x="Location",
            y="Crime Density",
            title="Crime Density by Location",
            color="Crime Density",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Lighting Quality
        fig3 = px.bar(
            df.sort_values("Lighting Quality"),
            x="Location",
            y="Lighting Quality",
            title="Lighting Quality by Location",
            color="Lighting Quality",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Recent Incidents
        fig4 = px.bar(
            df.sort_values("Recent Incidents", ascending=False),
            x="Location",
            y="Recent Incidents",
            title="Recent Incidents (Last Month)",
            color="Recent Incidents",
            color_continuous_scale="Oranges"
        )
        st.plotly_chart(fig4, use_container_width=True)

# PAGE 3: Available Locations
elif page == "📋 Available Locations":
    st.header("Available Locations for Analysis")
    
    locations_info = st.session_state.analyzer.get_available_locations()
    
    st.metric("Total Locations", locations_info["total"])
    
    st.divider()
    
    # Create detailed location view
    for location_data in locations_info["locations"]:
        location_name = location_data["name"]
        info = st.session_state.analyzer.safety_data[location_name]
        
        with st.expander(f"📍 {location_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Safety Level:** {location_data['safety_level'].upper()}")
                st.write(f"**Crime Density:** {location_data['crime_density']} per sq km")
                st.write(f"**Recent Incidents:** {location_data['recent_incidents']}")
            
            with col2:
                st.write(f"**Latitude:** {info['latitude']}")
                st.write(f"**Longitude:** {info['longitude']}")
                st.write(f"**Police Station:** {info['police_station']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Lighting Quality:** {info['lighting_quality']}/100")
            with col2:
                st.write(f"**Surveillance:** {info['surveillance_coverage']}%")
            with col3:
                st.write(f"**Crowd Density:** {info['crowd_density']}")

# PAGE 4: Settings
elif page == "⚙️ Settings":
    st.header("Settings & Information")
    
    st.subheader("About SafeRoute")
    st.info("""
    **SafeRoute** is an AI-powered safety navigation system designed for women commuters in metropolitan cities.
    
    ### Features:
    - 🔍 Route safety risk analysis
    - 📊 Location-based safety metrics
    - ⚠️ Risk level alerts
    - 🔄 Alternative route suggestions
    
    ### Risk Levels:
    - 🚨 **Critical (0):** Do not use this route
    - ⚠️ **High Risk (1):** Not recommended
    - ⚡ **Moderate Risk (2):** Be cautious
    - ✓ **Acceptable (3):** Normal risk
    - ✅ **Good (4):** Highly recommended
    - 🟢 **Excellent (5):** Very safe route
    """)
    
    st.divider()
    
    st.subheader("Risk Level Matrix Legend")
    
    risk_matrix = {
        "high-high": "🟢 EXCELLENT - Very safe endpoints",
        "high-mid": "✅ GOOD - Safe start, moderate destination",
        "high-low": "⚡ MODERATE - Safe start, unsafe destination",
        "mid-high": "✅ GOOD - Moderate start, safe destination",
        "mid-mid": "✓ ACCEPTABLE - Both moderate safety",
        "mid-low": "⚡ MODERATE - Moderate start, unsafe destination",
        "low-high": "✅ GOOD - Unsafe start, safe destination",
        "low-mid": "⚡ MODERATE - Unsafe start, moderate destination",
        "low-low": "🚨 CRITICAL - Both unsafe endpoints",
    }
    
    for combo, description in risk_matrix.items():
        st.write(f"**{combo.upper()}**: {description}")

# Footer
st.divider()
st.markdown("""
---
**SafeRoute v1.0** | Designed for Women Safety in Metro Cities | Built with ❤️ for Safe Travel
""")