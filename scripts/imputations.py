import polars as pl
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

df = pl.read_csv("../data/semi_final.csv")

imputer = IterativeImputer(max_iter=1000, min_value=0, n_nearest_features=20)
imputer.fit(df)

data = imputer.transform(df)

imputed_df = pl.DataFrame(data, schema=df.columns)
imputed_df = imputed_df.select(
    pl.col("year").cast(pl.Int64),
    pl.col("life_expectancy"),
    pl.col("gdp").cast(pl.Int64),
    pl.col("relative_health_expenditure").round(2),
    pl.col("urbanization_rate").round(2),
    pl.col("daily_caloric_intake").round(2),
    pl.col("average_working_hours").round(2),
    pl.col("child_mortality").round(2),
    pl.col("ww1").cast(pl.Int64),
    pl.col("ww2").cast(pl.Int64),
    pl.col("lighting_price").round(2),
)
# imputed_df.select(
#     pl.col("relative_health_expenditure"),
#     pl.col("average_working_hours"),
#     pl.col("lighting_price"),
# )
imputed_df.write_csv("../data/final.csv")
