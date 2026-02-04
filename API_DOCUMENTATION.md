# API Documentation - Financial Health Assessment Tool

## Base URL
```
http://127.0.0.1:5000/api
```

## Authentication
Currently, the API is open. For production, implement JWT authentication.

## Content Types
- Request: `application/json` or `multipart/form-data`
- Response: `application/json`

---

## Endpoints

### 1. Health Check
**Endpoint**: `GET /api/health`

**Description**: Check API health status

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-02-01T12:00:00",
  "version": "1.0.0"
}
```

---

### 2. Get Business Analysis
**Endpoint**: `GET /api/analysis/<business_id>`

**Parameters**:
- `business_id` (path): Unique business identifier
- `language` (query, optional): `en` or `hi` (default: `en`)

**Example**:
```
GET /api/analysis/SME_1?language=en
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "business_id": "SME_1",
    "analysis": {
      "business_id": "SME_1",
      "industry_type": "E-commerce",
      "financial_metrics": {
        "annual_revenue": 34999221,
        "total_expenses": 26355176,
        "net_profit": 8644045,
        "total_assets": 50000000,
        "total_liabilities": 25000000,
        "equity": 25000000,
        "current_assets": 15000000,
        "current_liabilities": 5700000
      },
      "liquidity_ratios": {
        "current_ratio": 2.63,
        "quick_ratio": 2.54
      },
      "profitability_ratios": {
        "profit_margin": 24.69,
        "roa": 17.29,
        "roe": 34.58,
        "net_profit": 8644045
      },
      "leverage_ratios": {
        "debt_equity_ratio": 1.0,
        "debt_ratio": 0.5,
        "equity_multiplier": 2.0,
        "dscr": 2.61
      },
      "efficiency_ratios": {
        "asset_turnover": 0.7,
        "receivables_turnover": 3.5,
        "inventory_turnover": 2.2,
        "days_inventory": 166,
        "days_receivables": 104
      },
      "working_capital": {
        "working_capital": 9300000,
        "working_capital_ratio": 0.266,
        "cash_conversion_cycle": 65,
        "operating_cash_flow": 5249883
      },
      "creditworthiness": {
        "score": 95,
        "assessment": ["Strong current ratio...", "Healthy debt-equity ratio..."]
      },
      "financial_health": {
        "health_score": 95,
        "risk_category": "Low Risk"
      },
      "gst_compliance": "Compliant",
      "industry_benchmarks": {...}
    },
    "recommendations": {...}
  }
}
```

---

### 3. List All Businesses
**Endpoint**: `GET /api/businesses`

**Parameters**: None

**Response**:
```json
{
  "status": "success",
  "count": 10,
  "data": [
    {
      "business_id": "SME_1",
      "industry_type": "E-commerce",
      "annual_revenue": 34999221,
      "financial_health_score": 100
    },
    ...
  ]
}
```

---

### 4. Upload and Analyze
**Endpoint**: `POST /api/upload`

**Headers**: `Content-Type: multipart/form-data`

**Parameters**:
- `file` (form-data): CSV or Excel file

**Example**:
```bash
curl -X POST http://127.0.0.1:5000/api/upload \
  -F "file=@financial_data.csv"
```

**Response**:
```json
{
  "status": "success",
  "message": "Processed 5 records",
  "file_path": "20240201_120000_financial_data.csv",
  "data": [
    {
      "business_id": "UPLOADED_1",
      "analysis": {...},
      "recommendations": {...}
    }
  ]
}
```

---

### 5. Batch Analysis
**Endpoint**: `POST /api/batch-analysis`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "business_ids": ["SME_1", "SME_2", "SME_3"],
  "language": "en"
}
```

**Response**:
```json
{
  "status": "success",
  "count": 3,
  "data": [
    {
      "business_id": "SME_1",
      "status": "success",
      "analysis": {...},
      "recommendations": {...}
    },
    {
      "business_id": "SME_2",
      "status": "success",
      "analysis": {...}
    },
    {
      "business_id": "SME_3",
      "status": "not_found"
    }
  ]
}
```

---

### 6. Get Dashboard Metrics
**Endpoint**: `GET /api/dashboard`

