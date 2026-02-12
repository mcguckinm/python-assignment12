from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

SQL = """
SELECT
    o.order_id,
    SUM(p.price * l.quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id;
"""

def main() -> None:
    base_dir = Path(__file__).resolve().parent
    db_path = base_dir.parent /"db" / "lesson.db"

    conn = sqlite3.connect(db_path)

    try:
        df = pd.read_sql_query(SQL,conn)
        print(df.columns)
    finally:
        conn.close()

    def cumulative(row):
        totals_above = df["total_price"][0 :row.name+1]
        return totals_above.sum()
    
    df["cumulative"] = df.apply(cumulative, axis=1)


    ax = df.plot(
        kind="line",
        x="order_id",
        y="cumulative",
        title="Cumulative Revenue by Order",
        xlabel="Order ID",
        ylabel="Cumulative Revenue ($)",
        legend=False
    )
    ax.get_yaxis().set_major_formatter( plt.FuncFormatter(lambda x, pos: f"${x:,.0f}")
                                       )
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()