# -*- coding: utf-8 -*-
"""Lab 8 Nguyễn đức Nguyên Phúc Bigdata.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nN8vOTz_57LTKPwY0H8ReJLF_UIrEt6q
"""

from google.colab import drive
drive.mount('/content/drive')

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('daily_weather').getOrCreate()

daily_weather_df = spark.read.csv('/content/drive/MyDrive/daily_weather.csv', header=True, inferSchema=True)

daily_weather_df.show()

daily_weather_df.printSchema()

daily_weather_df.describe().show()

daily_weather_df.corr("rain_accumulation_9am", "rain_duration_9am")

daily_weather_df_without_null = daily_weather_df.na.drop()

daily_weather_df_without_null.count()

daily_weather_df_without_null.describe("air_temp_9am").show()

daily_weather_df.columns

mean_values = {col_name: daily_weather_df.agg({col_name: "mean"}).collect()[0][0] for col_name in daily_weather_df.columns}

print(mean_values)

for col_name, mean_value in mean_values.items():
  daily_weather_df_replace_mean = daily_weather_df.na.fill(mean_value, [col_name])

daily_weather_df_replace_mean.show()

daily_weather_df_replace_mean.count()

daily_weather_df_replace_mean.describe().show()

daily_weather_df_replace_mean.summary().show()

daily_weather_df_classification = daily_weather_df.na.drop()

daily_weather_df_classification = daily_weather_df_classification.drop("number")

daily_weather_df_classification.show()

from pyspark.sql.functions import when, col

# Create a new categorical column: 1 if Humidity < 30, else 0
daily_weather_df_classification = daily_weather_df_classification.withColumn("low_humidity", when(col("relative_humidity_3pm") < 30, 1).otherwise(0))

# Show updated DataFrame
daily_weather_df_classification.select("low_humidity", "relative_humidity_3pm").show(10)

train_df, test_df = daily_weather_df_classification.randomSplit([0.8, 0.2], seed=42)

train_df.count()

test_df.count()

from pyspark.ml.feature import VectorAssembler

feature_cols = ["air_pressure_9am", "air_temp_9am", "avg_wind_speed_9am",
                "max_wind_speed_9am", "rain_accumulation_9am", "relative_humidity_9am"]

assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

# Biến đổi dữ liệu
train_df = assembler.transform(train_df)
test_df = assembler.transform(test_df)

# Chỉ giữ lại cột cần thiết
train_df = train_df.select("features", "low_humidity")
test_df = test_df.select("features", "low_humidity")

from pyspark.ml.classification import DecisionTreeClassifier

# Tạo mô hình Decision Tree
dt = DecisionTreeClassifier(labelCol="low_humidity", featuresCol="features")

# Huấn luyện mô hình
dt_model = dt.fit(train_df)

predictions = dt_model.transform(test_df)

# Hiển thị 10 dòng đầu tiên
predictions.select("features", "low_humidity", "prediction").show(10)

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(labelCol="low_humidity", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print(f"Độ chính xác của mô hình: {accuracy:.2f}")

from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Define a UDF to convert the vector to a string representation
vector_to_string = udf(lambda v: str(v), StringType())

# Apply the UDF to the 'features' column
predictions = predictions.withColumn("features_str", vector_to_string("features"))

# Select the desired columns, including the new string representation
predictions.select("features_str", "low_humidity", "prediction").write.csv("predictions.csv", header=True)





