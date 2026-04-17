import pandas as pd

def get_recommendations(products_df, current_product_id=None, user_history=None, limit=3):
    """
    Suggest products based on logic.
    For simplicity, if we pass a current product, we suggest items in the same category.
    If no context, return top random / popular items as recommendations.
    """
    if current_product_id is not None:
        try:
            # Get the category of the current product
            product_row = products_df[products_df['product_id'] == current_product_id]
            if not product_row.empty:
                category = product_row.iloc[0]['category']
                
                # Recommend other products in the same category
                recommendations = products_df[
                    (products_df['category'] == category) & 
                    (products_df['product_id'] != current_product_id)
                ]
                
                # If we don't have enough in the same category, get some random others
                if len(recommendations) < limit:
                    others = products_df[products_df['product_id'] != current_product_id]
                    # Exclude the ones already in recommendations
                    others = others[~others['product_id'].isin(recommendations['product_id'])]
                    recommendations = pd.concat([recommendations, others.sample(n=min(limit - len(recommendations), len(others)))])
                
                return recommendations.head(limit).to_dict('records')
        except Exception as e:
            print(f"Error in recommendation: {e}")
            
    # Default recommendations: return a mix
    # We could sort by some heuristic, here just take a sample
    if not products_df.empty:
        return products_df.sample(n=min(limit, len(products_df))).to_dict('records')
    return []
