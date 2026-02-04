
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Financial product recommendations
FINANCIAL_PRODUCTS = {
    'Working Capital Loan': {
        'min_score': 50,
        'loan_amount_factor': 0.3,  # 30% of annual revenue
        'interest_rate_range': '9-12%',
        'tenure': '1-3 years',
        'description': 'For managing daily operational expenses and inventory'
    },
    'Term Loan': {
        'min_score': 60,
        'loan_amount_factor': 0.5,  # 50% of annual revenue
        'interest_rate_range': '8-11%',
        'tenure': '3-7 years',
        'description': 'For capital expenditure and expansion'
    },
    'Equipment Financing': {
        'min_score': 55,
        'loan_amount_factor': 0.4,
        'interest_rate_range': '8.5-11%',
        'tenure': '3-5 years',
        'description': 'For purchasing machinery and equipment'
    },
    'Business Credit Card': {
        'min_score': 45,
        'loan_amount_factor': 0.05,  # 5% of annual revenue
        'interest_rate_range': '18-24%',
        'tenure': 'Revolving',
        'description': 'For short-term operational needs'
    },
    'Invoice Discounting': {
        'min_score': 50,
        'loan_amount_factor': 0.8,  # 80% of receivables
        'interest_rate_range': '9-13%',
        'tenure': '30-180 days',
        'description': 'Against pending customer invoices'
    },
    'Trade Credit': {
        'min_score': 55,
        'loan_amount_factor': 0.3,
        'interest_rate_range': '10-14%',
        'tenure': 'Custom',
        'description': 'For purchasing raw materials and goods'
    }
}

def analyze_cash_flow_health(df):
    """Analyze cash flow health and identify issues"""
    revenue = df['annual_revenue'].iloc[0]
    expenses = df['total_expenses'].iloc[0]
    
    issues = []
    opportunities = []
    
    net_margin = (revenue - expenses) / revenue if revenue > 0 else 0
    
    if net_margin < 0:
        issues.append({
            'severity': 'Critical',
            'issue': 'Negative Cash Flow',
            'detail': f'Business is operating at a loss ({net_margin*100:.1f}%)',
            'action': 'Urgent: Reduce operational expenses or increase revenue'
        })
    elif net_margin < 0.05:
        issues.append({
            'severity': 'High',
            'issue': 'Low Cash Flow Margin',
            'detail': f'Minimal profit margins ({net_margin*100:.1f}%)',
            'action': 'Focus on improving operational efficiency'
        })
    else:
        opportunities.append('Strong cash flow position maintained')
    
    return {'issues': issues, 'opportunities': opportunities}

def analyze_debt_obligations(df):
    """Analyze debt obligations and repayment capacity"""
    recommendations = []
    
    if 'dscr' in df.columns:
        dscr = df['dscr'].iloc[0]
        if dscr < 1.0:
            recommendations.append({
                'priority': 'Critical',
                'recommendation': 'Debt Repayment Concern',
                'detail': f'DSCR is {dscr:.2f} - Unable to service debt from current earnings',
                'action': 'Refinance existing debt or reduce obligations'
            })
        elif dscr < 1.25:
            recommendations.append({
                'priority': 'High',
                'recommendation': 'Limited Borrowing Capacity',
                'detail': f'DSCR is {dscr:.2f} - Limited room for additional debt',
                'action': 'Avoid new borrowing until cash flow improves'
            })
        else:
            recommendations.append({
                'priority': 'Low',
                'recommendation': 'Healthy Debt Servicing',
                'detail': f'DSCR is {dscr:.2f} - Adequate capacity for debt obligations',
                'action': 'Maintain current debt management strategy'
            })
    
    return recommendations

