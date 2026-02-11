import plotly.express as px
import plotly.data as pldata
import pandas as pd



def main() -> None:
    df = pldata.wind(return_type="pandas")

    print("FIRST 10 ROWS")
    print(df.head(10))
    print("\nLast 10 ROWS")
    print(df.tail(10))


    strength_clean = (
        df["strength"].astype(str).str.replace(r"[^\d\.\-]", "", regex=True)
    )
    parts = strength_clean.str.split("-",n=1,expand=True)

    low= pd.to_numeric(parts[0],errors="coerce")
    high = pd.to_numeric(parts[1],errors="coerce")

    df["strength_float"] = (low + high) /2
    df.loc[high.isna(), "strength_float"] = low

    df = df.dropna(subset=["strength_float", "frequency", "direction"])

    fig = px.scatter(
        df,
        x="strength_float",
        y="frequency",
        color="direction",
        title="Wind Dataset: Strength vs Frequency (colored by direction)",
        labels={
            "strength_float": "Strength (midpoint of bin)",
            "frequency": "Frequency",
            "direction": "Direction",
        },
        hover_data = ["strength"],
    )

    out_file = "wind.html"
    fig.write_html(out_file, include_plotlyjs="cdn")
    print(f"\nSaved interactive plot to: {out_file}")

    with open(out_file, "r", encoding="UTF-8") as f:
        html = f.read()

    if "plotly" in html.lower():
        print("Verified: wind.html appears to contain Plotly output.")
    else:
        print("Warning: wind.html does not look like Plotly HTML file.")



if __name__ =="__main__":
    main()