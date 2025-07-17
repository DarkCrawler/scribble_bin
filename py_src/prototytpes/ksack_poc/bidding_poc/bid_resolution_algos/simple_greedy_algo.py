def select_bids_greedy(bids_main_df, stock_limit):
    capacity = stock_limit
    total_weight = 0
    total_cost = 0
    selected_items = []

    df_greed = bids_main_df.sort_values(by="bid_priority_score", ascending=True)

    for _, row in df_greed.iterrows():
        weight = row['pax_count']  # Extract as scalar
        if total_weight + weight <= capacity:
            selected_items.append(row['bid_order_id'])
            total_weight += row['pax_count']
            print('*****',row['total_bid_amount'])
            total_cost += row['total_normalized_bid']
        if total_weight == capacity:
            break;

    df_result = bids_main_df[bids_main_df['bid_order_id'].isin(selected_items)]

    return df_result, total_cost