def recommend_cost_optimization(df, analysis):
    """Recommend cost optimization strategies"""
    recommendations = []
    
    total_revenue = df['annual_revenue'].iloc[0]
    total_expenses = df['total_expenses'].iloc[0]
    
    # Expense ratio analysis
    expense_ratio = total_expenses / total_revenue if total_revenue > 0 else 0
    
    if expense_ratio > 0.85:
        savings_target = total_expenses * 0.10
        recommendations.append({
            'category': 'Expense Management',
            'title': 'High Expense Ratio Alert',
            'detail': f'Expenses are {expense_ratio*100:.1f}% of revenue',
            'target_saving': f'Reduce expenses by ₹{int(savings_target):,} (10%)',
            'action_items': [
                'Review and negotiate supplier contracts',
                'Optimize staffing levels',
                'Consolidate service providers',
                'Reduce overhead expenses'
            ]
        })
    
    # Working capital optimization
    if 'current_assets' in df.columns and 'current_liabilities' in df.columns:
        wc_ratio = df['current_assets'].iloc[0] / (df['current_liabilities'].iloc[0] + 1)
        if wc_ratio > 2.5:
            excess_wc = df['current_assets'].iloc[0] - (df['current_liabilities'].iloc[0] * 2)
            recommendations.append({
                'category': 'Working Capital',
                'title': 'Excess Working Capital',
                'detail': f'Current assets significantly exceed operational needs',
                'opportunity': f'Potential cash release of ₹{int(excess_wc):,}',
                'action_items': [
                    'Optimize inventory levels',
                    'Accelerate receivables collection',
                    'Negotiate extended payables terms',
                    'Deploy excess cash in growth initiatives'
                ]
            })
    
    return recommendations

def recommend_financial_products(analysis):
    """Recommend suitable financial products based on health score"""
    cred_score = analysis['creditworthiness']['score']
    revenue = analysis['financial_metrics']['annual_revenue']
    
    suitable_products = []
    
    for product_name, product_details in FINANCIAL_PRODUCTS.items():
        if cred_score >= product_details['min_score']:
            loan_amount = int(revenue * product_details['loan_amount_factor'])
            suitable_products.append({
                'product': product_name,
                'eligibility': 'Eligible',
                'estimated_loan_amount': f'₹{loan_amount:,}',
                'interest_rate_range': product_details['interest_rate_range'],
                'tenure': product_details['tenure'],
                'description': product_details['description'],
                'recommended': 'High' if cred_score >= 70 else 'Medium'
            })
    
    return suitable_products

def assess_industry_risks(df):
    """Assess industry-specific risks"""
    industry = df['industry_type'].iloc[0] if 'industry_type' in df.columns else 'Unknown'
    
    industry_risks = {
        'Manufacturing': [
            'Capital intensity - high fixed assets requirement',
            'Raw material price volatility',
            'Supply chain disruptions',
            'Regulatory compliance costs (environmental, safety)'
        ],
        'Retail': [
            'Seasonal demand fluctuations',
            'Competitive pressure on margins',
            'E-commerce disruption',
            'Real estate cost inflation'
        ],
        'Services': [
            'Client concentration risk',
            'Talent retention and costs',
            'Scalability challenges',
            'Regulatory changes'
        ],
        'Logistics': [
            'Fuel cost volatility',
            'Vehicle maintenance costs',
            'Driver availability',
            'Route optimization challenges'
        ],
        'E-commerce': [
            'High customer acquisition costs',
            'Payment gateway risk',
            'Supply chain complexity',
            'Cybersecurity threats'
        ],
        'Agriculture': [
            'Weather and climate risks',
            'Crop price volatility',
            'Limited access to credit',
            'Regulatory compliance (pesticides, GMO)'
        ]
    }
    
    risks = industry_risks.get(industry, [])
    
    return {
        'industry': industry,
        'identified_risks': risks,
        'mitigation_suggested': True
    }

