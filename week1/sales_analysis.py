import pandas as pd

sales = pd.DataFrame({
    "month": ["January", "February", "March", "April", "May", "June"],
    "revenue": [80000, 85000, 82000, 95000, 110000, 130000],
    "products_sold": [400, 420, 410, 450, 500, 550],
})

sales = sales.set_index("month")

# Part A: Data analysis

# A1. Total revenue for the six months
total_revenue = sales["revenue"].sum()
# A2. Average monthly revenue
average_revenue = sales["revenue"].mean()
# A3. Month with the highest revenue
highest_month = sales["revenue"].idxmax()
highest_revenue = sales["revenue"].max()
# A4. Month with the lowest revenue
lowest_month = sales["revenue"].idxmin()
lowest_revenue = sales["revenue"].min()
# A5. Total number of products sold
total_products = sales["products_sold"].sum()
# A6. Average revenue per product for each month
sales["revenue_per_product"] = sales["revenue"] / sales["products_sold"]
# A7. Percentage increase in revenue from January to June
jan_revenue = sales["revenue"].loc["January"]
jun_revenue = sales["revenue"].loc["June"]
revenue_increase_pct = (jun_revenue - jan_revenue) / jan_revenue * 100

print("PART A: DATA ANALYSIS")
print(f"A1. Total revenue: ${total_revenue:,}")
print(f"A2. Average monthly revenue: ${average_revenue:,.0f}")
print(f"A3. Highest revenue: {highest_month} (${highest_revenue:,})")
print(f"A4. Lowest revenue: {lowest_month} (${lowest_revenue:,})")
print(f"A5. Total products sold: {total_products:,}")
print("A6. Average revenue per product:")
for month, value in sales["revenue_per_product"].items():
    print(f"      {month:<10}${value:.2f}")
print(f"A7. Revenue increase from January to June: {revenue_increase_pct:.1f}%")


# Part B: Identifying trends

# Change compared with the previous month. January has no previous
# month, so its values are NaN.
sales["revenue_change"] = sales["revenue"].diff()
sales["revenue_change_pct"] = sales["revenue"].pct_change() * 100
sales["products_change"] = sales["products_sold"].diff()
sales["revenue_per_product_change"] = sales["revenue_per_product"].diff()

# B1. Did revenue go up every month?
increased_every_month = (sales["revenue_change"].dropna() > 0).all()
# B2. Months where revenue was lower than the month before
decline_months = sales.index[sales["revenue_change"] < 0].tolist()
# B3. Change from February to March (stored in the March row)
feb_mar_change = sales["revenue_change"].loc["March"]
feb_mar_change_pct = sales["revenue_change_pct"].loc["March"]
# B4. Products sold in January compared with June
jan_products = sales["products_sold"].loc["January"]
jun_products = sales["products_sold"].loc["June"]
products_increase_pct = (jun_products - jan_products) / jan_products * 100
# B5. Average revenue per product in January compared with June
jan_rev_per_product = sales["revenue_per_product"].loc["January"]
jun_rev_per_product = sales["revenue_per_product"].loc["June"]
rev_per_product_increase_pct = (
    (jun_rev_per_product - jan_rev_per_product) / jan_rev_per_product * 100
)

print("\nPART B: IDENTIFYING TRENDS")
print("Change from the previous month:")
print(f"      {'':<10}{'revenue':>10}{'revenue %':>11}{'products':>10}{'$ per product':>15}")
for month, row in sales.iloc[1:].iterrows():
    print(f"      {month:<10}"
          f"{row['revenue_change']:>+10,.0f}"
          f"{row['revenue_change_pct']:>+10.2f}%"
          f"{row['products_change']:>+10.0f}"
          f"{row['revenue_per_product_change']:>+15.2f}")

print(f"B1. Did revenue increase every month? "
      f"{'Yes' if increased_every_month else 'No'}")
print(f"B2. Month(s) with lower revenue than the month before: "
      f"{', '.join(decline_months)}")
print(f"B3. Revenue change from February to March: "
      f"{feb_mar_change:+,.0f} NZD ({feb_mar_change_pct:+.2f}%)")
print(f"B4. Did products sold increase from January to June? "
      f"{'Yes' if jun_products > jan_products else 'No'}, "
      f"from {jan_products} to {jun_products} ({products_increase_pct:+.1f}%)")
print(f"B5. Did average revenue per product increase from January to June? "
      f"{'Yes' if jun_rev_per_product > jan_rev_per_product else 'No'}, "
      f"from ${jan_rev_per_product:.2f} to ${jun_rev_per_product:.2f} "
      f"({rev_per_product_increase_pct:+.1f}%)")


# Part C: Business interpretation

# Months with revenue above the six-month average
above_average = sales.index[sales["revenue"] > average_revenue].tolist()

