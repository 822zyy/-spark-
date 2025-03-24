from django.db import models


# Create your models here.
class User(models.Model):
    id = models.AutoField("id", primary_key=True)
    username = models.CharField("username", max_length=255, default='')
    password = models.CharField("password", max_length=255, default='')
    createTime = models.DateField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "user"


class History(models.Model):
    id = models.AutoField("id", primary_key=True)
    jobId = models.CharField("职位ID", max_length=255, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField("收藏次数", default=1)

    class Meta:
        db_table = "history"


class JobData(models.Model):
    id = models.AutoField("id", primary_key=True)
    type = models.CharField("职位类型", max_length=255)
    city = models.CharField("城市", max_length=255)
    title = models.CharField("职位名称", max_length=255)
    company = models.CharField("公司名称", max_length=255)
    minsalary = models.IntegerField("最低薪资")
    maxsalary = models.IntegerField("最高薪资")
    work_experience = models.CharField("工作经验", max_length=255)
    education = models.CharField("学历要求", max_length=255)
    com_tag = models.TextField("公司标签")
    com_People = models.CharField("公司规模", max_length=255)
    workTag = models.TextField("工作标签")
    welfare = models.TextField("员工福利")
    imgSrc = models.TextField("公司Logo")

    class Meta:
        db_table = "jobdata"
        managed = False  # 不管增删


class RecomData(models.Model):
    id = models.AutoField("id", primary_key=True)
    title = models.CharField("职位", max_length=255)
    address = models.CharField("工作地址", max_length=255)
    post_time = models.CharField("发布时间", max_length=255)
    work_experience = models.CharField("工作经验", max_length=255)
    education = models.CharField("学历", max_length=255)
    salary = models.CharField("薪资范围", max_length=255)
    company = models.CharField("公司", max_length=255)
    workTag = models.TextField("工作标签")
    welfare = models.TextField("工作福利")
    work_content = models.TextField("职位描述")

    class Meta:
        db_table = "recomdata"
        managed = False


class Favorite(models.Model):
    id = models.AutoField("id", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    job = models.ForeignKey(RecomData, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "favorite"
        unique_together = ('user', 'job')


class cityData(models.Model):
    # 城市选择
    CITY_CHOICES = [
        ('beijing', '北京'),
        ('shanghai', '上海'),
        ('guangzhou', '广州'),
        ('shenzhen', '深圳'),
        ('hangzhou', '杭州'),
        ('chengdu', '成都'),
    ]

    # 编程语言选择
    LANGUAGE_CHOICES = [
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('python', 'Python'),
        ('php', 'PHP'),
    ]

    city = models.CharField(
        max_length=20,
        choices=CITY_CHOICES,
        verbose_name='城市'
    )

    programming_language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        verbose_name='编程语言'
    )

    job_count = models.IntegerField(
        default=0,
        verbose_name='招聘数量'
    )


    class Meta:
        db_table = 'cityData'
        unique_together = ('city', 'programming_language')
