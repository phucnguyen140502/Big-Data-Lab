# -*- coding: utf-8 -*-
"""lab 4 Nguyễn đức Nguyên Phúc SQL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14WPzoGhM_BJJKUo0UxpbtJTr5qvoZdqx
"""

from google.colab import drive
drive.mount('/content/drive')

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("PySpark_Exercises").getOrCreate()

spark_sql = spark.read.csv("/content/drive/My Drive/mtcars.csv", header=True, inferSchema=True)
spark_sql.show(5)

spark_sql.printSchema()

spark_sql.select("mpg").show()

spark_sql.filter(spark_sql.mpg < 18).show()

from pyspark.sql.functions import col

spark_sql = spark_sql.withColumn("wtTon", col("wt")*0.45)
spark_sql.select("wt","wtTon").show(5)

spark_sql = spark_sql.withColumnRenamed("vs", "versus")
spark_sql.show(5)

data1 = [("A101", "John"), ("A102", "Peter"), ("A103", "Charlie")]
columns1 = ["emp_id", "emp_name"]
df1 = spark.createDataFrame(data1, columns1)

df1.show()

data2 = [("A101", 1000), ("A102", 2000), ("A103", 3000)]
columns2 = ["emp_id", "salary"]
df2 = spark.createDataFrame(data2, columns2)

df2.show()

combined_df = df1.join(df2, on="emp_id", how="inner")
combined_df.show()

data3 = [("A101", 1000), ("A102", 2000), ("A103", None)]
columns3 = ["emp_id", "salary"]
df3 = spark.createDataFrame(data3, columns3)

df3.show()

df3 = df3.fillna({"salary": 3000})

df3.show()

spark_sql.groupBy("cyl").agg({"wt": "mean"}).orderBy("cyl").show()

spark_sql.createOrReplaceTempView("cars")

spark.sql("SELECT * FROM cars").show()

spark.sql("SELECT * FROM cars").show()

spark.sql("SELECT DISTINCT(mpg) FROM cars").show()

spark.sql("SELECT * FROM cars WHERE mpg > 20 and cyl < 6").show()

spark.sql("""SELECT cyl, avg(wt) as avg_weight
          FROM cars
          group by cyl""").show()

from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType

def convert_weight(wt):
  return wt*0.45

convert_weight_udf = udf(convert_weight, FloatType())
spark.udf.register("convert_weight", convert_weight_udf)

spark.sql("SELECT wt, convert_weight(wt) as wtTon FROM cars").show()

