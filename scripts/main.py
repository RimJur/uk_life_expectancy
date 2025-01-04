import polars as pl

schema = {
    "life_expectancy": pl.String,
    "public_health_expenditure_pc_gdp": pl.String,
    "lighting_price": pl.String,
    "average_working_hours": pl.String,
    "daily_caloric_intake": pl.String,
}
df = pl.read_csv("../data/starting.csv", try_parse_dates=True, schema_overrides=schema)
df = df.select(
    pl.col("year"),
    pl.col("life_expectancy").str.replace_all(",", ".").cast(pl.Float64).round(2),
    pl.col("Real GDP (at market prices) (BoE (2017))").alias("gdp"),
    pl.col("Real GDP recent")
    .str.replace_all(",", ".")
    .cast(pl.Float64)
    .round(2)
    .alias("gdp_recent"),
    pl.col("public_health_expenditure_pc_gdp")
    .str.replace_all(",", ".")
    .cast(pl.Float64)
    .round(2)
    .alias("relative_health_expenditure"),
    pl.col("health_expenditure_recent")
    .str.replace_all(",", ".")
    .cast(pl.Float64)
    .round(2)
    .alias("relative_health_expenditure_recent"),
    pl.col("urbanization_rate").str.replace_all(",", ".").cast(pl.Float64).round(2),
    pl.col("daily_caloric_intake").str.replace_all(",", ".").cast(pl.Float64).round(2),
    pl.col("average_working_hours").str.replace_all(",", ".").cast(pl.Float64).round(2),
    pl.col("child_mortality").str.replace_all(",", ".").cast(pl.Float64).round(2),
    pl.col("world_war_1").alias("ww1"),
    pl.col("world_war_2").alias("ww2"),
    pl.col("lighting_price").str.replace_all(",", ".").cast(pl.Float64).round(2),
)
df.write_csv("../data/intermediate.csv")
