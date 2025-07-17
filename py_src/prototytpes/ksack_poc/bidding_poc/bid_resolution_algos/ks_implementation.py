import numpy as np


def knapsack_from_dataframe(df, max_capacity):
    n = len(df)
    values = df["total_normalized_bid"].tolist()
    weights = df["pax_count"].tolist()
    items = df["bid_order_id"].tolist()
    dp = np.zeros((n + 1, max_capacity + 1))

    # Fill DP table
    for i in range(1, n + 1):
        for w in range(1, max_capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # Traceback to find selected items
    w = max_capacity
    selected_items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # Item was included
            selected_items.append(items[i - 1])
            w -= weights[i - 1]

    df_selected = df[df["bid_order_id"].isin(selected_items)].reset_index(drop=True)

    total_cost = 0
    for _, row in df_selected.iterrows():
        total_cost += row['total_normalized_bid']

    return df_selected, dp[n][max_capacity], total_cost  # Return selected items and max value
