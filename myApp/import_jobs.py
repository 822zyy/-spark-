# import os
# import django
# import pandas as pd
#
# # 设置 Django 环境
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
# django.setup()
#
# # 导入必要的模型
# from myApp.models import JobData
#
#
# def import_data():
#     csv_file_path = r'D:\djangoProject\基于spark的求职智能分析系统\spark\jobData.csv'
#
#     try:
#         # 读取CSV文件
#         df = pd.read_csv(csv_file_path)
#
#         # 逐行创建数据
#         for index, row in df.iterrows():
#             JobData.objects.create(
#                 type=row['type'],
#                 city=row['city'],
#                 title=row['title'],
#                 company=row['company'],
#                 minsalary=row['minsalary'],
#                 maxsalary=row['maxsalary'],
#                 work_experience=row['work_experience'],
#                 education=row['education'],
#                 com_tag=row['com_tag'],
#                 com_People=row['com_People'],
#                 workTag=row['workTag'],
#                 welfare=row['welfare'],
#                 imgSrc=row['imgSrc']
#             )
#             print(f"已导入第 {index + 1} 条数据")
#
#         print('成功导入所有职位数据')
#
#     except Exception as e:
#         print(f'导入失败: {str(e)}')
#
#
# if __name__ == "__main__":
#     import_data()