**Parameters**: None

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_businesses": 10,
    "total_revenue": 350000000,
    "average_health_score": 72.5,
    "risk_distribution": {
      "low_risk": 7,
      "medium_risk": 2,
      "high_risk": 1
    },
    "businesses": [...]
  }
}
```

---

### 7. Generate PDF Report
**Endpoint**: `GET /api/report/pdf/<business_id>`

**Parameters**:
- `business_id` (path): Unique business identifier

**Response**: Binary PDF file

**Example**:
```bash
curl -X GET http://127.0.0.1:5000/api/report/pdf/SME_1 \
  -o SME_1_report.pdf
```

---

### 8. Generate Excel Report
**Endpoint**: `GET /api/report/excel/<business_id>`

**Parameters**:
- `business_id` (path): Unique business identifier

**Response**: Binary Excel file

**Example**:
```bash
curl -X GET http://127.0.0.1:5000/api/report/excel/SME_1 \
  -o SME_1_report.xlsx
```

---

### 9. Get JSON Report
**Endpoint**: `GET /api/report/json/<business_id>`

**Parameters**:
- `business_id` (path): Unique business identifier

**Response**:
```json
{
  "status": "success",
  "data": {
    "metadata": {
      "business_id": "SME_1",
      "industry": "E-commerce",
      "report_date": "2024-02-01 12:00:00",
      "report_version": "1.0"
    },
    "financial_analysis": {...},
    "recommendations": {...},
    "generated_at": "2024-02-01T12:00:00"
  }
}
```

---

### 10. Get Supported Languages
**Endpoint**: `GET /api/languages`

**Parameters**: None

**Response**:
```json
{
  "status": "success",
  "languages": ["en", "hi"]
}
```

---

### 11. Translate Key
**Endpoint**: `GET /api/translate/<key>`

**Parameters**:
- `key` (path): Translation key
- `language` (query): Language code (en or hi)

**Example**:
```
GET /api/translate/annual_revenue?language=hi
```

**Response**:
```json
{
  "status": "success",
  "key": "annual_revenue",
  "language": "hi",
  "translation": "वार्षिक राजस्व"
}
```

---

### 12. API Documentation
**Endpoint**: `GET /api/docs`

**Parameters**: None

**Response**:
```json
{
  "title": "Financial Health Assessment Tool API",
  "version": "1.0.0",
  "endpoints": {
    "GET /api/health": "Health check",
    "GET /api/analysis/<business_id>": "Get comprehensive financial analysis",
    ...
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Bad request",
  "details": "Error details"
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Business with ID SME_999 not found"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "Internal server error",
  "details": "Error details"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, add:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## Pagination

For list endpoints, add pagination in future versions:

```
GET /api/businesses?page=1&limit=10&sort=business_id&order=asc
```

---

## Data Validation

Required fields for CSV/Excel uploads:
- `business_id` - string
- `industry_type` - string
- `annual_revenue` - number (positive)
- `total_expenses` - number (positive)
- `current_assets` - number
- `current_liabilities` - number (positive)
- `total_assets` - number
- `total_liabilities` - number
- `gst_compliance_status` - string (Compliant/Non-Compliant/Delayed)

---

## Usage Examples

### JavaScript/Fetch
```javascript
// Get analysis
const response = await fetch('http://127.0.0.1:5000/api/analysis/SME_1');
const data = await response.json();
console.log(data.data.analysis);

// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
const uploadResponse = await fetch('http://127.0.0.1:5000/api/upload', {
  method: 'POST',
  body: formData
});
```

### Python/Requests
```python
import requests

# Get analysis
response = requests.get('http://127.0.0.1:5000/api/analysis/SME_1')
analysis = response.json()

# Upload file
with open('data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://127.0.0.1:5000/api/upload', files=files)
```

### cURL
```bash
# Get analysis
curl -X GET "http://127.0.0.1:5000/api/analysis/SME_1"

# Upload file
curl -X POST "http://127.0.0.1:5000/api/upload" \
  -F "file=@data.csv"

# Download PDF
curl -X GET "http://127.0.0.1:5000/api/report/pdf/SME_1" \
  -o report.pdf
```

---

## Version History

### v1.0.0 (Current)
- Core financial analysis
- 15+ API endpoints
- PDF/Excel/JSON reports
- Multilingual support
- File upload capability

### Future (v1.1.0)
- Rate limiting
- Authentication/JWT
- Database integration
- Advanced caching
- Webhook support

---

For more information, refer to [README.md](README.md) and [CONFIGURATION.md](CONFIGURATION.md)
