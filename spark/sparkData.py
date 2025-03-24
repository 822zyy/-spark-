# from pyspark.sql import SparkSession
# from pyspark.sql.functions import monotonically_increasing_id
# from pyspark.sql.types import StructType,StructField,IntegerType,StringType,FloatType
# #
# import os
# os.environ['JAVA_HOME'] = "C:\Program Files\Java\jdk1.8.0_231"
#
# if __name__ == '__main__':
#     spark = SparkSession.builder.appName("sparkSQL").master("local[*]").\
#         config("spark.sql.shuffle.partitions", 2).\
#         config("spark.sql.warehouse.dir", "hdfs://hadoop01:9000/root/hive/warehouse/").\
#         config("spark.hadoop.hive.metastore.uris", "thrift://hadoop03:9083").\
#         enableHiveSupport().\
#         getOrCreate()
#
#     sc = spark.sparkContext
# #数据表框架
#     schema = StructType().add("type",StringType,nullable=True). \
#         add("type",StringType(),nullable=True). \
#         add("city",StringType(),nullable=True). \
#         add("title",StringType(),nullable=True). \
#         add("company",StringType(),nullable=True). \
#         add("minsalary",IntegerType(),nullable=True). \
#         add("maxsalary",IntegerType(),nullable=True). \
#         add("work_experience",StringType(),nullable=True). \
#         add("education",StringType(),nullable=True). \
#         add("com_tag",StringType(),nullable=True). \
#         add("com_People",StringType(),nullable=True). \
#         add("workTag",StringType(),nullable=True). \
#         add("welfare",StringType(),nullable=True). \
#         add("imgSrc",StringType(),nullable=True)
#
#     df = spark.read.format("csv").\
#         option("sep",",").\
#         option("quote",'"').\
#         option("escape",'"').\
#         option("header",True).\
#         option("encoding","utf-8").\
#         schema(schema=schema).\
#         load("./jobData.csv")
#     #数据清洗
#     df.drop_duplicates()
#
#     df = df.withColumn("id",monotonically_increasing_id())
#
#     df.show()
#
#     #sql
#     df.write.mode("overwriter").\
#         format("jdbc").\
#         option("url","jdbc:mysql://192.168.5.123:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8"). \
#         option("dbtable","jobData"). \
#         option("user","root"). \
#         option("password","12345678"). \
#         option("encoding","utf-8").\
#         save()
#
#     df.write.mode("overwriter").saveAsTable("jobData","parquet")
#     spark.sql("select * from jobData").show()
#
#
#
#
#
