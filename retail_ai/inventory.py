import pandas as pd

def analyze_inventory(products_df, sales_df):
    """
    Analyze stock levels and past sales to predict demand and identify
    actionable insights for the retailer.
    """
    insights = []
    
    try:
        # Merge products with total sales
        sales_summary = sales_df.groupby('product_id')['quantity_sold'].sum().reset_index()
        sales_summary.rename(columns={'quantity_sold': 'total_sold'}, inplace=True)
        
        merged_df = pd.merge(products_df, sales_summary, on='product_id', how='left')
        merged_df['total_sold'] = merged_df['total_sold'].fillna(0)
        
        for _, row in merged_df.iterrows():
            item = {
                'id': row['product_id'],
                'name': row['name'],
                'stock': row['stock'],
                'total_sold': row['total_sold'],
                'status': 'Normal',
                'action': 'None'
            }
            
            # Simple rules for inventory optimization
            # Reorder threshold logic
            if row['stock'] < 10:
                item['status'] = 'Low Stock'
                item['action'] = 'Reorder soon'
            
            # Demand prediction logic (simplified)
            # If item represents a high proportion of sales relative to stock
            if row['total_sold'] > row['stock'] * 0.5 and row['stock'] < 20:
                item['status'] = 'High Demand Risk'
                item['action'] = 'Immediate Reorder'
                
            # Overstock logic
            if row['stock'] > 100 and row['total_sold'] < 5:
                item['status'] = 'Overstock'
                item['action'] = 'Consider Discount'
                
            insights.append(item)
            
        return insights
    except Exception as e:
        print(f"Error analyzing inventory: {e}")
        return []
