import pandas as pd
from bid_resolution_algos.bid_resolution_orchestrator import orchestrate_bid_evaluation


def resolve_bids_poc(request_json):
    results = orchestrate_bid_evaluation(request_json)
    ks_selected_bids_df = results[0]
    ks_total_bid_amount = results[1]
    greedy_selected_bids_df = results[2]
    greedy_total_amount = results[3]
    master_df = results[4]

    normalized_score = master_df.rename(columns={
        'bid_order_id': 'bid_id',
        'total_bid_amount': 'total_bid_vale',
        'fft_score': 'fft_score',
        'fbc_score': 'fbc_score',
        'ph_score': 'purchase_history_score',
        'bid_normalized_score': 'normalized_bid',
        'total_normalized_bid': 'total_normalized_bid',
        'bid_priority_score': 'bid_priority_score'
    })[['bid_id', 'total_bid_vale', 'fft_score', 'fbc_score', 'purchase_history_score', 'normalized_bid',
        'total_normalized_bid', 'bid_priority_score']]

    normalized_score_json = normalized_score.to_dict(orient='records')

    ks_result = ks_selected_bids_df.rename(
        columns={
            'bid_order_id': 'bid_id',
            'bid_priority_score': 'bid_priority_score',
            'pax_count': 'pax_count',
            'total_normalized_bid': 'total_normalized_bid',
            'total_bid_amount': 'total_bid_amount'
        })[['bid_id', 'bid_priority_score', 'pax_count', 'total_normalized_bid', 'total_bid_amount']]

    ks_result_json = ks_result.to_dict(orient='records')

    sp_result = greedy_selected_bids_df.rename(
        columns={
            'bid_order_id': 'bid_id',
            'bid_priority_score': 'bid_priority_score',
            'pax_count': 'pax_count',
            'total_normalized_bid': 'total_normalized_bid',
            'total_bid_amount': 'total_bid_amount'
        })[['bid_id', 'bid_priority_score', 'pax_count', 'total_normalized_bid', 'total_bid_amount']]

    sp_result_json = sp_result.to_dict(orient='records')

    final_response = {
        "normalized_score": normalized_score_json,
        "sp_result": sp_result_json,
        "ks_result": ks_result_json,
        "ks_result_sale_value": ks_total_bid_amount,
        "sp_resul_sale_value": greedy_total_amount
    }

    print("*****", final_response)

    return final_response

# return None;
