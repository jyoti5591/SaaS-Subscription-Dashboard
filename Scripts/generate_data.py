import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random, uuid

np.random.seed(42)
N = 500

# dim_customers.csv
customers = pd.DataFrame({
    'customer_id': [f'C{i:04d}' for i in range(1, N+1)],
    'company_name': [f'Company_{i}' for i in range(1, N+1)],
    'country': np.random.choice(['US','IN','GB','DE','CA','AU'], N),
    'industry': np.random.choice(['SaaS','FinTech','HealthTech','EdTech','RetailTech'], N),
    'signup_date': pd.date_range('2021-01-01', periods=N, freq='D')[:N],
    'referral_source': np.random.choice(['Organic','Paid','Referral','Partner'], N),
    'is_trial': np.random.choice([True, False], N, p=[0.3, 0.7])
})

# fact_subscriptions.csv
plans = ['Starter','Growth','Pro','Enterprise']
subs = []
for cid in customers['customer_id']:
    plan = np.random.choice(plans, p=[0.3,0.3,0.25,0.15])
    mrr = {'Starter':49,'Growth':149,'Pro':399,'Enterprise':999}[plan]
    start = datetime(2021,1,1) + timedelta(days=random.randint(0,700))
    subs.append({
        'subscription_id': str(uuid.uuid4())[:8],
        'customer_id': cid,
        'plan': plan,
        'mrr': mrr,
        'arr': mrr * 12,
        'start_date': start.date(),
        'end_date': (start + timedelta(days=random.randint(30,730))).date(),
        'churn_flag': np.random.choice([0,1], p=[0.75,0.25]),
        'upgrade_flag': np.random.choice([0,1], p=[0.8,0.2]),
        'downgrade_flag': np.random.choice([0,1], p=[0.9,0.1]),
        'auto_renew': np.random.choice([True,False], p=[0.7,0.3])
    })
pd.DataFrame(subs).to_csv('data/fact_subscriptions.csv', index=False)

# fact_mrr_monthly.csv — one row per customer per month
months = pd.date_range('2021-01-01', '2023-12-01', freq='MS')
mrr_rows = []
for _, row in customers.iterrows():
    for m in months:
        if random.random() > 0.2:
            mrr_rows.append({'customer_id': row['customer_id'],
                             'month': m.date(),
                             'mrr': random.choice([49,149,399,999]),
                             'country': row['country']})
pd.DataFrame(mrr_rows).to_csv('data/fact_mrr_monthly.csv', index=False)

# dim_date.csv
dates = pd.date_range('2021-01-01','2024-12-31')
dim_date = pd.DataFrame({'date': dates,
    'year': dates.year, 'quarter': dates.quarter,
    'month': dates.month, 'month_name': dates.strftime('%B'),
    'week': dates.isocalendar().week,
    'day_of_week': dates.day_name()})
dim_date.to_csv('data/dim_date.csv', index=False)

customers.to_csv('data/dim_customers.csv', index=False)
print("All CSVs generated ✓")