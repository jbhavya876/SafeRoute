# 🛣️ SafeRoute - Route Safety Risk Analyzer

**AI-powered route safety analysis system for women commuters in metropolitan cities.**

---

## 📋 Overview

SafeRoute is an intelligent route safety analysis system that combines a Python backend with an interactive Streamlit UI. It analyzes source and destination combinations to determine route safety risk levels and provides alerts for high-risk routes.

### ✨ Key Features

- 🔍 **Route Risk Analysis** - Analyze any source-destination combination
- ⚠️ **Alert System** - Critical alerts for high-risk routes
- 🗺️ **12 Sample Locations** - Pre-loaded Delhi locations with safety data
- 📊 **Safety Dashboard** - Visualizations of safety metrics
- 🔄 **Alternative Routes** - Suggestions for safer paths
- 💚 **Risk Classification** - 6-level priority system (0=Critical, 5=Excellent)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (tested on 3.12)
- pip package manager
- Virtual environment (recommended)

### Installation

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements_streamlit_fixed.txt

# 3. Run the application
streamlit run streamlit_app.py
```

**Opens in browser:** http://localhost:8501

---

## 📦 What's Included

### Backend Files

| File | Purpose |
|------|---------|
| `risk_data.py` | 12 Delhi locations with safety metrics |
| `risk_analyzer.py` | Core analysis engine |

### Frontend Files

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Interactive UI dashboard (4 pages) |

### Configuration

| File | Purpose |
|------|---------|
| `requirements_streamlit.txt` | Python 3.12 compatible dependencies |

---

## 🎯 How It Works

### Risk Analysis System

The system analyses **source + destination safety levels** to determine route safety:

```
Source Safety Level: high/mid/low
Destination Safety Level: high/mid/low
        ↓
Risk Combination: e.g., "mid-high"
        ↓
Priority Level: 0-5
        ↓
Alert Message (if risky)
```

### 6 Priority Levels

```
0 🚨 CRITICAL - Do NOT use this route
1 ⚠️ HIGH RISK - Not recommended
2 ⚡ MODERATE - Be cautious
3 ✓ ACCEPTABLE - Recommended
4 ✅ GOOD - Highly recommended
5 🟢 EXCELLENT - Very safe route
```

---

## 🎨 UI Overview

### Page 1: Analyze Route (Main Feature)
- Select source location
- Select destination location
- Get instant risk analysis
- View color-coded alerts
- See alternative safer routes
- Check detailed metrics

### Page 2: Safety Dashboard
- Location statistics table
- Safety level distribution
- Crime density comparison
- Lighting quality overview
- Recent incidents tracking

### Page 3: Available Locations
- Browse all 12 locations
- Expandable location details
- View coordinates & police stations
- Safety metrics per location

### Page 4: Settings
- About SafeRoute
- Risk level legend
- Risk combination matrix

---

## 🗺️ Sample Locations

### HIGH Safety (🟢)
- IIT Delhi
- Vasant Kunj
- Dwarka
- Rajiv Chowk Metro
- Delhi Airport Metro

### MID Safety (🟡)
- Connaught Place
- Rohini
- South Extension
- Hauz Khas
- Noida City Center

### LOW Safety (🔴)
- Vivek Vihar
- Greater Noida

---

## 💻 Backend Usage (Python)

### Basic Example

```python
from risk_analyzer import RiskAnalyzer

analyzer = RiskAnalyzer()

# Analyze a route
result = analyzer.analyze_route("Dwarka", "Vivek Vihar")

# Check if recommended
if result["recommendation"]["is_recommended"]:
    print("✅ Route is safe")
else:
    print(f"❌ {result['recommendation']['alert_message']}")

# Get alternative routes
alternatives = analyzer.get_safe_alternatives("Vivek Vihar", "CP")
for alt in alternatives:
    print(f"Safe option: {alt['location']}")
