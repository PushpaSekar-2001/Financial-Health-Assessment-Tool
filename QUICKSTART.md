# Quick Start Guide - Financial Health Assessment Tool

## 5-Minute Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Step 1: Clone/Navigate to Project
```bash
cd Financial_Health_Assessment_Tool
```

### Step 2: Start Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
python app.py
```
✅ Backend running at: `http://127.0.0.1:5000`

### Step 3: Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```
✅ Frontend running at: `http://localhost:3000`

### Step 4: Access Application
Open your browser and go to: **http://localhost:3000**

---

## First Actions to Try

### 1. View Dashboard
- Click on **Dashboard** tab
- See all businesses and their financial health scores
- Click **Analyze** on any business

### 2. Analyze a Business
- Go to **Analysis** tab after analyzing
- View comprehensive financial metrics
- Check ratios and financial health assessment

### 3. Get Recommendations
- Click **Recommendations** tab
- See AI-powered suggestions
- Review action plans

### 4. Generate Reports
- Go to **Reports** tab
- Download PDF or Excel report
- View JSON data

### 5. Upload Your Data
- Click **Upload** tab
- Upload CSV or Excel file with your data
- Instant analysis of your business data

---

## Sample Data Format

If uploading a CSV file, use this format:

```csv
business_id,industry_type,annual_revenue,total_expenses,current_assets,current_liabilities,total_assets,total_liabilities,gst_compliance_status
SME_100,Manufacturing,5000000,3500000,1500000,800000,8000000,3000000,Compliant
SME_101,Retail,2000000,1800000,600000,400000,2500000,1200000,Compliant
```

---

## API Quick Reference

### Get Analysis
```bash
curl http://127.0.0.1:5000/api/analysis/SME_1
```

### List Businesses
```bash
curl http://127.0.0.1:5000/api/businesses
```

### Upload File
```bash
curl -F "file=@data.csv" http://127.0.0.1:5000/api/upload
```

### Download PDF Report
```bash
curl http://127.0.0.1:5000/api/report/pdf/SME_1 -o report.pdf
```

---

## Common Issues & Solutions

### Issue: "Connection refused" on port 5000
**Solution**: Ensure backend is running
```bash
cd backend
python app.py
```

### Issue: npm packages not found
**Solution**: Install dependencies
```bash
cd frontend
npm install
```

### Issue: Business not found
**Solution**: Check the business_id is correct
```bash
curl http://127.0.0.1:5000/api/businesses
```

### Issue: Port 3000 already in use
**Solution**: Use different port
```bash
PORT=3001 npm start
```

### Issue: Python module not found
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

---

## Feature Highlights

### 📊 Dashboard
- View all businesses at a glance
- Risk distribution charts
- Industry breakdown
- Quick search functionality

### 📈 Analysis
- Comprehensive financial metrics
- Liquidity, profitability, leverage ratios
- Working capital analysis
- Efficiency metrics

### 💡 Recommendations
- AI-powered cost optimization suggestions
- Suitable financial product recommendations
- Industry-specific risk assessment
- Strategic action plans

### 📁 File Upload
- Support for CSV and Excel formats
- Batch processing
- Instant analysis
- Result summary

### 📄 Reports
- **PDF**: Professional, investor-ready format
- **Excel**: Data-friendly spreadsheet format
- **JSON**: API-friendly format

---

## Key Metrics Explained

### Current Ratio
- Shows short-term liquidity
- Formula: Current Assets / Current Liabilities
- Healthy Range: 1.5 - 3.0

### Debt-to-Equity Ratio
- Shows financial leverage
- Formula: Total Liabilities / Equity
- Healthy Range: 0.5 - 1.5

### Profit Margin
- Shows profitability
- Formula: (Net Profit / Revenue) × 100
- Healthy Range: 10% - 20%

### Return on Equity (ROE)
- Shows shareholder returns
- Formula: (Net Profit / Equity) × 100
- Healthy Range: 15% - 25%

---

## Financial Health Scoring

| Score | Category | Assessment |
|-------|----------|-----------|
| 80-100 | Low Risk | Excellent health |
| 60-79 | Medium Risk | Good health, areas for improvement |
| 40-59 | High Risk | Concerns, action needed |
| 0-39 | Critical Risk | Severe distress |

---

## Languages Supported

- 🇬🇧 English (en)
- 🇮🇳 हिन्दी (hi)

Switch languages in the top navigation bar.

---

## File Requirements for Upload

### Minimum Columns Required:
```
business_id, industry_type, annual_revenue, total_expenses,
current_assets, current_liabilities, total_assets, 
total_liabilities, gst_compliance_status
```

### File Size Limits:
- Maximum: 16 MB
- Supported: CSV, XLSX, XLS

---

## Next Steps

1. **Explore Sample Data**: Analyze the pre-loaded SME businesses
2. **Upload Your Data**: Test with your own financial data
3. **Generate Reports**: Download and share comprehensive reports
4. **Integrate API**: Use the API endpoints in your applications
5. **Customize**: Modify settings in CONFIGURATION.md

---

## Getting Help

- 📖 Read [README.md](README.md) for detailed documentation
- 🔌 Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- ⚙️ See [CONFIGURATION.md](CONFIGURATION.md) for customization

---

## Performance Tips

### For Faster Load Times:
1. Use the Dashboard to browse businesses
2. Filter by industry or risk level
3. Batch analyze multiple businesses together
4. Cache reports for repeated viewing

### For Better Analysis:
1. Ensure accurate data input
2. Include all required columns
3. Use consistent formatting
4. Update data regularly

---

## Deployment Checklist

Before going production:
- [ ] Update SECRET_KEY in configuration
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up database (PostgreSQL recommended)
- [ ] Configure environment variables
- [ ] Set up logging and monitoring
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Set up backups
- [ ] Test all endpoints
- [ ] Load test the system

---

## Support Resources

| Resource | Link |
|----------|------|
| Main README | [README.md](README.md) |
| API Docs | [API_DOCUMENTATION.md](API_DOCUMENTATION.md) |
| Configuration | [CONFIGURATION.md](CONFIGURATION.md) |
| Quick Start | This file |

---

## Keyboard Shortcuts

- `Tab` - Navigate between form fields
- `Enter` - Submit forms
- `Esc` - Close dialogs

---

## Tips & Tricks

1. **Export Data**: Use Excel reports for further analysis in spreadsheet tools
2. **Share Reports**: PDF reports are perfect for sharing with stakeholders
3. **API Integration**: Use JSON reports to integrate with other systems
4. **Batch Analysis**: Upload multiple businesses to analyze in one go
5. **Comparison**: Compare multiple businesses side-by-side in the dashboard

---

**Happy Analyzing! 🚀**

For detailed information, please refer to the complete [README.md](README.md)
