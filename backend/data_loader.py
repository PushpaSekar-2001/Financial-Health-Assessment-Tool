
import pandas as pd
import os
from pathlib import Path
import numpy as np
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "SME_Financial_Health_Dataset.csv")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Supported file formats
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_financial_data(df):
    """Validate that required financial columns are present"""
    required_columns = {
        'annual_revenue', 'total_expenses', 'current_assets', 
        'current_liabilities', 'total_assets', 'total_liabilities'
    }
    
    missing_cols = required_columns - set(df.columns)
    if missing_cols:
        return False, f"Missing required columns: {missing_cols}"
    
    # Check for positive values in revenue
    if (df['annual_revenue'] <= 0).any():
        return False, "Annual revenue must be positive"
    
    return True, "Validation passed"

def load_csv_data(file_path):
    """Load financial data from CSV"""
    try:
        df = pd.read_csv(file_path)
        df['business_id'] = df.get('business_id', [f"CSV_{i}" for i in range(len(df))])
        df['upload_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['source'] = 'CSV Upload'
        return df
    except Exception as e:
        return None, f"Error loading CSV: {str(e)}"

def load_xlsx_data(file_path):
    """Load financial data from Excel (XLSX/XLS)"""
    try:
        df = pd.read_excel(file_path)
        df['business_id'] = df.get('business_id', [f"XLSX_{i}" for i in range(len(df))])
        df['upload_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df['source'] = 'Excel Upload'
        return df
    except Exception as e:
        return None, f"Error loading Excel: {str(e)}"

def load_business_data(business_id):
    """Load business data from default dataset"""
    try:
        # Read with python engine and explicit separator to be resilient to odd line breaks
        df = pd.read_csv(CSV_PATH, sep=',', engine='python', skipinitialspace=True)
        df["business_id"] = df["business_id"].astype(str).str.strip()
        df = df[df["business_id"] == business_id.strip()]
        if df.empty:
            return None

        # Ensure required numeric columns exist. If missing, create reasonable defaults
        ar = float(df['annual_revenue'].fillna(0).iloc[0]) if 'annual_revenue' in df.columns else 0.0

        # current_assets
        if 'current_assets' not in df.columns:
            if 'current_ratio' in df.columns and 'current_liabilities' in df.columns and df['current_liabilities'].iloc[0] not in (0, None):
                df['current_assets'] = df['current_ratio'] * df['current_liabilities']
            elif 'current_ratio' in df.columns:
                df['current_assets'] = ar * 0.2 * float(df['current_ratio'].fillna(1).iloc[0])
            else:
                df['current_assets'] = ar * 0.2

        # current_liabilities
        if 'current_liabilities' not in df.columns:
            if 'current_ratio' in df.columns and df['current_ratio'].iloc[0] not in (0, None):
                df['current_liabilities'] = df['current_assets'] / df['current_ratio']
            else:
                df['current_liabilities'] = max(1.0, ar * 0.1)

        # total_assets
        if 'total_assets' not in df.columns:
            df['total_assets'] = ar * 1.2 if ar > 0 else 0.0

        # total_liabilities
        if 'total_liabilities' not in df.columns:
            # try to infer from debt_equity_ratio if available
            if 'debt_equity_ratio' in df.columns and df['debt_equity_ratio'].iloc[0] not in (0, None):
                de = float(df['debt_equity_ratio'].fillna(0).iloc[0])
                # use scalar values to avoid Series boolean ambiguity
                total_assets_val = float(df['total_assets'].iloc[0]) if 'total_assets' in df.columns else float(ar * 1.2)
                if 'total_liabilities' in df.columns:
                    total_liabilities_val = float(df['total_liabilities'].iloc[0])
                    equity = total_assets_val - total_liabilities_val
                else:
                    equity = total_assets_val * 0.7
                df['total_liabilities'] = de * (equity if equity > 0 else total_assets_val * 0.5)
            else:
                df['total_liabilities'] = df['total_assets'] * 0.3

        # inventory (optional)
        if 'inventory' not in df.columns:
            df['inventory'] = ar * 0.05

        # Ensure numeric types
        numeric_cols = ['annual_revenue', 'total_expenses', 'current_assets', 'current_liabilities', 'total_assets', 'total_liabilities', 'inventory']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        return df
    except Exception as e:
        print(f"Error loading business data: {str(e)}")
        return None

def load_data_from_file(file_path):
    """Load financial data from uploaded file (CSV, XLSX, PDF)"""
    if not os.path.exists(file_path):
        return None, "File not found"
    
    file_ext = Path(file_path).suffix.lower().strip('.')
    
    if file_ext == 'csv':
        return load_csv_data(file_path)
    elif file_ext in ['xlsx', 'xls']:
        return load_xlsx_data(file_path)
    elif file_ext == 'pdf':
        return None, "PDF extraction requires manual review - please export as CSV/XLSX"
    else:
        return None, f"Unsupported file format: {file_ext}"

def normalize_financial_data(df):
    """Normalize and clean financial data"""
    # Fill missing values
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Ensure positive values for key metrics
    if 'annual_revenue' in df.columns:
        df['annual_revenue'] = df['annual_revenue'].abs()
    if 'total_expenses' in df.columns:
        df['total_expenses'] = df['total_expenses'].abs()
    
    return df

def get_all_businesses():
    """Get list of all businesses in dataset"""
    try:
        df = pd.read_csv(CSV_PATH)
        return df[['business_id', 'industry_type', 'annual_revenue', 'financial_health_score']].to_dict('records')
    except Exception as e:
        print(f"Error getting businesses: {str(e)}")
        return []
