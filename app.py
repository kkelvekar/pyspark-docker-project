from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

def main():
    """Main function to run the Spark job."""

    # Initialize Spark Session
    # In a local Docker setup, you always define the master as 'local[*]'
    # to use all available cores in the container.
    spark = SparkSession.builder \
        .appName("DockerPySparkTest") \
        .master("local[*]") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("WARN")

    print("✅ Spark Session created successfully.")

    # Create a sample DataFrame
    data = [("Alice", "Sales", 30),
            ("Bob", "Engineering", 35),
            ("Charlie", "Sales", 28)]
    columns = ["name", "department", "age"]
    df = spark.createDataFrame(data, columns)

    print("--- Original DataFrame ---")
    df.show()

    # Perform a simple transformation: make the department name uppercase
    transformed_df = df.withColumn("department_upper", upper(col("department")))

    print("--- Transformed DataFrame ---")
    transformed_df.show()

    # Stop the Spark session
    spark.stop()
    print("✅ Spark Session stopped.")

if __name__ == "__main__":
    main()