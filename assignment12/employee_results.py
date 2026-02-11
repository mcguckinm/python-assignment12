import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

SQL = """
SELECT last_name, SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""

def main() -> None:

    db_path = "../db/lesson.db"

    conn = sqlite3.connect(db_path)

    try:
        employee_results = pd.read_sql_query(SQL, conn)
    finally:
        conn.close()

    employee_results = employee_results.sort_values("revenue", ascending=False)

    ax = employee_results.plot(
        kind="bar",
        x="last_name",
        y="revenue",
        legend=False,
        title="Revenue by Employee",
        xlabel="Revenue ($)",
        color="skyblue",
    )

    ax.tick_params(axis="x",rotation=45)
    ax.get_yaxis().set_major_formatter(lambda x, pos: f"${x:,.0f}")

    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    main()
