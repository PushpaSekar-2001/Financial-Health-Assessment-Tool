from data_loader import load_business_data
import traceback

try:
    df = load_business_data('SME_1')
    print('Returned type:', type(df))
    if df is None:
        print('df is None')
    else:
        print(df.columns.tolist())
        print(df.head(1).to_dict('records'))
except Exception:
    traceback.print_exc()
