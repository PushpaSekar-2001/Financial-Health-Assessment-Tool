
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

# Industry-specific benchmarks
INDUSTRY_BENCHMARKS = {
    'Manufacturing': {
        'current_ratio': 1.8, 'quick_ratio': 1.2, 'debt_equity': 1.5,
        'profit_margin': 0.12, 'asset_turnover': 1.5, 'roe': 0.18
    },
    'Retail': {
        'current_ratio': 1.5, 'quick_ratio': 0.8, 'debt_equity': 1.0,
        'profit_margin': 0.08, 'asset_turnover': 2.0, 'roe': 0.15
    },
    'Services': {
        'current_ratio': 1.8, 'quick_ratio': 1.5, 'debt_equity': 0.8,
        'profit_margin': 0.15, 'asset_turnover': 2.5, 'roe': 0.20
    },
    'Logistics': {
        'current_ratio': 1.3, 'quick_ratio': 0.9, 'debt_equity': 1.2,
        'profit_margin': 0.10, 'asset_turnover': 1.8, 'roe': 0.16
    },
    'E-commerce': {
        'current_ratio': 1.6, 'quick_ratio': 1.2, 'debt_equity': 0.9,
        'profit_margin': 0.10, 'asset_turnover': 3.0, 'roe': 0.22
    },
    'Agriculture': {
        'current_ratio': 1.4, 'quick_ratio': 0.7, 'debt_equity': 1.3,
        'profit_margin': 0.12, 'asset_turnover': 1.2, 'roe': 0.14
    }
}

def calculate_liquidity_ratios(df):
    """Calculate liquidity ratios"""
    # Use provided ratio columns when available, otherwise compute from assets/liabilities if present
    try:
        if 'current_ratio' in df.columns:
            current_ratio = float(df['current_ratio'].iloc[0])
        elif 'current_assets' in df.columns and 'current_liabilities' in df.columns and float(df['current_liabilities'].iloc[0]) != 0:
            current_ratio = float(df['current_assets'].iloc[0]) / float(df['current_liabilities'].iloc[0])
        else:
            current_ratio = 0.0

        if 'quick_ratio' in df.columns:
            quick_ratio = float(df['quick_ratio'].iloc[0])
        else:
            if 'inventory' in df.columns and 'current_assets' in df.columns and 'current_liabilities' in df.columns and float(df['current_liabilities'].iloc[0]) != 0:
                quick_ratio = (float(df['current_assets'].iloc[0]) - float(df['inventory'].iloc[0])) / float(df['current_liabilities'].iloc[0])
            else:
                quick_ratio = round(current_ratio * 0.9, 2) if current_ratio else 0.0

        return {
            'current_ratio': round(float(current_ratio), 2),
            'quick_ratio': round(float(quick_ratio), 2)
        }
    except Exception:
        return {'current_ratio': 0.0, 'quick_ratio': 0.0}

def calculate_profitability_ratios(df):
    """Calculate profitability ratios"""
    profit = df['annual_revenue'] - df['total_expenses']
    rev = float(df['annual_revenue'].iloc[0]) if 'annual_revenue' in df.columns else 0.0
    profit_margin = (profit / rev * 100) if rev > 0 else 0

    # ROA: prefer total_assets if available, otherwise use 'roce' if present
    try:
        if 'total_assets' in df.columns and float(df['total_assets'].iloc[0]) > 0:
            roa = (profit / float(df['total_assets'].iloc[0]) * 100)
        elif 'roce' in df.columns:
            roa = float(df['roce'].iloc[0])
        else:
            roa = 0
    except Exception:
        roa = 0

    # ROE: compute if total_assets and total_liabilities present
    try:
        if 'total_assets' in df.columns and 'total_liabilities' in df.columns:
            equity = float(df['total_assets'].iloc[0]) - float(df['total_liabilities'].iloc[0])
            roe = (profit / equity * 100) if equity > 0 else 0
        else:
            roe = 0
    except Exception:
        roe = 0

    return {
        'profit_margin': round(float(profit_margin.iloc[0]) if hasattr(profit_margin, 'iloc') else float(profit_margin), 2),
        'roa': round(float(roa), 2),
        'roe': round(float(roe), 2),
        'net_profit': int(profit.iloc[0])
    }

