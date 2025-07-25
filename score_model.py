def normalize_column(col):
    return (col - col.min()) / (col.max() - col.min() + 1e-6)

def calculate_score(df):
    df = df.copy()
    df['repay_ratio'] = df['total_repaid'] / df['total_borrowed'].replace(0, 1)

    df['score'] = (
        0.3 * (1 - normalize_column(df['repay_ratio'])) +
        0.3 * normalize_column(df['liquidation_count']) +
        0.2 * normalize_column(df['total_borrowed']) +
        0.2 * (1 - normalize_column(df['interaction_count']))
    ) * 1000

    df['score'] = df['score'].round().astype(int)
    return df[['wallet_id', 'score']]

