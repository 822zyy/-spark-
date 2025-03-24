# import os
# import sys
#
# # 设置环境变量
# os.environ['PYSPARK_PYTHON'] = sys.executable
# os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
#
# from pyspark.sql import SparkSession
#
# # 创建 SparkSession，连接到远程 Spark 集群
# spark = SparkSession.builder \
#     .appName("Remote Spark Test") \
#     .config("spark.driver.host", "root") \
#     .config("spark.driver.bindAddress", "127.0.0.1") \
#     .master("spark://192.168.5.123:7077") \
# .getOrCreate()
#
# try:
#     # 创建测试数据
#     test_data = [
#         ("Python", 100000),
#         ("Java", 20000),
#         ("Scala", 3000),
#         ("R", 2000)
#     ]
#     columns = ["language", "users"]
#
#     # 创建 DataFrame
#     df = spark.createDataFrame(test_data, schema=columns)
#
#     # 显示数据
#     print("原始数据:")
#     df.show()
#
#     # 执行一些转换操作
#     print("\n用户数大于 5000 的语言:")
#     df.filter(df.users > 5000).show()
#
#     print("\n按用户数排序:")
#     df.orderBy("users", ascending=False).show()
#
# except Exception as e:
#     print(f"错误类型: {type(e).__name__}")
#     print(f"错误详情: {str(e)}")
#     import traceback
#
#     print("堆栈跟踪:")
#     print(traceback.format_exc())
#
# finally:
#     if 'spark' in locals():
#         spark.stop()