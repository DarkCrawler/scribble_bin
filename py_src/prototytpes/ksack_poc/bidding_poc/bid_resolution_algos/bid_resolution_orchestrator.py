import pandas as pd
from click.core import batch
from tabulate import tabulate
import numpy as np

from .ks_implementation import knapsack_from_dataframe
from .simple_greedy_algo import select_bids_greedy


def assign_pph_score(val):
    past_purchase_score = pd.DataFrame({
        'min': [0, 1, 4],
        'max': [0, 3, 9999],
        'score': [1, 0.8, 0.5]
    })
    row = past_purchase_score[(past_purchase_score['min'] <= val) & (past_purchase_score['max'] >= val)]
    return row['score'].values[0] if not row.empty else None  # Returns None if no match


def master_data_frame_creation(bid_info_request_attrib):
    pdf = pd.DataFrame(bid_info_request_attrib)

    # chaning data types
    pdf["purchase_history"] = pdf["purchase_history"].astype(int)
    pdf["bid_value"] = pdf["bid_value"].astype(float)
    pdf["pax_count"] = pdf["pax_count"].astype(int)

    # scoring_config_tables
    fft_score_df = pd.DataFrame({
        "pax_fft": ["GOLD", "SILVER", "NO FFT"],
        "fft_score": [1.2, 1.1, 1.0]
    })

    fbc_score_df = pd.DataFrame({
        "fare_basis_code": ["FLEX", "CHOICE", "SAVER"],
        "fbc_score": [1.1, 1.05, 1.0]
    })

    # allot scoring to rows

    # joing with fft_score
    pdf = pdf.merge(fft_score_df, on="pax_fft", how="left")

    # joing with fbc_score
    pdf = pdf.merge(fbc_score_df, on="fare_basis_code", how="left")

    # assign pph score
    pdf['ph_score'] = pdf['purchase_history'].apply(assign_pph_score)

    # creation of normalized_bid_val
    pdf['bid_normalized_score'] = np.round(pdf[['fft_score', 'fbc_score', 'ph_score', 'bid_value']].prod(axis=1),
                                           0).astype(int)

    pdf['total_normalized_bid'] = pdf['pax_count'] * pdf['bid_normalized_score']

    pdf['total_bid_amount'] = pdf['pax_count'] * pdf['bid_value']

    pdf['bid_priority_score'] = pdf['total_normalized_bid'].rank(ascending=False, method='dense').astype(int)

    return pdf


def orchestrate_bid_evaluation(evaluation_request):
    bid_info_request_attrib = evaluation_request['bids']
    available_inventory = int(evaluation_request['stock_limit'])

    master_df = master_data_frame_creation(bid_info_request_attrib)

    selected_columns = ['bid_order_id', 'total_normalized_bid', 'bid_priority_score', 'pax_count']

    # print(tabulate(master_df[selected_columns], headers='keys', tablefmt='pretty'))

    # Steps to do :
    # 1 : call KS and get the values
    ks_result_tuple = knapsack_from_dataframe(master_df, available_inventory)
    ks_selected_bids_df = ks_result_tuple[0]
    ks_total_amount = ks_result_tuple[1]
    ks_total_bid_amount = ks_result_tuple[2]

    # 2 : call simple score based evaluation and get the values
    greedy_result_tuple = select_bids_greedy(master_df, available_inventory)
    greedy_selected_bids_df = greedy_result_tuple[0]
    greedy_total_amount = greedy_result_tuple[1]

    # 3 : pass #1 , #2 and scoring data_structure to service to form the response

    return ks_selected_bids_df, ks_total_bid_amount, greedy_selected_bids_df, greedy_total_amount, master_df
