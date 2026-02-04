# Configuration Guide for Financial Health Assessment Tool

## Environment Variables

Create a `.env` file in the backend directory for production configurations:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=False
SECRET_KEY=your_secret_key_here

# Database (for future PostgreSQL integration)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=financial_health
DB_USER=postgres
DB_PASSWORD=your_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
MAX_UPLOAD_SIZE=16777216  # 16MB in bytes

# File Upload
UPLOAD_FOLDER=./uploads
ALLOWED_EXTENSIONS=csv,xlsx,xls,pdf

# Security
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Email Notifications (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_password
```

## Flask Configuration (app.py)

The application uses the following default configurations:

```python
# File Upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# CORS
CORS(app)

# JSON Settings
app.config['JSON_SORT_KEYS'] = False
```

## React Configuration (.env)

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_BASE_URL=http://127.0.0.1:5000/api
REACT_APP_TIMEOUT=30000  # milliseconds
```

## Industry Benchmark Configuration

Modify the INDUSTRY_BENCHMARKS dictionary in `analysis.py` to add or update industry standards:

```python
INDUSTRY_BENCHMARKS = {
    'YourIndustry': {
        'current_ratio': 1.8,
        'quick_ratio': 1.2,
        'debt_equity': 1.5,
        'profit_margin': 0.12,
        'asset_turnover': 1.5,
        'roe': 0.18
    }
}
```

## Financial Ratios Configuration

Customize the financial health scoring criteria in `recommendation.py`:

```python
def assess_creditworthiness(df, ratios):
    score = 0
    
    # Adjust weights as needed
    if ratios['liquidity']['current_ratio'] >= 2.0:
        score += 20  # Current ratio weight
    # ... rest of assessment
```

## Report Template Customization

Modify the PDF report template in `report_generator.py`:

```python
# Customize fonts
title_style = ParagraphStyle(
    'CustomTitle',
    fontSize=24,  # Adjust size
    textColor=colors.HexColor('#003366'),  # Adjust color
    alignment=TA_CENTER
)
```

## Multilingual Support

Add new languages in `translations.py`:

```python
TRANSLATIONS = {
    'es': {  # Spanish
        'app_name': 'Herramienta de Evaluación de Salud Financiera',
        'annual_revenue': 'Ingresos Anuales',
        # ... add all keys
    }
}
```

## Database Configuration (Future)

When integrating PostgreSQL:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db_name'
db = SQLAlchemy(app)
```

## Logging Configuration

Customize logging in `app.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

## API Response Format

Standard API response format:

```json
{
    "status": "success|error",
    "message": "Description",
    "data": {
        // Response data
    },
    "timestamp": "2024-01-01T00:00:00Z"
}
```

## Financial Health Score Ranges

Customize score ranges in `analysis.py`:

```python
if creditworthiness_score >= 80:
    risk_category = "Low Risk"
elif creditworthiness_score >= 60:
    risk_category = "Medium Risk"
elif creditworthiness_score >= 40:
    risk_category = "High Risk"
else:
    risk_category = "Critical Risk"
```

## Working Capital Calculation

Modify working capital optimization parameters:

```python
# Days inventory outstanding benchmark (industry-specific)
DIE_BENCHMARK = 45

# Days sales outstanding benchmark
DSO_BENCHMARK = 30

# Days payable outstanding benchmark
DPO_BENCHMARK = 25

# Optimal working capital ratio
OPTIMAL_WC_RATIO = 0.3
```

## Debt Service Coverage Ratio (DSCR)

Configure DSCR thresholds:

```python
# DSCR Assessment
DSCR_EXCELLENT = 1.5   # >= 1.5
DSCR_HEALTHY = 1.25    # >= 1.25
DSCR_ACCEPTABLE = 1.0  # >= 1.0
DSCR_CONCERN = 0.8     # < 1.0
```

## GST Compliance Levels

Customize GST compliance assessment:

```python
GST_STATUS_LEVELS = {
    'Compliant': {'score': 100, 'risk': 'Low'},
    'Delayed': {'score': 70, 'risk': 'Medium'},
    'Non-Compliant': {'score': 30, 'risk': 'High'}
}
```

## Production Deployment Settings

For production, modify `app.py`:

```python
if __name__ == "__main__":
    # Production settings
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,  # Set to False
        threaded=True,
        ssl_context='adhoc'  # For HTTPS
    )
```

## Performance Optimization

### Backend
- Enable caching for business lookups
- Batch analysis for multiple businesses
- Database indexing on business_id

### Frontend
- Lazy load components
- Code splitting for faster load times
- Compress images and assets

## Security Hardening

### HTTPS
```python
from flask_talisman import Talisman
Talisman(app)
```

### Rate Limiting
```python
from flask_limiter import Limiter
limiter = Limiter(app)

@app.route('/api/analysis/<business_id>')
@limiter.limit("100 per hour")
def get_business_analysis(business_id):
    pass
```

### Input Validation
Use Pydantic models for request validation:

```python
from pydantic import BaseModel, validator

class BusinessData(BaseModel):
    business_id: str
    annual_revenue: float
    total_expenses: float
    
    @validator('annual_revenue', 'total_expenses')
    def positive_values(cls, v):
        if v < 0:
            raise ValueError('Values must be positive')
        return v
```

## Monitoring & Logging

Configure structured logging:

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module
        }
        return json.dumps(log_data)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

## Backup & Recovery

Set up automated backups:

```bash
# Backup database daily
0 2 * * * pg_dump -U postgres financial_health > /backup/db_$(date +\%Y\%m\%d).sql

# Backup uploaded files
0 3 * * * tar -czf /backup/uploads_$(date +\%Y\%m\%d).tar.gz uploads/
```

## Testing Configuration

Run tests with coverage:

```bash
# Backend tests
pytest tests/ --cov=backend

# Frontend tests
npm test -- --coverage
```

## CI/CD Configuration

Example GitHub Actions workflow:

```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

---

For more information, refer to the main [README.md](README.md)
