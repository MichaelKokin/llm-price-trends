"""
LLM Inference Price Trends Analysis
Reproduces and extends Epoch AI's analysis to March 2026.
Based on: https://epoch.ai/data-insights/llm-inference-price-trends
Code reference: https://github.com/epoch-research/llm-benchmark-efficiency
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
from scipy import stats
from datetime import datetime

# --- Config ---
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Epoch AI color palette (from their plotting.py)
COLORS = [
    "#034752", "#0a7a8a", "#15b2b0", "#6dc4a0",
    "#a4d691", "#d5e77d", "#f9f871", "#e8784a",
    "#c24b6d", "#8b2f8f", "#5533a1", "#2244aa",
    "#1166cc"
]

# Benchmarks config: name -> (column, threshold_description)
BENCHMARKS = {
    "MMLU": {"col": "MMLU", "label": "MMLU (General Knowledge)", "unit": "%"},
    "GPQA Diamond": {"col": "GPQA Diamond", "label": "GPQA Diamond (PhD-level Science)", "unit": "%"},
    "HumanEval": {"col": "HumanEval", "label": "HumanEval (Coding)", "unit": "%"},
    "MATH-500": {"col": "MATH-500", "label": "MATH-500", "unit": "%"},
    "MATH 5": {"col": "MATH 5", "label": "MATH Level 5 (Advanced Math)", "unit": "%"},
    "LMSys Chatbot Arena ELO": {"col": "LMSys Chatbot Arena ELO", "label": "LMSys Chatbot Arena ELO", "unit": "ELO"},
}


def load_data():
    """Load and combine Epoch original data + our updated data."""
    # Load Epoch originals
    aa = pd.read_csv(DATA_DIR / "epoch_original" / "aa_data_with_math5.csv")
    epoch = pd.read_csv(DATA_DIR / "epoch_original" / "epoch_ai_price_data_not_in_aa_with_benchmarks.csv")

    # Standardize columns
    for df in [aa, epoch]:
        df.rename(columns={"USD per 1M Tokens": "price"}, inplace=True)
        df["Release Date"] = pd.to_datetime(df["Release Date"])

    original = pd.concat([aa, epoch], ignore_index=True)

    # Load updated data
    updated = pd.read_csv(DATA_DIR / "updated" / "new_models_raw.csv")
    updated.rename(columns={
        "Weighted Avg Price (USD/1M tokens)": "price",
        "MATH Level 5": "MATH 5",
    }, inplace=True)
    updated["Release Date"] = pd.to_datetime(updated["Release Date"])

    # Combine (drop duplicates by model name, keeping updated version)
    original["source"] = "epoch"
    updated["source"] = "updated_2026"

    combined = pd.concat([original, updated], ignore_index=True)

    # Smart dedup: only remove duplicates where the SAME model appears
    # in both Epoch and updated sources. Keep all Epoch-internal duplicates
    # (they represent intentional price change tracking, e.g. GPT-3 price drops).
    # For cross-source duplicates, prefer updated data.
    epoch_names = set(original["Model Name"].unique())
    updated_names = set(updated["Model Name"].unique())
    overlap_names = epoch_names & updated_names

    if overlap_names:
        # For overlapping models, keep updated version
        mask_drop = (combined["source"] == "epoch") & (combined["Model Name"].isin(overlap_names))
        combined = combined[~mask_drop]

    # Also dedup exact same (model, date, price) rows
    combined = combined.drop_duplicates(
        subset=["Model Name", "Release Date", "price"], keep="last"
    )

    combined = combined.sort_values("Release Date").reset_index(drop=True)

    # Exclude reasoning models (Epoch AI methodology: different token generation patterns)
    reasoning_patterns = ["o1", "o3", "o4", "DeepSeek-R1", "o1-mini", "o1-preview", "o3-mini", "o3-pro"]
    reasoning_mask = combined["Model Name"].apply(
        lambda x: any(x.strip().startswith(p) or x.strip() == p for p in reasoning_patterns)
    )
    n_reasoning = reasoning_mask.sum()
    combined_all = combined.copy()  # Keep for reference
    combined = combined[~reasoning_mask].reset_index(drop=True)

    print(f"Total models: {len(combined)} (excluded {n_reasoning} reasoning models)")
    print(f"  From Epoch: {(combined['source'] == 'epoch').sum()}")
    print(f"  Updated/New: {(combined['source'] == 'updated_2026').sum()}")
    print(f"  Date range: {combined['Release Date'].min()} to {combined['Release Date'].max()}")

    # Debug: show price range for key benchmarks
    for col in ["MMLU", "GPQA Diamond"]:
        valid = combined.dropna(subset=[col, "price"])
        if len(valid) > 0:
            print(f"  {col}: price range ${valid['price'].min():.2f} - ${valid['price'].max():.2f}")
            cheapest = valid.loc[valid["price"].idxmin()]
            most_expensive = valid.loc[valid["price"].idxmax()]
            print(f"    Cheapest: {cheapest['Model Name']} (${cheapest['price']:.2f}, {col}={cheapest[col]:.1f})")
            print(f"    Most expensive: {most_expensive['Model Name']} (${most_expensive['price']:.2f}, {col}={most_expensive[col]:.1f})")

    return combined


def datetime_to_float_year(dt):
    """Convert datetime to decimal year."""
    year_start = datetime(dt.year, 1, 1)
    year_end = datetime(dt.year + 1, 1, 1)
    return dt.year + (dt - year_start).total_seconds() / (year_end - year_start).total_seconds()


def compute_frontier_and_regression(df, benchmark_col, price_col="price"):
    """
    Epoch AI methodology: for a given benchmark, define multiple performance
    thresholds. For each threshold, track the cheapest model over time that
    achieves at least that score. This creates a set of (date, price) points
    showing how the cost to achieve each quality level drops over time.
    Fit log-linear regression through all these points.

    Returns: frontier_points DataFrame, slope, intercept, rate_per_year
    """
    subset = df.dropna(subset=[benchmark_col, price_col]).copy()
    subset = subset[subset[benchmark_col] > 0]
    subset = subset.sort_values("Release Date")

    if len(subset) < 4:
        return None, None, None, None

    # Define thresholds: use the score of each model that set a new record
    scores_sorted = subset.sort_values("Release Date")
    thresholds = []
    running_max = -np.inf
    for _, row in scores_sorted.iterrows():
        if row[benchmark_col] > running_max:
            running_max = row[benchmark_col]
            thresholds.append(running_max)

    # For each threshold, find the cheapest model at each point in time
    frontier_points = []
    for threshold in thresholds:
        above = subset[subset[benchmark_col] >= threshold].sort_values("Release Date")
        if len(above) == 0:
            continue

        # Track the cheapest model available at each new release date
        running_min_price = np.inf
        for _, row in above.iterrows():
            if row[price_col] <= running_min_price:
                running_min_price = row[price_col]
                frontier_points.append({
                    "Model Name": row["Model Name"],
                    "Release Date": row["Release Date"],
                    "price": row[price_col],
                    "score": row[benchmark_col],
                    "threshold": threshold,
                    "benchmark": benchmark_col,
                })

    if len(frontier_points) < 4:
        return None, None, None, None

    frontier_df = pd.DataFrame(frontier_points)
    # Deduplicate (same model can appear for multiple thresholds)
    frontier_df = frontier_df.drop_duplicates(subset=["Model Name", "Release Date", "price"])

    # Log-linear regression: log(price) = slope * year + intercept
    years = frontier_df["Release Date"].apply(
        lambda x: datetime_to_float_year(x.to_pydatetime())
    ).values
    log_prices = np.log10(frontier_df["price"].values)

    if len(years) < 2:
        return frontier_df, None, None, None

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, log_prices)

    # Rate: 10^(-slope) is how many times cheaper per year
    rate_per_year = 10 ** (-slope)

    return frontier_df, slope, intercept, rate_per_year


def create_benchmark_chart(df, benchmark_name, config, show_regression=True):
    """Create a single benchmark price trend chart."""
    col = config["col"]
    label = config["label"]

    subset = df.dropna(subset=[col, "price"]).copy()
    subset = subset[subset[col] > 0]
    subset = subset.sort_values("Release Date")

    if len(subset) < 3:
        print(f"  Skipping {benchmark_name}: only {len(subset)} data points")
        return None, None

    fig = go.Figure()

    # Color by source
    colors_map = {"epoch": "#0a7a8a", "updated_2026": "#e8784a"}

    for source, color in colors_map.items():
        mask = subset["source"] == source
        if mask.any():
            src_data = subset[mask]
            fig.add_trace(go.Scatter(
                x=src_data["Release Date"],
                y=src_data["price"],
                mode="markers+text",
                marker=dict(size=8, color=color, line=dict(width=1, color="white")),
                text=src_data["Model Name"],
                textposition="top center",
                textfont=dict(size=7),
                name="Epoch data" if source == "epoch" else "Updated (2025-2026)",
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    f"{label}: %{{customdata[0]:.1f}}<br>"
                    "Price: $%{y:.2f}/1M tokens<br>"
                    "Date: %{x}<extra></extra>"
                ),
                customdata=src_data[[col]].values,
            ))

    # Regression
    frontier_df, slope, intercept, rate = compute_frontier_and_regression(df, col)

    if slope is not None and show_regression:
        # Generate regression line
        date_range = pd.date_range(
            df["Release Date"].min() - pd.Timedelta(days=60),
            pd.Timestamp("2026-06-01"),
            periods=100
        )
        years = [datetime_to_float_year(d.to_pydatetime()) for d in date_range]
        predicted_log_price = [slope * y + intercept for y in years]
        predicted_price = [10**p for p in predicted_log_price]

        fig.add_trace(go.Scatter(
            x=date_range,
            y=predicted_price,
            mode="lines",
            line=dict(dash="dash", color="#c24b6d", width=2),
            name=f"Trend: {rate:.0f}x cheaper/year",
            hoverinfo="skip",
        ))

    # Layout
    fig.update_layout(
        title=dict(
            text=f"<b>LLM Inference Price Trends — {label}</b><br>"
                 f"<span style='font-size:12px;color:gray;'>"
                 f"{'Price drops ~' + str(round(rate)) + 'x per year' if rate else 'Insufficient data for trend'}"
                 f"</span>",
            font=dict(family="Georgia, serif", size=16),
        ),
        xaxis=dict(
            title="Release Date",
            gridcolor="#eee",
        ),
        yaxis=dict(
            title="Price (USD per 1M tokens)",
            type="log",
            gridcolor="#eee",
        ),
        plot_bgcolor="white",
        legend=dict(
            x=0.02, y=0.98,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#ccc", borderwidth=1,
        ),
        width=1000,
        height=600,
        margin=dict(l=80, r=40, t=100, b=60),
    )

    return fig, rate


def create_combined_chart(df, results):
    """Create combined overview chart showing all benchmark trends."""
    fig = go.Figure()

    for i, (bench_name, info) in enumerate(results.items()):
        rate = info["rate"]
        if rate is None:
            continue
        slope = info["slope"]
        intercept = info["intercept"]

        date_range = pd.date_range("2021-06-01", "2026-06-01", periods=100)
        years = [datetime_to_float_year(d.to_pydatetime()) for d in date_range]
        predicted_price = [10 ** (slope * y + intercept) for y in years]

        color = COLORS[i % len(COLORS)]
        fig.add_trace(go.Scatter(
            x=date_range,
            y=predicted_price,
            mode="lines",
            line=dict(color=color, width=3),
            name=f"{bench_name} ({rate:.0f}x/yr)",
        ))

    fig.update_layout(
        title=dict(
            text="<b>LLM Inference Price Trends — All Benchmarks</b><br>"
                 "<span style='font-size:12px;color:gray;'>"
                 "Log-linear regression lines by benchmark (updated to March 2026)</span>",
            font=dict(family="Georgia, serif", size=16),
        ),
        xaxis=dict(title="Date", gridcolor="#eee"),
        yaxis=dict(title="Price (USD per 1M tokens)", type="log", gridcolor="#eee"),
        plot_bgcolor="white",
        legend=dict(x=0.02, y=0.02, yanchor="bottom",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#ccc", borderwidth=1),
        width=1000, height=600,
        margin=dict(l=80, r=40, t=100, b=60),
    )

    return fig


def main():
    print("=" * 60)
    print("LLM Inference Price Trends Analysis")
    print("Updated to March 2026")
    print("=" * 60)

    # Load data
    df = load_data()

    # Save combined dataset
    combined_path = DATA_DIR / "combined.csv"
    df.to_csv(combined_path, index=False)
    print(f"\nSaved combined dataset to {combined_path}")

    # Analyze each benchmark
    results = {}
    print("\n--- Benchmark Analysis ---")
    for bench_name, config in BENCHMARKS.items():
        col = config["col"]
        n_points = df[col].notna().sum()

        frontier_df, slope, intercept, rate = compute_frontier_and_regression(df, col)

        results[bench_name] = {
            "rate": rate,
            "slope": slope,
            "intercept": intercept,
            "n_points": n_points,
        }

        if rate:
            print(f"  {bench_name}: {rate:.1f}x cheaper/year ({n_points} data points)")
        else:
            print(f"  {bench_name}: insufficient data ({n_points} points)")

    # Generate individual charts
    print("\n--- Generating Charts ---")
    for bench_name, config in BENCHMARKS.items():
        fig, rate = create_benchmark_chart(df, bench_name, config)
        if fig:
            filename = bench_name.lower().replace(" ", "_").replace("-", "_")
            fig.write_html(str(OUTPUT_DIR / f"{filename}.html"))
            fig.write_image(str(OUTPUT_DIR / f"{filename}.png"), scale=2)
            print(f"  Saved: {filename}.html + .png")

    # Generate combined chart
    combined_fig = create_combined_chart(df, results)
    combined_fig.write_html(str(OUTPUT_DIR / "combined_all_benchmarks.html"))
    combined_fig.write_image(str(OUTPUT_DIR / "combined_all_benchmarks.png"), scale=2)
    print(f"  Saved: combined_all_benchmarks.html + .png")

    # Summary
    print("\n--- Summary ---")
    rates = [v["rate"] for v in results.values() if v["rate"] is not None]
    if rates:
        print(f"  Median price decline: {np.median(rates):.0f}x per year")
        print(f"  Range: {min(rates):.0f}x to {max(rates):.0f}x per year")

    print(f"\nAll outputs saved to: {OUTPUT_DIR}")
    print("Done!")


if __name__ == "__main__":
    main()