```

### Available Methods

- `analyze_route(source, destination)` - Get risk analysis
- `get_safe_alternatives(source, destination)` - Find safer routes
- `get_available_locations()` - List all locations
- `batch_analyze(routes)` - Analyze multiple routes
- `get_risk_matrix()` - Get all combinations

---

## 📊 Example Test Routes

| Route | Result | Status |
|-------|--------|--------|
| Dwarka → Vasant Kunj | 🟢 EXCELLENT (5) | ✅ Safe |
| Vivek Vihar → Greater Noida | 🚨 CRITICAL (0) | ❌ Avoid |
| CP → Vivek Vihar | ⚡ MODERATE (2) | ⚠️ Caution |
| IIT Delhi → Dwarka | 🟢 EXCELLENT (5) | ✅ Safe |

---

## 🔧 Troubleshooting

### Python 3.12 Compatibility Error

If you get `BackendUnavailable: Cannot import 'setuptools.build_meta'`:

```bash
pip cache purge
pip install -r requirements_streamlit_fixed.txt
```

### Import Errors

Make sure all three files are in the same directory:
- `risk_data.py`
- `risk_analyzer.py`
- `streamlit_app.py`

### Streamlit Won't Start

```bash
pip install --upgrade streamlit
streamlit run streamlit_app.py
```

---

## 📚 File Structure

```
SafeRoute/
├── risk_data.py                    # Location data & metrics
├── risk_analyzer.py                # Analysis engine
├── streamlit_app.py                # UI dashboard
├── requirements_streamlit_fixed.txt # Dependencies
└── README.md                       # This file
```

---

## 🔌 Integration

### Use with Flask Backend

```python
from flask import Flask, request, jsonify
from risk_analyzer import RiskAnalyzer

app = Flask(__name__)
analyzer = RiskAnalyzer()

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    result = analyzer.analyze_route(
        data['source'], 
        data['destination']
    )
    return jsonify(result)
```

---

## 📋 Metrics

Each location includes:
- **Safety Level**: high/mid/low
- **Crime Density**: per sq km
- **Lighting Quality**: 0-100%
- **Surveillance Coverage**: 0-100%
- **Recent Incidents**: count in last month
- **Police Station**: nearest station name

---

## 🎓 Understanding Risk Levels

```
HIGH-HIGH (Source: High, Dest: High)
→ 🟢 EXCELLENT (Priority 5)
→ Very safe route - Highly Recommended

MID-MID (Source: Mid, Dest: Mid)
→ ✓ ACCEPTABLE (Priority 3)
→ Normal risk - Recommended

LOW-LOW (Source: Low, Dest: Low)
→ 🚨 CRITICAL (Priority 0)
→ Very risky - DO NOT USE

HIGH-LOW or LOW-HIGH (Mixed)
→ ⚡ MODERATE (Priority 2)
→ Mixed safety - Be Cautious
```

---

## 🚀 Next Steps

1. **Run the app** → `streamlit run streamlit_app.py`
2. **Test routes** → Try different location combinations
3. **Explore dashboard** → View safety statistics
4. **Integrate** → Use backend with your own frontend
5. **Extend** → Add more locations and metrics

---

## 💡 Features

✅ Real-time route analysis
✅ Risk classification system
✅ Critical alert generation
✅ Alternative route suggestions
✅ Safety statistics dashboard
✅ Location browsing interface
✅ Python 3.10+ compatible
✅ Production-ready code

---

## 📞 Support

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure all 3 Python files in same directory |
| Python 3.12 error | Use `requirements_streamlit_fixed.txt` |
| Streamlit won't start | Run `pip install --upgrade streamlit` |
| Import errors | Check file names and paths |


---

## 👥 Contributing

Contributions welcome! Please:
1. Test thoroughly
2. Update documentation
3. Follow existing code style

---

## 🎯 Project Status

✅ **Version 1.0** - Stable Release
- Core analysis engine
- Streamlit UI complete
- 12 test locations
- Documentation complete

---

## 📈 Future Enhancements

- [ ] Real-time incident data integration
- [ ] Machine learning safety prediction
- [ ] Google Maps integration
- [ ] Weather-based risk adjustment
- [ ] Mobile app
- [ ] User incident reporting
- [ ] Analytics dashboard

---

## 🏆 Key Achievements

✅ Complete route safety analysis system
✅ Interactive user interface
✅ Intelligent alert system
✅ 12 pre-loaded locations
✅ Production-ready code
✅ Full documentation

---

## 🎊 Quick Reference

```bash
# Install dependencies
pip install -r requirements_streamlit_fixed.txt

# Run the app
streamlit run streamlit_app.py

# Test backend
python risk_analyzer.py

# Check Python version
python --version
```

**Browser opens to:** http://localhost:8501

---

**SafeRoute v1.0** | Built with ❤️ for women's safety in metro cities