def calculate_leverage_ratios(df):
    """Calculate leverage and solvency ratios"""
    try:
        # prefer a provided debt_equity_ratio
        if 'debt_equity_ratio' in df.columns:
            de = float(df['debt_equity_ratio'].iloc[0])
        elif 'debt_equity_ratio' not in df.columns and 'total_assets' in df.columns and 'total_liabilities' in df.columns:
            equity = float(df['total_assets'].iloc[0]) - float(df['total_liabilities'].iloc[0])
            de = (float(df['total_liabilities'].iloc[0]) / equity) if equity > 0 else 0
        else:
            de = 0

        debt_ratio = float(df['total_liabilities'].iloc[0]) / float(df['total_assets'].iloc[0]) if 'total_liabilities' in df.columns and 'total_assets' in df.columns and float(df['total_assets'].iloc[0]) != 0 else 0
        equity_multiplier = float(df['total_assets'].iloc[0]) / (float(df['total_assets'].iloc[0]) - float(df['total_liabilities'].iloc[0])) if 'total_assets' in df.columns and 'total_liabilities' in df.columns and (float(df['total_assets'].iloc[0]) - float(df['total_liabilities'].iloc[0])) != 0 else 0

        dscr = float(df['dscr'].iloc[0]) if 'dscr' in df.columns else 0

        return {
            'debt_equity_ratio': round(de, 2),
            'debt_ratio': round(debt_ratio, 2),
            'equity_multiplier': round(equity_multiplier, 2),
            'dscr': round(dscr, 2)
        }
    except Exception:
        return {'debt_equity_ratio': 0.0, 'debt_ratio': 0.0, 'equity_multiplier': 0.0, 'dscr': 0.0}

def calculate_efficiency_ratios(df):
    """Calculate asset and turnover efficiency ratios"""
    asset_turnover = df['annual_revenue'] / (df['total_assets'] + 1)
    receivables_turnover = df['annual_revenue'] / (df.get('accounts_receivable', pd.Series([df['annual_revenue'].iloc[0] * 0.2])).iloc[0] + 1)
    inventory_turnover = df['total_expenses'] / (df.get('inventory', pd.Series([df['total_expenses'].iloc[0] * 0.15])).iloc[0] + 1)
    
    return {
        'asset_turnover': round(float(asset_turnover.iloc[0]), 2),
        'receivables_turnover': round(float(receivables_turnover.iloc[0]), 2),
        'inventory_turnover': round(float(inventory_turnover.iloc[0]), 2),
        'days_inventory': round(365 / float(inventory_turnover.iloc[0]), 0) if float(inventory_turnover.iloc[0]) > 0 else 0,
        'days_receivables': round(365 / float(receivables_turnover.iloc[0]), 0) if float(receivables_turnover.iloc[0]) > 0 else 0
    }

def calculate_working_capital_metrics(df):
    """Calculate working capital and cash flow metrics"""
    working_capital = df['current_assets'] - df['current_liabilities']
    working_capital_ratio = working_capital / df['annual_revenue']
    cash_conversion_cycle = (df.get('days_inventory', pd.Series([45])).iloc[0] + 
                            df.get('days_receivables', pd.Series([30])).iloc[0] - 
                            df.get('days_payables', pd.Series([25])).iloc[0])
    
    operating_cash_flow = df['annual_revenue'] * 0.15  # Estimate 15% of revenue
    
    return {
        'working_capital': int(working_capital.iloc[0]),
        'working_capital_ratio': round(float(working_capital_ratio.iloc[0]), 3),
        'cash_conversion_cycle': int(cash_conversion_cycle),
        'operating_cash_flow': int(operating_cash_flow.iloc[0])
    }