# Revenue in January to March compared with April to June
jan_to_mar = sales["revenue"].loc["January":"March"].sum()
apr_to_jun = sales["revenue"].loc["April":"June"].sum()
apr_to_jun_increase_pct = (apr_to_jun - jan_to_mar) / jan_to_mar * 100

# Split the January to June revenue increase into two parts:
#   - more products sold, valued at January's revenue per product
#   - higher revenue per product, on all the products sold in June
revenue_increase = jun_revenue - jan_revenue
increase_from_products = (jun_products - jan_products) * jan_rev_per_product
increase_from_rev_per_product = (
    (jun_rev_per_product - jan_rev_per_product) * jun_products
)

print("\nPART C: SUPPORTING CALCULATIONS")
print(f"Months above the average of ${average_revenue:,.0f}: "
      f"{', '.join(above_average)}")
print(f"Revenue January to March: ${jan_to_mar:,}")
print(f"Revenue April to June: ${apr_to_jun:,} "
      f"({apr_to_jun_increase_pct:+.1f}% on January to March)")
print(f"Revenue increase from January to June: ${revenue_increase:,}")
print(f"  from selling more products: ${increase_from_products:,.0f} "
      f"({increase_from_products / revenue_increase:.0%})")
print(f"  from higher revenue per product: ${increase_from_rev_per_product:,.0f} "
      f"({increase_from_rev_per_product / revenue_increase:.0%})")


# Part C answers
#
# C1. Three findings
#
# 1. Revenue grew 62.5% in six months, from $80,000 in January to
#    $130,000 in June. Total revenue was $582,000, or $97,000 a month on
#    average. Only May and June were above that average.
#
# 2. Growth was slow until March and fast from April. March was the only
#    month where revenue fell (-$3,000, or -3.53% on February). From
#    April, revenue went up every month and each rise was bigger than
#    the one before (+$13,000, +$15,000, +$20,000). April to June brought
#    in $335,000, which is 35.6% more than January to March ($247,000).
#
# 3. Each product sold is bringing in more money. Average revenue per
#    product went from $200.00 in January to $236.36 in June (+18.2%),
#    with the biggest jump in June (+$16.36 on May).
#
# C2. Growth from sales volume, revenue per product, or both?
#
# Both, with sales volume (products sold) doing more of the work.
# Products sold went up 37.5% (400 to 550) and average revenue per
# product went up 18.2% between January and June. If each product in
# June had still brought in January's $200, June revenue would have been
# 550 x $200 = $110,000. So of the $50,000 increase, $30,000 came from
# selling more products and $20,000 from higher revenue per product.
# The two also moved together month by month: both fell in March and
# both rose in every other month.
#
# C3. Two recommendations
#
# 1. Find out what drove the growth from April and use it earlier in the
#    year. The company should check what changed in April and plan a similar
#    campaign for January to March, the weakest three months.
#
# 2. Keep raising revenue per product. It accounts for $20,000 of the
#    $50,000 increase, and products sold kept growing at the same time,
#    so the higher spend per item has not reduced the number of products
#    sold so far. Product bundles and add-on offers at checkout could
#    lift it further. Products sold and revenue per product should be
#    tracked separately every month, so the company sees early if higher
#    prices start to reduce sales volume.


# Output
# PART A: DATA ANALYSIS
# A1. Total revenue: $582,000
# A2. Average monthly revenue: $97,000
# A3. Highest revenue: June ($130,000)
# A4. Lowest revenue: January ($80,000)
# A5. Total products sold: 2,730
# A6. Average revenue per product:
#       January   $200.00
#       February  $202.38
#       March     $200.00
#       April     $211.11
#       May       $220.00
#       June      $236.36
# A7. Revenue increase from January to June: 62.5%
#
# PART B: IDENTIFYING TRENDS
# Change from the previous month:
#                    revenue  revenue %  products  $ per product
#       February      +5,000     +6.25%       +20          +2.38
#       March         -3,000     -3.53%       -10          -2.38
#       April        +13,000    +15.85%       +40         +11.11
#       May          +15,000    +15.79%       +50          +8.89
#       June         +20,000    +18.18%       +50         +16.36
# B1. Did revenue increase every month? No
# B2. Month(s) with lower revenue than the month before: March
# B3. Revenue change from February to March: -3,000 NZD (-3.53%)
# B4. Did products sold increase from January to June? Yes, from 400 to 550 (+37.5%)
# B5. Did average revenue per product increase from January to June? Yes, from $200.00 to $236.36 (+18.2%)
#
# PART C: SUPPORTING CALCULATIONS
# Months above the average of $97,000: May, June
# Revenue January to March: $247,000
# Revenue April to June: $335,000 (+35.6% on January to March)
# Revenue increase from January to June: $50,000
#   from selling more products: $30,000 (60%)
#   from higher revenue per product: $20,000 (40%)
