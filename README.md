# Financial Health Assessment Tool for SMEs

A comprehensive AI-powered platform for analyzing financial health, creditworthiness, and providing actionable recommendations for Small and Medium Enterprises (SMEs).

## 🎯 Project Overview

This tool provides:
- **Financial Analysis**: Comprehensive metrics including liquidity, profitability, and leverage ratios
- **Creditworthiness Assessment**: AI-powered scoring system (0-100)
- **Risk Evaluation**: Low, Medium, High, and Critical risk categories
- **Smart Recommendations**: Cost optimization, financial product suggestions, and action plans
- **Multi-format Reports**: PDF, Excel, and JSON export capabilities
- **Multilingual Support**: English and Hindi interfaces
- **Tax Compliance Tracking**: GST and income tax compliance checking
- **Industry Benchmarking**: Comparison against industry standards

## 📋 Features

### Backend Features
✅ RESTful API with 15+ endpoints
✅ Financial data processing (CSV, XLSX, PDF)
✅ Advanced financial ratio calculations
✅ Industry-specific analysis and benchmarking
✅ Working capital optimization
✅ Cash flow analysis
✅ Debt management insights
✅ Tax compliance assessment
✅ Professional report generation
✅ Multilingual API responses

### Frontend Features
✅ Interactive dashboard with statistics
✅ Real-time financial analysis visualizations
✅ Business comparison tools
✅ File upload and processing
✅ Multiple report formats (PDF, Excel, JSON)
✅ Responsive Bootstrap design
✅ Language switching (English/Hindi)
✅ Risk assessment visualization
✅ Industry analysis charts

## 🏗️ Project Structure

```
Financial_Health_Assessment_Tool/
├── backend/
│   ├── app.py                      # Flask API server
│   ├── analysis.py                 # Financial analysis module
│   ├── data_loader.py              # Data processing & validation
│   ├── recommendation.py           # AI recommendations engine
│   ├── report_generator.py         # Report generation
│   ├── translations.py             # Multilingual support
│   ├── requirements.txt            # Python dependencies
│   └── SME_Financial_Health_Dataset.csv  # Sample data
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.js       # Top navigation bar
│   │   │   ├── Dashboard.js        # Main dashboard
│   │   │   ├── AnalysisPanel.js    # Financial analysis display
│   │   │   ├── RecommendationsPanel.js  # Recommendations display
│   │   │   ├── FileUpload.js       # File upload functionality
│   │   │   └── ReportGenerator.js  # Report generation UI
│   │   ├── App.js                  # Main app component
│   │   ├── App.css                 # Styling
│   │   └── index.js                # Entry point
│   ├── public/
│   └── package.json
│
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Flask server**
   ```bash
   python app.py
   ```
   
   Server will run at: `http://127.0.0.1:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the React development server**
   ```bash
   npm start
   ```
   
   Application will open at: `http://localhost:3000`

## 📊 Key Metrics Calculated

### Liquidity Ratios
- Current Ratio = Current Assets / Current Liabilities
- Quick Ratio = (Current Assets - Inventory) / Current Liabilities

### Profitability Ratios
- Profit Margin = (Net Profit / Revenue) × 100
- ROA = (Net Profit / Total Assets) × 100
- ROE = (Net Profit / Equity) × 100

### Leverage Ratios
- Debt-to-Equity = Total Liabilities / Equity
- Debt Ratio = Total Liabilities / Total Assets
- DSCR = Operating Cash Flow / Debt Obligations

### Efficiency Ratios
- Asset Turnover = Revenue / Total Assets
- Days Inventory Outstanding
- Days Sales Outstanding

### Working Capital Metrics
- Working Capital = Current Assets - Current Liabilities
- Cash Conversion Cycle
- Operating Cash Flow

## 🔌 API Endpoints

### Health & Documentation
- `GET /api/health` - API health check
- `GET /api/docs` - API documentation

### Analysis
- `GET /api/analysis/<business_id>` - Get complete analysis for a business
- `GET /api/businesses` - List all businesses
- `POST /api/batch-analysis` - Analyze multiple businesses

### Reports
- `GET /api/report/pdf/<business_id>` - Download PDF report
- `GET /api/report/excel/<business_id>` - Download Excel report
- `GET /api/report/json/<business_id>` - Get JSON report

### Data Management
- `POST /api/upload` - Upload and analyze financial data file
- `GET /api/dashboard` - Get dashboard metrics

### Multilingual
- `GET /api/languages` - Supported languages
- `GET /api/translate/<key>` - Translate a key

## 📈 Financial Health Scoring

The tool calculates a comprehensive health score (0-100) based on:

1. **Liquidity (20%)** - Current ratio, quick ratio
2. **Leverage (20%)** - Debt-to-equity, DSCR
3. **Profitability (20%)** - Profit margins, ROA, ROE
4. **Debt Servicing (20%)** - DSCR assessment
5. **Returns (20%)** - Shareholder returns (ROE)

### Risk Categories
- **Low Risk** (80-100): Excellent financial health
- **Medium Risk** (60-79): Adequate financial health with areas for improvement
- **High Risk** (40-59): Significant financial concerns
- **Critical Risk** (0-39): Severe financial distress

## 💼 Recommended Financial Products

