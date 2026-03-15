import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


import os
print(os.getcwd())
os.chdir(r"C:\Users\acer\OneDrive\文件\python files")

st.title("Food Delivery Analysis")

conn = sqlite3.connect('fooddelivery.db')
df = pd.read_sql_query("SELECT * FROM food_delivery_table", conn)
conn.close()


st.header("Entire Table")
if st.button("click to view"):
    st.dataframe(df)


st.header("Top spending customers")
if st.button("click to view",key="k1"):
    top10 = df.nlargest(10, 'Final_Amount')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top10['Customer_ID'].astype(str), top10['Final_Amount'], color='steelblue')
    ax.set_xlabel('Customer_ID')
    ax.set_ylabel('Final_Amount')
    ax.set_ylim(top10['Final_Amount'].min() - 10, top10['Final_Amount'].max() + 10)
    ax.set_title('Top 10 Spending Customers')
    plt.xticks(rotation=45)
    st.pyplot(fig)



st.header("Age Group vs Order Value")
if st.button("Click to View", key="age_chart_button"):
    age_group_order = df.groupby('age_group')['Order_Value'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(age_group_order['age_group'].astype(str), age_group_order['Order_Value'], color='steelblue')
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Order Value')
    ax.set_title('Age Group vs Order Value')
    ax.set_ylim(age_group_order['Order_Value'].min() - 10, age_group_order['Order_Value'].max() + 10)
    plt.xticks(rotation=45)
    st.pyplot(fig)





st.header("Weekend vs Weekday Orders")
if st.button("Click to View", key="day_type_button"):
    day_type_order = df.groupby('Order_Day')['Order_Value'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(day_type_order['Order_Day'].astype(str), day_type_order['Order_Value'], color='steelblue')
    ax.set_xlabel('Order day')
    ax.set_ylabel('Order Value')
    ax.set_title('Weekend vs Weekday Orders')
    ax.set_ylim(day_type_order['Order_Value'].min() - 10, day_type_order['Order_Value'].max() + 10)
    plt.xticks(rotation=45)
    st.pyplot(fig)


df['Month'] = pd.to_datetime(df['Order_Date']).dt.month_name()

st.header("Month vs Final Amount")
if st.button("Click to View", key="month_button"):
    month_order_list = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
    
    month_order = df.groupby('Month')['Final_Amount'].sum().reset_index()
    month_order['Month'] = pd.Categorical(month_order['Month'], categories=month_order_list, ordered=True)
    month_order = month_order.sort_values('Month')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(month_order['Month'].astype(str), month_order['Final_Amount'], color='steelblue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Final Amount')
    ax.set_title('Month vs Final Amount')
    ax.set_ylim(month_order['Final_Amount'].min() - 10, month_order['Final_Amount'].max() + 10)
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.header("Impact of Discounts on Profit")
if st.button("Click to View", key="discount_button"):
    discount_profit = df.groupby('Discount_Applied')['Profit_Margin'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(discount_profit['Discount_Applied'].astype(str), discount_profit['Profit_Margin'], color='steelblue')
    ax.set_xlabel('Discount Applied')
    ax.set_ylabel('Average Profit Margin')
    ax.set_title('Impact of Discounts on Profit')
    plt.xticks(rotation=45)
    st.pyplot(fig)


st.header("Top 5 Cities and Cuisines by Revenue")
if st.button("Click to View", key="city_cuisine_button"):
    top5_cities = df.groupby('City')['Final_Amount'].sum().nlargest(5).reset_index()
    top5_cuisines = df.groupby('Cuisine_Type')['Final_Amount'].sum().nlargest(5).reset_index()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.bar(top5_cities['City'], top5_cities['Final_Amount'], color='steelblue')
    ax1.set_xlabel('City')
    ax1.set_ylabel('Final Amount')
    ax1.set_title('Top 5 Cities by Final Amount')
    ax1.set_ylim(top5_cities['Final_Amount'].min() - 10, top5_cities['Final_Amount'].max() + 10)
    ax1.tick_params(axis='x', rotation=45)
    
    ax2.bar(top5_cuisines['Cuisine_Type'], top5_cuisines['Final_Amount'], color='coral')
    ax2.set_xlabel('Cuisine Type')
    ax2.set_ylabel('Final Amount')
    ax2.set_title('Top 5 Cuisines by Final Amount')
    ax2.set_ylim(top5_cuisines['Final_Amount'].min() - 10, top5_cuisines['Final_Amount'].max() + 10)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)


st.header("Average Delivery Time by City")
if st.button("Click to View", key="delivery_time_button"):
    avg_delivery = df.groupby('City')['Delivery_Time_Min'].mean().reset_index()
    avg_delivery.columns = ['City', 'Avg_Delivery_Time']
    avg_delivery = avg_delivery.sort_values('Avg_Delivery_Time', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(avg_delivery['City'], avg_delivery['Avg_Delivery_Time'], color='steelblue')
    ax.set_xlabel('City')
    ax.set_ylabel('Average Delivery Time (mins)')
    ax.set_title('Average Delivery Time by City')
    ax.set_ylim(avg_delivery['Avg_Delivery_Time'].min() - 1, avg_delivery['Avg_Delivery_Time'].max() + 1)
    plt.xticks(rotation=45)
    st.pyplot(fig)


st.header("Delivery Delay Analysis")
if st.button("Click to View", key="delivery_delay_button"):
    
    df['Expected_Time'] = df['Distance_km'] * 3
    df['Delay'] = df['Delivery_Time_Min'] - df['Expected_Time']
    df['Status'] = df['Delay'].apply(lambda x: 'Delayed' if x > 0 else 'On Time')
    
    colors = df['Status'].map({'Delayed': 'red', 'On Time': 'green'})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(df['Distance_km'], df['Delivery_Time_Min'], c=colors, alpha=0.6)
    
    ax.plot(sorted(df['Distance_km']), 
            [x * 3 for x in sorted(df['Distance_km'])], 
            color='blue', linestyle='--', label='Expected Time')
    
    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Delivery Time (mins)')
    ax.set_title('Delivery Delay Analysis')
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', label='Delayed'),
                       Patch(facecolor='green', label='On Time'),
                       plt.Line2D([0], [0], color='blue', linestyle='--', label='Expected Time')]
    ax.legend(handles=legend_elements)
    
    st.pyplot(fig)


st.header("Average Delivery Time by Rating")
if st.button("Click to View", key="rating_button"):
    avg_delivery_rating = df.groupby('Delivery_Rating')['Delivery_Time_Min'].mean().reset_index()
    avg_delivery_rating.columns = ['Delivery_Rating', 'Avg_Delivery_Time']
    avg_delivery_rating = avg_delivery_rating.sort_values('Delivery_Rating')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(avg_delivery_rating['Delivery_Rating'].astype(str), avg_delivery_rating['Avg_Delivery_Time'], color='steelblue')
    ax.set_xlabel('Delivery Rating')
    ax.set_ylabel('Average Delivery Time (mins)')
    ax.set_title('Average Delivery Time by Delivery Rating')
    ax.set_ylim(avg_delivery_rating['Avg_Delivery_Time'].min() - 1, avg_delivery_rating['Avg_Delivery_Time'].max() + 1)
    plt.xticks(rotation=0)
    st.pyplot(fig)


st.header("Top Rated Restaurants")
if st.button("Click to View", key="restaurant_button"):
    avg_restaurant_rating = df.groupby('Restaurant_Name')['Restaurant_Rating'].mean().reset_index()
    avg_restaurant_rating = avg_restaurant_rating.sort_values('Restaurant_Rating', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(avg_restaurant_rating['Restaurant_Name'], avg_restaurant_rating['Restaurant_Rating'], color='steelblue')
    ax.set_xlabel('Restaurant Name')
    ax.set_ylabel('Restaurant Rating')
    ax.set_title('Top 10 Restaurants by Rating')
    ax.set_ylim(avg_restaurant_rating['Restaurant_Rating'].min() - 0.1, avg_restaurant_rating['Restaurant_Rating'].max() + 0.1)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)



st.header("Cancellation Rate by Restaurant")
if st.button("Click to View", key="cancellation_button"):
    total_orders = df.groupby('Restaurant_Name')['Order_Status'].count()
    cancelled_orders = df[df['Order_Status'].isin(['Canceled', 'Cancelled', 'cancelled', 'canceled'])].groupby('Restaurant_Name')['Order_Status'].count()
    
    cancellation_rate = (cancelled_orders / total_orders * 100).fillna(0).reset_index()
    cancellation_rate.columns = ['Restaurant_Name', 'Cancellation_Rate']
    cancellation_rate = cancellation_rate.sort_values('Cancellation_Rate', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(cancellation_rate['Restaurant_Name'], cancellation_rate['Cancellation_Rate'], color='red')
    ax.set_xlabel('Restaurant Name')
    ax.set_ylabel('Cancellation Rate (%)')
    ax.set_title('Top 10 Restaurants by Cancellation Rate')
    ax.set_ylim(0, cancellation_rate['Cancellation_Rate'].max() + 1)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)


st.header("Cuisine-wise Performance")
if st.button("Click to View", key="cuisine_performance_button"):
    cuisine_performance = df.groupby('Cuisine_Type').agg(
        Total_Orders=('Order_Value', 'count'),
        Avg_Order_Value=('Order_Value', 'mean'),
        Total_Revenue=('Final_Amount', 'sum'),
        Avg_Rating=('Restaurant_Rating', 'mean'),
        Avg_Delivery_Time=('Delivery_Time_Min', 'mean')
    ).reset_index()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    axes[0, 0].bar(cuisine_performance['Cuisine_Type'], cuisine_performance['Total_Orders'], color='steelblue')
    axes[0, 0].set_title('Total Orders by Cuisine')
    axes[0, 0].set_xlabel('Cuisine Type')
    axes[0, 0].set_ylabel('Total Orders')
    axes[0, 0].set_ylim(cuisine_performance['Total_Orders'].min() - 10, cuisine_performance['Total_Orders'].max() + 10)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    axes[0, 1].bar(cuisine_performance['Cuisine_Type'], cuisine_performance['Total_Revenue'], color='coral')
    axes[0, 1].set_title('Total Revenue by Cuisine')
    axes[0, 1].set_xlabel('Cuisine Type')
    axes[0, 1].set_ylabel('Total Revenue')
    axes[0, 1].set_ylim(cuisine_performance['Total_Revenue'].min() - 10, cuisine_performance['Total_Revenue'].max() + 10)
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    axes[1, 0].bar(cuisine_performance['Cuisine_Type'], cuisine_performance['Avg_Rating'], color='green')
    axes[1, 0].set_title('Average Rating by Cuisine')
    axes[1, 0].set_xlabel('Cuisine Type')
    axes[1, 0].set_ylabel('Average Rating')
    axes[1, 0].set_ylim(cuisine_performance['Avg_Rating'].min() - 0.1, cuisine_performance['Avg_Rating'].max() + 0.1)
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    axes[1, 1].bar(cuisine_performance['Cuisine_Type'], cuisine_performance['Avg_Delivery_Time'], color='purple')
    axes[1, 1].set_title('Average Delivery Time by Cuisine')
    axes[1, 1].set_xlabel('Cuisine Type')
    axes[1, 1].set_ylabel('Average Delivery Time (mins)')
    axes[1, 1].set_ylim(cuisine_performance['Avg_Delivery_Time'].min() - 1, cuisine_performance['Avg_Delivery_Time'].max() + 1)
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.suptitle('Cuisine-wise Performance Analysis', fontsize=16)
    plt.tight_layout()
    st.pyplot(fig)


st.header("Peak Hour Demand Analysis")
if st.button("Click to View", key="peak_hour_button"):
    peak_hour = df.groupby('Peak_Hour').agg(
        Total_Orders=('Order_Value', 'count'),
        Total_Revenue=('Final_Amount', 'sum'),
        Avg_Delivery_Time=('Delivery_Time_Min', 'mean')
    ).reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    axes[0].bar(peak_hour['Peak_Hour'].astype(str), peak_hour['Total_Orders'], color='steelblue')
    axes[0].set_title('Total Orders by Peak Hour')
    axes[0].set_xlabel('Peak Hour')
    axes[0].set_ylabel('Total Orders')
    axes[0].set_ylim(peak_hour['Total_Orders'].min() - 10, peak_hour['Total_Orders'].max() + 10)
    axes[0].tick_params(axis='x', rotation=45)

    axes[1].bar(peak_hour['Peak_Hour'].astype(str), peak_hour['Total_Revenue'], color='coral')
    axes[1].set_title('Total Revenue by Peak Hour')
    axes[1].set_xlabel('Peak Hour')
    axes[1].set_ylabel('Total Revenue')
    axes[1].set_ylim(peak_hour['Total_Revenue'].min() - 10, peak_hour['Total_Revenue'].max() + 10)
    axes[1].tick_params(axis='x', rotation=45)

    axes[2].bar(peak_hour['Peak_Hour'].astype(str), peak_hour['Avg_Delivery_Time'], color='green')
    axes[2].set_title('Avg Delivery Time by Peak Hour')
    axes[2].set_xlabel('Peak Hour')
    axes[2].set_ylabel('Avg Delivery Time (mins)')
    axes[2].set_ylim(peak_hour['Avg_Delivery_Time'].min() - 1, peak_hour['Avg_Delivery_Time'].max() + 1)
    axes[2].tick_params(axis='x', rotation=45)

    plt.suptitle('Peak Hour Demand Analysis', fontsize=16)
    plt.tight_layout()
    st.pyplot(fig)


st.header("Payment Mode Preferences")
if st.button("Click to View", key="payment_mode_button"):
    payment_counts = df['Payment_Mode'].value_counts().reset_index()
    payment_counts.columns = ['Payment_Mode', 'Count']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(payment_counts['Payment_Mode'], payment_counts['Count'], color='steelblue')
    ax.set_xlabel('Payment Mode')
    ax.set_ylabel('Count')
    ax.set_title('Payment Mode vs Count')
    ax.set_ylim(payment_counts['Count'].min() - 10, payment_counts['Count'].max() + 10)
    plt.xticks(rotation=45)
    st.pyplot(fig)


st.header("Cancellation Reason Analysis")
if st.button("Click to View", key="cancellation_reason_button"):
    cancellation_counts = df['Cancellation_Reason'].value_counts().reset_index()
    cancellation_counts.columns = ['Cancellation_Reason', 'Count']

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(cancellation_counts['Cancellation_Reason'], cancellation_counts['Count'], color='red')
    ax.set_xlabel('Cancellation Reason')
    ax.set_ylabel('Count')
    ax.set_title('Cancellation Reason vs Count')
    ax.set_ylim(cancellation_counts['Count'].min() - 10, cancellation_counts['Count'].max() + 10)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

st.header("Total Number of Orders")
if st.button("Click to View", key="total_orders_button"):
    total_orders = len(df)
    st.metric(label="Total Orders", value=total_orders)

st.header("Total Revenue")
if st.button("Click to View", key="total_revenue_button"):
    total_revenue = df['Final_Amount'].sum()
    st.metric(label="Total Revenue", value=f"₹{total_revenue:,.2f}")


st.header("Average Order Value")
if st.button("Click to View", key="avg_order_button"):
    avg_order_value = df['Order_Value'].mean()
    st.metric(label="Average Order Value", value=f"₹{avg_order_value:,.2f}")

st.header("Average Delivery Time")
if st.button("Click to View", key="avg_delivery_button"):
    avg_delivery_time = df['Delivery_Time_Min'].mean()
    st.metric(label="Average Delivery Time", value=f"{avg_delivery_time:,.2f} mins")

st.header("Cancellation Rate")
if st.button("Click to View", key="cancellation_rate_button"):
    cancellation_rate = (df[df['Order_Status'].isin(['Canceled', 'Cancelled', 'cancelled', 'canceled'])].shape[0] / len(df) * 100)
    st.metric(label="Cancellation Rate", value=f"{cancellation_rate:,.2f}%")

st.header("Average Delivery Rating")
if st.button("Click to View", key="avg_rating_button"):
    avg_delivery_rating = df['Delivery_Rating'].mean()
    st.metric(label="Average Delivery Rating", value=f"{avg_delivery_rating:,.2f}")


