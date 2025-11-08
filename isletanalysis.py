import pandas as pd
import matplotlib.pyplot as plt

# Permanently changes the pandas settings
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

# Read the excel file
df = pd.read_excel(
    "/Users/jonathan/Documents/PYTHON/islets/islets_summery_tidy.xlsx",
    sheet_name="counts",
)
run_meta = pd.read_excel(
    "/Users/jonathan/Documents/PYTHON/islets/islets_summery_tidy.xlsx",
    sheet_name="run_meta",
)

# Reshape data and explore
counts_wide = df.pivot_table(
    index=["Run", "flush"], columns="status", values="value", aggfunc="sum"
).reset_index()

# Calculate proportion alive
counts_wide["proportion_alive"] = counts_wide["alive"] / (
    counts_wide["alive"] + counts_wide["dead"]
)

# Add proportion passaged
counts_wide["tot_passaged"] = counts_wide["alive"] + counts_wide["dead"]

# Merge the dataframes
merged = pd.merge(counts_wide, run_meta, on="Run")

merged = merged.sort_values(["Run", "flush"])

# print(merged.groupby("Run")["tot_passaged"].cumsum().shift(fill_value=0).head(100))
# print(merged.groupby("Run")["tot_passaged"].cumsum().head(100))
# print(merged.groupby("Run")["tot_passaged"].head(100))

merged["cumalative_injected"] = merged.groupby("Run")["tot_passaged"].cumsum()
merged["proportion passaged"] = merged["cumalative_injected"] / merged["Cells injected"]

# print(merged.head(100))

df = merged.copy()

# Make sure flush is numeric and sorted
df = df.sort_values(["Run", "flush"])
df["flush"] = df["flush"].astype(int)

# plot
fig, ax = plt.subplots()

for run, d in df.groupby("Run"):
    ax.plot(
        d["flush"],
        d["proportion passaged"],
        marker="o",
        label=f"Condition {run}",
        linewidth=5,
    )

ax.set_xlabel("Flush")
ax.set_ylabel("Proportion passaged")
ax.legend()
ax.grid(visible=True)
plt.show()