def assess_tax_compliance(df):
    """Assess tax compliance and suggestions"""
    recommendations = []
    gst_status = df['gst_compliance_status'].iloc[0] if 'gst_compliance_status' in df.columns else 'Unknown'
    
    if gst_status == 'Non-Compliant':
        recommendations.append({
            'compliance_area': 'GST',
            'status': 'Non-Compliant',
            'priority': 'Critical',
            'action': 'File pending GST returns and rectify compliance status',
            'benefit': 'Avoid penalties and improve creditworthiness'
        })
    elif gst_status == 'Delayed':
        recommendations.append({
            'compliance_area': 'GST',
            'status': 'Delayed',
            'priority': 'High',
            'action': 'File delayed GST returns immediately',
            'benefit': 'Minimize penalties and interest charges'
        })
    else:
        recommendations.append({
            'compliance_area': 'GST',
            'status': 'Compliant',
            'priority': 'Low',
            'action': 'Maintain GST filing discipline',
            'benefit': 'Stay compliant with tax authorities'
        })
    
    # Income tax recommendations
    recommendations.append({
        'compliance_area': 'Income Tax',
        'status': 'Review',
        'priority': 'Medium',
        'action': 'Ensure timely filing of income tax returns and ITR',
        'benefit': 'Strengthen credit profile and compliance record'
    })
    
    return recommendations

def generate_recommendation(df, analysis=None):
    """Generate comprehensive AI-powered recommendations"""
    if df is None or df.empty:
        return {
            'executive_summary': 'Unable to generate recommendations - insufficient data',
            'recommendations': []
        }
    
    recommendations_dict = {
        'executive_summary': '',
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'business_id': str(df['business_id'].iloc[0]),
        
        # Cash flow analysis
        'cash_flow_analysis': analyze_cash_flow_health(df),
        
        # Debt obligations
        'debt_analysis': analyze_debt_obligations(df),
        
        # Cost optimization
        'cost_optimization': recommend_cost_optimization(df, analysis) if analysis else [],
        
        # Financial products
        'financial_products': recommend_financial_products(analysis) if analysis else [],
        
        # Industry risks
        'industry_risks': assess_industry_risks(df),
        
        # Tax compliance
        'tax_compliance': assess_tax_compliance(df),
        
        # Action plan
        'action_plan': {
            'immediate': [],
            'short_term': [],
            'medium_term': [],
            'long_term': []
        }
    }
    
    # Build action plan based on analysis
    if analysis:
        health_score = analysis['financial_health']['health_score']
        risk_category = analysis['financial_health']['risk_category']
        
        if risk_category == 'Critical Risk':
            recommendations_dict['action_plan']['immediate'] = [
                'Emergency financial review and restructuring',
                'Halt non-essential expenses immediately',
                'Reach out to lenders to discuss restructuring options',
                'Consider strategic business review'
            ]
            recommendations_dict['executive_summary'] = f'CRITICAL ALERT: Financial Health Score {health_score}/100. Immediate intervention required.'
        
        elif risk_category == 'High Risk':
            recommendations_dict['action_plan']['immediate'] = [
                'Conduct comprehensive cost review',
                'Improve receivables collection',
                'Negotiate extended payment terms with suppliers'
            ]
            recommendations_dict['action_plan']['short_term'] = [
                'Improve operational efficiency',
                'Focus on revenue growth',
                'Reduce debt obligations'
            ]
            recommendations_dict['executive_summary'] = f'WARNING: Financial Health Score {health_score}/100. Significant improvements needed.'
        
        elif risk_category == 'Medium Risk':
            recommendations_dict['action_plan']['short_term'] = [
                'Optimize working capital management',
                'Improve profitability margins',
                'Monitor debt levels'
            ]
            recommendations_dict['action_plan']['medium_term'] = [
                'Plan for controlled growth',
                'Invest in process improvements',
                'Develop contingency plans'
            ]
            recommendations_dict['executive_summary'] = f'CAUTION: Financial Health Score {health_score}/100. Monitor key metrics and implement improvements.'
        
        else:  # Low Risk
            recommendations_dict['action_plan']['medium_term'] = [
                'Plan strategic expansion initiatives',
                'Invest in technology and automation',
                'Explore new revenue streams'
            ]
            recommendations_dict['action_plan']['long_term'] = [
                'Build reserves for future uncertainties',
                'Plan for succession and sustainability',
                'Consider market expansion'
            ]
            recommendations_dict['executive_summary'] = f'POSITIVE: Financial Health Score {health_score}/100. Maintain current trajectory with strategic growth initiatives.'
    
    return recommendations_dict
