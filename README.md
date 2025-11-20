# IWST - Isamgeo Wellbore Stability Tool

[![Version](https://img.shields.io/badge/version-0.1dev5-blue.svg)](https://github.com/manuelmorlin/IWST)
[![Python](https://img.shields.io/badge/python-3.12+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](https://isamgeo.com)

**IWST** (Isamgeo Wellbore Stability Tool) is an advanced web application for wellbore stability analysis, designed to optimize the planning and execution of drilling operations in geotechnical and petroleum engineering contexts.

🌐 **Live app:** [https://iwst.isamgeo.com/login](https://iwst.isamgeo.com/login)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technical Capabilities](#-technical-capabilities)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Analysis Tools](#-analysis-tools)
- [Technologies](#-technologies)
- [Authors](#-authors)

---

## 🎯 Overview

IWST is a professional tool designed for geotechnical and petroleum engineers that enables wellbore stability analysis through advanced stress distribution simulations. The application calculates and visualizes:

- **Radial and tangential stresses** around the wellbore wall
- **Mohr-Coulomb analysis** to assess failure risk
- **Polar plots** to identify optimal well orientations
- **Breakout predictions** and **tensile fractures**

---

## ✨ Key Features

### 🔐 Authentication System
- Secure login with user and permission management
- Support for evaluation and full access users
- Logout system with session management
- Authentication based on Flask-Login and bcrypt

### 📊 Interactive Analysis
- **3 main visualization modules:**
  1. **Interactive Borehole Stress and Mohr-Coulomb Plot** - Wellbore wall stress analysis
  2. **Breakouts Polar Plot** - Collapse zone prediction
  3. **Tensile Fracture Polar Plot** - Tensile failure analysis

### 💾 Project Management
- Project creation, saving, and loading
- Recent projects history (last 5)
- Detailed description for each project
- MongoDB database integration for data persistence
- Visual indicator for unsaved projects (asterisk in title)

### 🎨 Modern User Interface
- Responsive design with Dash Mantine Components
- Sidebar with real-time parametric inputs
- Toolbar with File and Help menus
- Real-time notifications for operations and validations
- Info drawer with embedded theoretical documentation

### 📈 Advanced Visualizations
- Interactive charts with Plotly
- Chart download in image format
- Custom legends and well status indicators
- Loading indicators during calculations

---

## 🔧 Technical Capabilities

### Input Parameters
The application allows configuration of the following geotechnical parameters:

- **σ₁, σ₂, σ₃** - Principal stresses (MPa)
- **Pₚ** - Pore pressure (MPa)
- **Pₘ** - Mud pressure (MPa)
- **ν** - Poisson's ratio
- **δ** - Azimuth (degrees)
- **ϕ** - Inclination angle (0-90 degrees)
- **Friction coefficient**
- **UCS** - Unconfined Compressive Strength (MPa)
- **T₀** - Tensile Strength (MPa)

### Input Validation
- Real-time validation of entered values
- Notifications for missing or incorrect inputs
- Automatic button disabling with invalid inputs
- Red borders to highlight problematic fields

### Geomechanical Calculations
The application implements advanced algorithms for:

- **Stress and rotation matrix calculation**
- **Coordinate transformations** for deviated wells
- **Radial, tangential, and axial stresses** at wellbore wall
- **Mohr-Coulomb analysis** for failure prediction
- **Hemispherical polar plots** for directional analysis

---

## 🏗️ Architecture

### Project Structure

```
IWST/
├── src/iwst/
│   ├── app.py              # Main Dash application
│   ├── wsgi.py             # WSGI server entry point (Gunicorn)
│   ├── routes/
│   │   ├── home/           # Main route with all tools
│   │   │   ├── callbacks.py
│   │   │   ├── layout.py
│   │   │   ├── components/
│   │   │   │   ├── sidebar.py      # Input parameters panel
│   │   │   │   ├── toolbar.py      # Menu and project management
│   │   │   │   ├── tabs.py         # Tabs with charts
│   │   │   │   └── placeholder.py
│   │   │   ├── utils/
│   │   │   │   ├── borehole_stress.py      # Wellbore stress calculations
│   │   │   │   ├── polar_plot_borehole.py  # Breakouts polar plots generation
│   │   │   │   ├── polar_tensile.py        # Tensile polar plots generation
│   │   │   │   ├── defaults.py             # Default values
│   │   │   │   └── utils.py                # Various utilities
│   │   │   └── data/                       # Theoretical documentation
│   │   └── homeevaluation/                 # Route for evaluation users
│   ├── utils/
│   │   ├── config.py       # Configuration management
│   │   ├── login.py        # Authentication system
│   │   └── logging.py      # MongoDB logging
│   ├── static/             # Static assets (CSS, JS, images)
│   ├── templates/          # HTML templates for login
│   └── tools/
│       └── cmd.py          # Command line interface
├── setup.py
├── setup.cfg
├── pyproject.toml
└── README.md
```

### Technology Stack

**Backend:**
- **Flask** - Web framework
- **Dash** - Framework for analytical applications
- **Flask-Login** - Authentication management
- **Flask-Bcrypt** - Password hashing

**Frontend:**
- **Dash Mantine Components** - UI Components
- **Plotly** - Interactive charts
- **Dash Iconify** - Icons

**Database:**
- **MongoDB** (PyMongo) - Project data persistence and logging

**Scientific Computing:**
- **NumPy** - Numerical computations
- **SciPy** - Scientific algorithms
- **Pandas** - Data manipulation

**Deployment:**
- **Gunicorn** - WSGI HTTP Server for production
- **Kaleido** - Static chart export

---

## 🚀 Installation

### Prerequisites

- Python 3.12 or higher
- MongoDB (for data persistence)
- pip and setuptools

### Installation from Source

```bash
# Clone the repository
git clone https://github.com/manuelmorlin/IWST.git
cd IWST

# Install dependencies
pip install -e .

# Or with setup.py
python setup.py install
```

### Configuration

1. Create a configuration file `iwst.conf` (example in `src/iwst/test/iwst.conf`)
2. Configure:
   - MongoDB credentials
   - Users and permissions
   - Email parameters for notifications
   - Secret keys

---

## 💻 Usage

### Development Mode

```bash
# Using the CLI command
iwst --config path/to/iwst.conf

# Or directly with Python
python -m iwst.app
```

### Production Mode with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 iwst.wsgi:application
```

### Accessing the Application

1. Open browser and navigate to `https://iwst.isamgeo.com/login`
2. Enter user credentials
3. Access the main dashboard

### Typical Workflow

1. **Enter geotechnical parameters** in the sidebar
2. **Click "Generate plots"** to run calculations
3. **Analyze charts** in the three available tabs
4. **Save project** from the File menu
5. **Download charts** for reports and documentation

---

## 📊 Analysis Tools

### 1. Borehole Stress Plot
Displays the variation of radial (σᵣᵣ) and tangential (σθθ) stresses as a function of azimuthal angle around the wellbore wall. Allows to:
- Identify stress concentration zones
- Predict where **breakouts** may form (σθθ peaks)
- Identify risks of **tensile fractures** (σθθ minimums)

### 2. Mohr-Coulomb Plot
Represents the three principal stresses (tangential, axial, and radial) as three-dimensional Mohr circles:
- The black line is the **Mohr-Coulomb failure envelope**
- If a circle intersects the line, it indicates the rock is near collapse
- Essential for **mud weight design** during drilling

### 3. Breakouts Polar Plot
Hemispherical polar plot showing the **required UCS** to prevent breakouts as a function of well orientation:
- **Red**: unstable orientations (high strength required)
- **Blue**: stable orientations (low strength required)
- Useful for **optimizing well trajectory**

### 4. Tensile Fracture Polar Plot
Hemispherical polar plot illustrating the **required mud pressure** to initiate tensile fractures:
- **Red**: orientations where fractures are more likely
- **Blue**: relatively safe orientations
- Critical for defining **upper limits of mud weight**

---

## 🛠️ Technologies

### Main Dependencies (from `setup.cfg`)

```
dash
dash-mantine-components
dash-ag-grid
dash-iconify
plotly
numpy
scipy
pandas
gunicorn
pymongo
kaleido
pyyaml
flask
flask-login
flask_security
flask-bcrypt
rich
matplotlib
```

### Python Version
Python >= 3.12

### Supported Browsers
- Chrome (recommended)
- Safari
- Edge
- **Note:** Firefox is not currently supported

---

## 👥 Authors

**Author:** Manuel Morlin  
**Email:** manuel.morlin@isamgeo.com  
**Organization:** Isamgeo  
**Role:** Developer

---

## 📝 Versions and Changelog

**Current Version:** 0.1dev5

For the complete changelog, see [CHANGELOG.md](CHANGELOG.md)

### Latest Changes (0.1dev5)
- UX improvements and notifications
- Advanced input validation system
- Optimized chart download
- Info drawer with theoretical documentation
- Integrated email support system

---

## 📄 License

Proprietary - © Isamgeo. All rights reserved.

---

## 🔗 Useful Links

- **Web Application:** [https://iwst.isamgeo.com/login](https://iwst.isamgeo.com/login)
- **Repository:** [https://github.com/manuelmorlin/IWST](https://github.com/manuelmorlin/IWST)
- **Dash Documentation:** [https://dash.plotly.com/](https://dash.plotly.com/)
- **Plotly:** [https://plotly.com/python/](https://plotly.com/python/)

---

## 📧 Support

For technical support or feature requests, contact:
- Email: manuel.morlin@isamgeo.com
- Use the integrated support system in the application (Help menu → Contact Support)