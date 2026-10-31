### Nassau Candy Distributor – Product Line Profitability & Margin Performance Analysis

## Project Overview

This project focuses on analyzing sales, profitability, and gross margin performance for Nassau Candy Distributor.

The main objective is to identify high-performing products, evaluate division and factory performance, analyze cost patterns, and generate meaningful business insights through data analysis and an interactive Streamlit dashboard.

The project uses Python-based data analysis and interactive visualizations to support data-driven business decisions.

## Project Objectives

- Analyze total sales, gross profit, and gross margin.
- Identify the most profitable and least profitable products.
- Compare performance across different business divisions.
- Evaluate factory-wise sales and profitability.
- Analyze product costs and identify low-margin products.
- Study monthly sales, profit, and units sold trends.
- Understand customer purchasing patterns.
- Generate data-driven business recommendations.

## Tools & Technologies

- **Programming Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Data Visualization:** Plotly
- **Dashboard Development:** Streamlit
- **Development Environment:** Jupyter Notebook, VS Code
- **Dataset Format:** CSV

## Key Analysis Performed

1. **Data Cleaning:** Checked missing values, duplicate records, and data types.
2. **Product Profitability:** Analyzed product-wise sales, profit, and gross margins.
3. **Division Analysis:** Compared Chocolate, Sugar, and Other divisions.
4. **Factory Analysis:** Evaluated factory-wise sales, profit, and margins.
5. **Cost Analysis:** Identified cost-heavy and low-margin products.
6. **Profit Concentration:** Identified products contributing the largest share of total profit.
7. **Revenue Analysis:** Studied product-wise revenue contribution.
8. **Customer Analysis:** Compared customer sales, profit, order count, and average order value.
9. **Monthly Trends:** Analyzed monthly sales and gross profit.
10. **Shipping Analysis:** Examined shipping-date differences and highlighted source-data quality concerns.

## Key Business Findings

- **Total Sales:** 141,783.63
- **Total Gross Profit:** 93,442.80
- **Total Units Sold:** 38,654
- **Overall Gross Margin:** 65.91%
- **Total Orders:** 8,549
- **Average Order Value:** 16.58

### Important Insights

- Chocolate Division contributes approximately 95.06% of total gross profit.
- The top 5 products contribute approximately 95.06% of total gross profit.
- Kazookles has a low gross margin of approximately 7.69%.
- Lickable Wallpaper has the highest profit per unit at 10.00.
- Shipping date data contains unusually large gaps and requires validation before drawing operational conclusions.

## Dashboard Features

- Interactive KPI cards for key business metrics.
- Division-wise performance analysis.
- Product-wise sales and profit comparison.
- Factory-wise performance analysis.
- Region and state performance insights.
- Cost and gross margin risk reports.
- Profit and revenue concentration analysis.
- Monthly sales and profit trends.
- Units sold analysis.
- Customer performance analysis.
- Shipping duration analysis.
- Interactive filters for division, date range, product search, and gross margin.
- Business recommendations based on analytical findings. 

## How to Run the Project

1. Clone the Repository

After publishing the project on GitHub, clone it using:

git clone <your-github-repository-url>

2. Navigate to the Project Folder

Open the terminal and move to the project directory:

cd Nassau_Candy_Analytics

3. Install Required Libraries

Install the required Python libraries using:

pip install pandas numpy plotly streamlit

4. Run the Streamlit Dashboard

Start the dashboard using the following command:

python -m streamlit run app.py

The dashboard will open in your default web browser.

## Project Structure

Nassau_Candy_Analytics/
│
├── app.py
│
├── data/
│   └── candy_sales.csv
│
└── README.md
## Future Improvements

- Add advanced sales forecasting features.
- Integrate SQL database connectivity.
- Add more interactive visualizations.
- Improve dashboard performance and user experience.
- Include automated report generation.

## Conclusion

This project demonstrates how Python and data analytics tools can be used to analyze business sales and profitability data.

Through product, division, factory, customer, and cost analysis, the project identifies important business trends and opportunities for improvement.

The interactive Streamlit dashboard presents these insights through visualizations, KPI metrics, and filters, helping users make informed, data-driven decisions.