def assess_creditworthiness(df, ratios):
    """Assess creditworthiness based on financial metrics"""
    score = 0
    details = []
    
    # Current ratio assessment (weight: 20)
    if ratios['liquidity']['current_ratio'] >= 2.0:
        score += 20
        details.append("Strong current ratio - Excellent short-term liquidity")
    elif ratios['liquidity']['current_ratio'] >= 1.5:
        score += 15
        details.append("Good current ratio - Adequate short-term liquidity")
    elif ratios['liquidity']['current_ratio'] >= 1.0:
        score += 10
        details.append("Moderate current ratio - Acceptable liquidity")
    else:
        score += 5
        details.append("Low current ratio - Potential liquidity concerns")
    
    # Debt-to-equity assessment (weight: 20)
    if ratios['leverage']['debt_equity_ratio'] <= 1.0:
        score += 20
        details.append("Healthy debt-equity ratio - Conservative leverage")
    elif ratios['leverage']['debt_equity_ratio'] <= 1.5:
        score += 15
        details.append("Moderate debt-equity ratio - Acceptable leverage")
    elif ratios['leverage']['debt_equity_ratio'] <= 2.0:
        score += 10
        details.append("High debt-equity ratio - Watch leverage levels")
    else:
        score += 5
        details.append("Very high debt-equity ratio - Risk of over-leverage")
    
    # Profitability assessment (weight: 20)
    if ratios['profitability']['profit_margin'] >= 15:
        score += 20
        details.append("Excellent profit margin - Strong profitability")
    elif ratios['profitability']['profit_margin'] >= 10:
        score += 15
        details.append("Good profit margin - Healthy profitability")
    elif ratios['profitability']['profit_margin'] >= 5:
        score += 10
        details.append("Moderate profit margin - Acceptable profitability")
    else:
        score += 5
        details.append("Low profit margin - Profitability concerns")
    
    # DSCR assessment (weight: 20)
    dscr = ratios['leverage'].get('dscr', 1.0)
    if dscr >= 1.5:
        score += 20
        details.append("Strong DSCR - Excellent debt servicing ability")
    elif dscr >= 1.2:
        score += 15
        details.append("Good DSCR - Healthy debt servicing")
    elif dscr >= 1.0:
        score += 10
        details.append("Adequate DSCR - Acceptable debt servicing")
    else:
        score += 5
        details.append("Low DSCR - Debt servicing concerns")
    
    # ROE assessment (weight: 20)
    if ratios['profitability']['roe'] >= 20:
        score += 20
        details.append("Excellent ROE - Strong shareholder returns")
    elif ratios['profitability']['roe'] >= 15:
        score += 15
        details.append("Good ROE - Healthy returns")
    elif ratios['profitability']['roe'] >= 5:
        score += 10
        details.append("Moderate ROE - Acceptable returns")
    else:
        score += 5
        details.append("Low ROE - Limited returns")
    
    return score, details

def assess_financial_health(df, creditworthiness_score):
    """Assess overall financial health and risk"""
    risk_category = "Low Risk"
    health_score = creditworthiness_score
    
    if creditworthiness_score >= 80:
        risk_category = "Low Risk"
    elif creditworthiness_score >= 60:
        risk_category = "Medium Risk"
    elif creditworthiness_score >= 40:
        risk_category = "High Risk"
    else:
        risk_category = "Critical Risk"
    
    return {
        'health_score': health_score,
        'risk_category': risk_category
    }

def perform_analysis(df):
    """Perform comprehensive financial analysis"""
    if df is None or df.empty:
        return None
    
    # Calculate all ratios
    liquidity = calculate_liquidity_ratios(df)
    profitability = calculate_profitability_ratios(df)
    leverage = calculate_leverage_ratios(df)
    efficiency = calculate_efficiency_ratios(df)
    working_capital = calculate_working_capital_metrics(df)
    
    # Combine all ratios
    all_ratios = {
        'liquidity': liquidity,
        'profitability': profitability,
        'leverage': leverage,
        'efficiency': efficiency,
        'working_capital': working_capital
    }
    
    # Calculate creditworthiness score
    cred_score, cred_details = assess_creditworthiness(df, all_ratios)
    
    # Assess financial health
    health = assess_financial_health(df, cred_score)
    
    # Determine GST compliance status
    gst_status = df['gst_compliance_status'].iloc[0] if 'gst_compliance_status' in df.columns else "Not Assessed"
    
    return {
        'business_id': str(df['business_id'].iloc[0]),
        'industry_type': str(df['industry_type'].iloc[0]) if 'industry_type' in df.columns else 'Unknown',
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        
        # Financial Metrics
        'financial_metrics': {
            'annual_revenue': int(df['annual_revenue'].iloc[0]),
            'total_expenses': int(df['total_expenses'].iloc[0]),
            'net_profit': profitability['net_profit'],
            'total_assets': int(df['total_assets'].iloc[0]),
            'total_liabilities': int(df['total_liabilities'].iloc[0]),
            'equity': int(df['total_assets'].iloc[0] - df['total_liabilities'].iloc[0]),
            'current_assets': int(df['current_assets'].iloc[0]),
            'current_liabilities': int(df['current_liabilities'].iloc[0])
        },
        
        # Liquidity Ratios
        'liquidity_ratios': liquidity,
        
        # Profitability Ratios
        'profitability_ratios': profitability,
        
        # Leverage Ratios
        'leverage_ratios': leverage,
        
        # Efficiency Ratios
        'efficiency_ratios': efficiency,
        
        # Working Capital
        'working_capital': working_capital,
        
        # Creditworthiness Assessment
        'creditworthiness': {
            'score': cred_score,
            'assessment': cred_details
        },
        
        # Financial Health
        'financial_health': health,
        'gst_compliance': gst_status,
        
        # Industry Comparison
        'industry_benchmarks': INDUSTRY_BENCHMARKS.get(df['industry_type'].iloc[0] if 'industry_type' in df.columns else 'Services', INDUSTRY_BENCHMARKS['Services'])
    }
