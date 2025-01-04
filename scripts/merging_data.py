import polars as pl

df = pl.read_csv("../data/intermediate.csv")


# Average multiplier is the average rate between
# changes in main and additional columns
def calculate_average_multipliear(
    df: pl.DataFrame, main_col: str, additional_col: str
) -> float:
    # Select rows that overlap
    df = df.filter(~pl.col(main_col).is_null() & ~pl.col(additional_col).is_null())

    # Calculate the change
    df = df.with_columns(
        change=(
            ((pl.col(main_col) - pl.col(main_col).shift(1)) / pl.col(main_col).shift(1))
            * 100
        ),
        recent_change=(
            (
                (pl.col(additional_col) - pl.col(additional_col).shift(1))
                / pl.col(additional_col).shift(1)
            )
            * 100
        ),
    )
    df = df.with_columns(
        multiplier=(
            pl.when(pl.col("recent_change") == 0)
            .then(1)
            .otherwise(pl.col("change") / pl.col("recent_change"))
        )
    )

    # Calculate average multiplier value
    average_multiplier = df.select(pl.col("multiplier").mean()).item()
    return average_multiplier


# Calculates the value based on the previous value and change
# of additionnal columns values
def merge_columns(
    df: pl.DataFrame, main_col: str, additional_col: str, multiplier: float
) -> pl.DataFrame:
    for n in range(10):
        if main_col == "gdp":
            df = df.with_columns(
                pl.when(
                    pl.col(main_col).is_null()
                    & pl.col(main_col).shift(1).is_not_null()
                    & pl.col(additional_col).is_not_null()
                    & pl.col(additional_col).shift(1).is_not_null()
                )
                .then(
                    pl.col(main_col).shift(1)
                    * (
                        (
                            (pl.col(additional_col) - pl.col(additional_col).shift(1))
                            / pl.col(additional_col).shift(1)
                        )
                        * multiplier
                        + 1
                    )
                )
                .otherwise(pl.col(main_col))
                .alias(main_col)
            )
        elif main_col == "relative_health_expenditure":
            df = df.with_columns(
                pl.when(
                    pl.col(main_col).is_null()
                    & pl.col("year").is_in([2022, 2023])
                    & pl.col(main_col).shift(1).is_not_null()
                    & pl.col(additional_col).is_not_null()
                    & pl.col(additional_col).shift(1).is_not_null()
                )
                .then(
                    pl.col(main_col).shift(1)
                    * (
                        (
                            (pl.col(additional_col) - pl.col(additional_col).shift(1))
                            / pl.col(additional_col).shift(1)
                        )
                        * multiplier
                        + 1
                    )
                )
                .otherwise(pl.col(main_col))
                .alias(main_col)
            )

    return df


df = df.with_columns(
    pl.col("gdp_recent").cast(pl.Int64).alias("gdp_recent"),
    pl.col("relative_health_expenditure_recent")
    .cast(pl.Float64)
    .alias("relative_health_expenditure_recent"),
)

df = merge_columns(
    df, "gdp", "gdp_recent", calculate_average_multipliear(df, "gdp", "gdp_recent")
)
df = merge_columns(
    df,
    "relative_health_expenditure",
    "relative_health_expenditure_recent",
    calculate_average_multipliear(
        df, "relative_health_expenditure", "relative_health_expenditure_recent"
    ),
)

df = df.with_columns(
    pl.col("gdp").cast(pl.Int64).alias("gdp"),
    pl.col("relative_health_expenditure").round(2).alias("relative_health_expenditure"),
)
df = df.drop(["gdp_recent", "relative_health_expenditure_recent"])
# df.tail(8).select(
#     pl.col("year"),
#     pl.col("gdp"),
#     pl.col("relative_health_expenditure"),
# )
df.write_csv("../data/semi_final.csv")

# df.count()
# d