Based on creditworthiness score:

| Score Range | Products |
|-------------|----------|
| 80+ | All products eligible |
| 70-79 | Term Loan, Equipment Financing, Trade Credit |
| 60-69 | Equipment Financing, Invoice Discounting |
| 50-59 | Working Capital Loan, Invoice Discounting |
| 45-49 | Business Credit Card |

## 🌍 Multilingual Support

Currently supported languages:
- **English** (en)
- **Hindi** (hi)

Add more languages by updating `backend/translations.py`

## 📁 Supported File Formats

- **CSV** (.csv) - Comma-separated values
- **Excel** (.xlsx, .xls) - Microsoft Excel spreadsheets
- **PDF** - Text-based exports (requires manual conversion to CSV/Excel)

### Required Data Columns
```
business_id
industry_type
annual_revenue
total_expenses
current_assets
current_liabilities
total_assets
total_liabilities
gst_compliance_status
```

## 🔐 Security Features

- ✅ CORS enabled for secure cross-origin requests
- ✅ Data validation for all inputs
- ✅ Error handling and logging
- ✅ File upload restrictions (16MB max)
- ✅ Sensitive financial data handling
- ✅ HTTPS ready (for production)

## 📝 Sample API Request

```bash
# Get analysis for a business
curl -X GET "http://127.0.0.1:5000/api/analysis/SME_1?language=en"

# Upload and analyze file
curl -X POST "http://127.0.0.1:5000/api/upload" \
  -F "file=@financial_data.csv"

# Download PDF report
curl -X GET "http://127.0.0.1:5000/api/report/pdf/SME_1" \
  -o SME_1_report.pdf
```

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Mode Ready**: Bootstrap theming support
- **Interactive Charts**: Using Chart.js
- **Real-time Updates**: Live financial calculations
- **Search & Filter**: Business lookup functionality
- **Export Options**: Multiple report formats

## 📊 Data Visualization

Charts included:
- Financial metrics bar charts
- Risk distribution pie charts
- Industry comparison charts
- Ratio trend analysis
- Working capital analysis

## 🔍 Industry-Specific Analysis

Benchmarks for:
- Manufacturing
- Retail
- Services
- Logistics
- E-commerce
- Agriculture

Each industry has specific benchmarks for:
- Current Ratio
- Quick Ratio
- Debt-to-Equity
- Profit Margin
- Asset Turnover
- ROE

## 📚 Technology Stack

### Backend
- **Framework**: Flask
- **Data Processing**: Pandas
- **Report Generation**: ReportLab
- **Excel Export**: openpyxl
- **Data Validation**: Pydantic
- **HTTP**: RESTful API

### Frontend
- **Library**: React.js
- **Styling**: CSS3 + Bootstrap 5
- **Charts**: Chart.js
- **HTTP Client**: Fetch API
- **State Management**: React Hooks

### Database (Optional for Production)
- PostgreSQL (recommended)

## 🧪 Testing

### Test the API
```bash
# Health check
curl http://127.0.0.1:5000/api/health

# Get businesses
curl http://127.0.0.1:5000/api/businesses

# Get specific business analysis
curl http://127.0.0.1:5000/api/analysis/SME_1
```

## 📖 Usage Examples

### Example 1: Analyze a Business
```javascript
// Frontend
const response = await fetch('http://127.0.0.1:5000/api/analysis/SME_1');
const data = await response.json();
console.log(data.data.analysis);
```

### Example 2: Upload Financial Data
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://127.0.0.1:5000/api/upload', {
  method: 'POST',
  body: formData
});
```

### Example 3: Generate Report
```javascript
// Download PDF
window.location.href = 'http://127.0.0.1:5000/api/report/pdf/SME_1';

// Get JSON report
const response = await fetch('http://127.0.0.1:5000/api/report/json/SME_1');
```

## 🐛 Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `app.py`
- **Module not found**: Reinstall dependencies: `pip install -r requirements.txt`
- **CORS error**: Ensure Flask-CORS is installed

### Frontend Issues
- **Dependencies not installed**: Run `npm install`
- **API not responding**: Ensure backend is running on port 5000
- **Port 3000 in use**: Kill process or use different port: `PORT=3001 npm start`

## 🚀 Deployment

### Production Deployment (Backend)
```bash
# Use Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Production Deployment (Frontend)
```bash
# Build for production
npm run build

# Deploy the 'build' folder to your hosting
```

## 📞 Support & Contributing

For issues or contributions, please create an issue or pull request in the repository.

## 📄 License

This project is open source and available under the MIT License.

## 🎓 Educational Use

This tool is designed for:
- SME financial management
- Credit decision making
- Financial planning
- Business analysis
- Educational purposes

## 📊 Report Contents

Each generated report includes:
- Executive summary
- Financial metrics overview
- Ratio analysis
- Risk assessment
- Creditworthiness score
- Recommended actions
- Suitable financial products
- Industry benchmarking
- Tax compliance status
- Action plan (immediate, short-term, medium-term, long-term)

## 🔄 Updates & Maintenance

- Regular security updates
- Enhanced financial algorithms
- New industry support
- Additional language support
- Performance optimizations

---

**Version**: 1.0.0  
**Last Updated**: February 2024  
**Status**: Production Ready ✅
