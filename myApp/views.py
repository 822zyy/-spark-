from random import random
from django.shortcuts import render, redirect
from myApp.models import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User, JobData, RecomData
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Favorite
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, Value, IntegerField
from .utils import extract_city
from django.db.models.functions import Lower

# Create your views here.
from utils.getChartData import changePwd


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {})


def registry(request):
    if request.method == 'GET':
        return render(request, 'auth-register.html', {})
    else:
        uname = request.POST.get('username')
        password = request.POST.get('password')
        ckpassword = request.POST.get('ckpassword')
        # print(uname,password,ckpassword)
        try:
            User.objects.get(username=uname)
            message = '用户名已注册！请选择登录'
        except:
            if not uname or not password or not ckpassword:
                message = '注册信息不能为空'
                messages.error(request, message)
                return HttpResponseRedirect('/myApp/registry/')
            elif password != ckpassword:
                message = '两次密码不一致，请重新输入'
                messages.error(request, message)
                return HttpResponseRedirect('/myApp/registry/')
            else:
                User.objects.create(username=uname, password=password)
                messages.success(request, '注册成功！')
                return HttpResponseRedirect('/myApp/login/')
        return render(request, 'auth-register.html', {})


def login(request):
    if request.method == 'GET':
        return render(request, 'auth-login.html', {})
    else:
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        try:
            user = User.objects.get(username=uname, password=pwd)
            request.session['username'] = uname
            return redirect('/myApp/home/')
        except:
            messages.error(request, '请正确输入用户名和密码')
            return HttpResponseRedirect('/myApp/login/')
        return render(request, 'auth-login.html', {})


def logOut(request):
    request.session.clear()
    return redirect('login')


def salaryChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        return render(request, 'index.html', {
            'userInfo': userInfo
        })


def educationChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        return render(request, 'educationChar.html', {
            'userInfo': userInfo
        })


def cityChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)

        data = cityData.objects.all()
        city_names = data.values_list('city', flat=True).distinct()
        languages = ['Java', 'C++', 'Python', 'PHP']

        city_data = {city: {language: 0 for language in languages} for city in city_names}
        for entry in data:
            city_data[entry.city][entry.programming_language] = entry.job_count

        return render(request, 'cityChar.html', {
            'userInfo': userInfo,
            'city_data': city_data
        })


# def cityChar(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#         return render(request, 'cityChar.html', {
#             'userInfo': userInfo
#         })


# def dataChar(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#         tableData = list(getjobData())
#         # type = request.session.get('type')
#         # jobInfo = JobData.objects.get(type=type)
#         return render(request, 'dataChar.html', {
#             'userInfo': userInfo
#             'tableData':tableData
#         })

def getjobData():
    try:
        jobs = JobData.objects.all().values(
            'imgSrc', 'company', 'title', 'city',
            'minsalary', 'maxsalary', 'work_experience',
            'education', 'com_tag', 'com_People',
            'workTag', 'welfare'
        )
        return jobs
    except Exception as e:
        print(f"获取数据出错: {str(e)}")
        return []


def dataChar(request):
    if request.method == 'GET':
        try:
            uname = request.session.get('username', '822zyy')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            userInfo = User.objects.get(username=uname)
            tableData = list(getjobData())

            return render(request, 'dataChar.html', {
                'userInfo': userInfo,
                'tableData': tableData,
                'current_time': current_time
            })
        except Exception as e:
            print(f"视图处理出错: {str(e)}")
            return render(request, 'dataChar.html', {
                'error': '获取数据失败'
            })


def Usercenter(request):
    uname = request.session.get('username')
    userInfo = User.objects.get(username=uname)
    if request.method == 'POST':
        res = changePwd(userInfo, request.POST)
        if res != None:
            messages.error(request, res)
            return HttpResponseRedirect('/myApp/Usercenter/')
        userInfo = User.objects.get(username=uname)
        messages.success(request, '修改成功')
    return render(request, 'Usercenter.html', {
        'userInfo': userInfo
    })


# def likedata(request):
#     if request.method == 'GET':
#         uname = request.session.get('username')
#         userInfo = User.objects.get(username=uname)
#         return render(request, 'educationChar.html', {
#             'userInfo': userInfo
#         })


def cloudeChar(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        return render(request, 'clouderChar.html', {
            'userInfo': userInfo
        })


def getRecomData(search_query=None, default_city="武汉"):
    try:
        # 基础查询
        query = RecomData.objects.all()

        # 如果有搜索关键词，添加搜索条件
        if search_query:
            search_query = search_query.lower()
            query = query.filter(
                Q(title__icontains=search_query) |
                Q(company__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(salary__icontains=search_query) |
                Q(work_experience__icontains=search_query) |
                Q(education__icontains=search_query) |
                Q(workTag__icontains=search_query) |
                Q(welfare__icontains=search_query) |
                Q(work_content__icontains=search_query)
            )

        # 添加城市优先级排序
        query = query.annotate(
            city_priority=Case(
                When(address__istartswith=default_city, then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('city_priority', '-post_time')

        # 获取所有字段
        return query.values(
            'id',
            'title',
            'address',
            'post_time',
            'work_experience',
            'education',
            'salary',
            'company',
            'workTag',
            'welfare',
            'work_content'
        )
    except Exception as e:
        print(f"获取推荐数据出错: {str(e)}")
        return []


def process_job_data(job):
    # 处理工作标签
    tags = str(job['workTag']).replace('｜', '|')
    if '/' in tags:
        job['workTag'] = [tag.strip() for tag in tags.split('/')]
    else:
        job['workTag'] = [tag.strip() for tag in tags.split(',')]

    # 处理福利标签
    if job['welfare']:
        job['welfare'] = [w.strip() for w in str(job['welfare']).split(',')]
    else:
        job['welfare'] = []

    return job


def recommend(request):
    if request.method == 'GET':
        try:
            # 基础信息获取
            uname = request.session.get('username', '822zyy')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            userInfo = User.objects.get(username=uname)
            default_city = "武汉"

            # 获取搜索关键词和页码
            search_query = request.GET.get('search', '').strip()
            page = request.GET.get('page', 1)

            # 获取数据
            recomData = getRecomData(search_query, default_city)

            # 获取用户收藏的职位ID列表
            favorited_job_ids = set(Favorite.objects.filter(
                user=userInfo
            ).values_list('job_id', flat=True))

            # 处理数据
            processed_data = []
            for job in recomData:
                job = process_job_data(job)
                job['is_favorited'] = job['id'] in favorited_job_ids
                processed_data.append(job)

            # 分页处理
            paginator = Paginator(processed_data, 7)  # 每页显示7条数据
            try:
                page = int(page)
                if page > paginator.num_pages:
                    page = 1
                current_page = paginator.get_page(page)
            except (ValueError, TypeError):
                current_page = paginator.get_page(1)

            # 准备上下文数据
            context = {
                'userInfo': userInfo,
                'recomData': current_page,
                'search_query': search_query,
                'current_time': current_time,
                'total_count': len(processed_data),
                'default_city': default_city,
                'page_range': paginator.page_range,
                'total_pages': paginator.num_pages,
                'current_page': page
            }

            return render(request, 'recommend.html', context)

        except Exception as e:
            print(f"推荐视图处理出错: {str(e)}")
            return render(request, 'recommend.html', {'error': '获取推荐数据失败'})


# def getRecomData(user_city=None):
#     """
#     获取推荐数据，根据用户所在城市优先排序
#     """
#     try:
#         # 获取所有职位数据
#         recom_jobs = RecomData.objects.all()
#
#         if user_city:
#             # 使用 annotate 和 Case/When 进行排序
#             recom_jobs = recom_jobs.annotate(
#                 city_match=Case(
#                     # 完全匹配城市名
#                     When(address__istartswith=user_city, then=Value(1)),
#                     default=Value(2),
#                     output_field=IntegerField(),
#                 )
#             ).order_by('city_match', '-post_time')  # 先按城市匹配度排序，然后按发布时间倒序
#
#         # 转换为值列表
#         recom_jobs = recom_jobs.values(
#             'id',
#             'title',
#             'address',
#             'post_time',
#             'work_experience',
#             'education',
#             'salary',
#             'company',
#             'workTag',
#             'welfare',
#             'work_content'
#         )
#
#         return recom_jobs
#     except Exception as e:
#         print(f"获取推荐数据出错: {str(e)}")
#         return []
#
#
# def recommend(request):
#     if request.method == 'GET':
#         try:
#             uname = request.session.get('username', '822zyy')
#             current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             userInfo = User.objects.get(username=uname)
#
#             # 获取默认城市（这里设置为武汉）
#             default_city = "武汉"
#
#             # 获取所有数据（按城市优先排序）
#             recomData = list(getRecomData(default_city))
#
#             # 获取用户收藏的职位ID列表
#             favorited_job_ids = set(Favorite.objects.filter(
#                 user=userInfo
#             ).values_list('job_id', flat=True))
#
#             # 获取搜索关键词
#             search_query = request.GET.get('search', '').lower()
#
#             # 预处理数据
#             filtered_data = []
#             for job in recomData:
#                 # 处理工作标签
#                 tags = str(job['workTag']).replace('｜', '|')
#                 if '/' in tags:
#                     job['workTag'] = [tag.strip() for tag in tags.split('/')]
#                 else:
#                     job['workTag'] = [tag.strip() for tag in tags.split(',')]
#
#                 # 处理福利标签
#                 if job['welfare']:
#                     job['welfare'] = [w.strip() for w in str(job['welfare']).split(',')]
#                 else:
#                     job['welfare'] = []
#
#                 # 添加收藏状态
#                 job['is_favorited'] = job['id'] in favorited_job_ids
#
#                 # 添加城市信息
#                 job['city'] = extract_city(job['address'])
#
#                 # 如果有搜索关键词，进行过滤
#                 if search_query:
#                     searchable_content = [
#                         job['title'].lower(),
#                         job['company'].lower(),
#                         job['address'].lower(),
#                         job['salary'].lower(),
#                         job['work_experience'].lower(),
#                         job['education'].lower(),
#                         ' '.join(job['workTag']).lower(),
#                         ' '.join(job['welfare']).lower() if job['welfare'] else '',
#                         str(job['work_content']).lower()
#                     ]
#
#                     if any(search_query in content for content in searchable_content):
#                         filtered_data.append(job)
#                 else:
#                     filtered_data.append(job)
#
#             # 手动对结果进行排序
#             if not search_query:
#                 filtered_data.sort(key=lambda x: (
#                     0 if x['city'] == default_city else 1,  # 武汉市优先
#                     -datetime.strptime(x['post_time'], '%Y-%m-%d').timestamp()  # 按发布时间倒序
#                 ))
#
#             # 分页处理
#             page = request.GET.get('page', 1)
#             paginator = Paginator(filtered_data, 7)  # 每页显示7条数据
#
#             try:
#                 page = int(page)
#                 if page > paginator.num_pages:
#                     page = 1
#                 page_obj = paginator.get_page(page)
#             except (ValueError, TypeError):
#                 page_obj = paginator.get_page(1)
#
#             return render(request, 'recommend.html', {
#                 'userInfo': userInfo,
#                 'recomData': page_obj,
#                 'search_query': search_query,
#                 'current_time': current_time,
#                 'total_count': len(filtered_data),
#                 'default_city': default_city
#             })
#
#         except Exception as e:
#             print(f"推荐视图处理出错: {str(e)}")
#             return render(request, 'recommend.html', {
#                 'error': '获取推荐数据失败'
#             })


# def getRecomData():
#     try:
#         recom_jobs = RecomData.objects.all().values(
#             'id',  # 添加 id 字段
#             'title',
#             'address',
#             'post_time',
#             'work_experience',
#             'education',
#             'salary',
#             'company',
#             'workTag',
#             'welfare',
#             'work_content'
#         )
#         return recom_jobs
#     except Exception as e:
#         print(f"获取推荐数据出错: {str(e)}")
#         return []
#
#
# def recommend(request):
#     if request.method == 'GET':
#         try:
#             uname = request.session.get('username', '822zyy')
#             current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             userInfo = User.objects.get(username=uname)
#
#             # 获取所有数据
#             recomData = list(getRecomData())
#
#             # 获取用户收藏的职位ID列表
#             favorited_job_ids = set(Favorite.objects.filter(
#                 user=userInfo
#             ).values_list('job_id', flat=True))
#
#             # 获取搜索关键词
#             search_query = request.GET.get('search', '').lower()
#
#             # 预处理数据
#             filtered_data = []
#             for job in recomData:
#                 # 处理工作标签
#                 tags = str(job['workTag']).replace('｜', '|')
#                 if '/' in tags:
#                     job['workTag'] = [tag.strip() for tag in tags.split('/')]
#                 else:
#                     job['workTag'] = [tag.strip() for tag in tags.split(',')]
#
#                 # 处理福利标签
#                 if job['welfare']:
#                     job['welfare'] = [w.strip() for w in str(job['welfare']).split(',')]
#                 else:
#                     job['welfare'] = []
#
#                 # 添加收藏状态
#                 job['is_favorited'] = job['id'] in favorited_job_ids
#
#                 # 如果有搜索关键词，进行过滤
#                 if search_query:
#                     # 扩展搜索范围
#                     searchable_content = [
#                         job['title'].lower(),
#                         job['company'].lower(),
#                         job['address'].lower(),
#                         job['salary'].lower(),
#                         job['work_experience'].lower(),
#                         job['education'].lower(),
#                         ' '.join(job['workTag']).lower(),
#                         ' '.join(job['welfare']).lower() if job['welfare'] else '',
#                         str(job['work_content']).lower()
#                     ]
#
#                     if any(search_query in content for content in searchable_content):
#                         filtered_data.append(job)
#                 else:
#                     filtered_data.append(job)
#
#             # 分页处理
#             page = request.GET.get('page', 1)
#             paginator = Paginator(filtered_data, 7)  # 每页显示7条数据
#
#             try:
#                 page = int(page)
#                 if page > paginator.num_pages:
#                     page = 1
#                 page_obj = paginator.get_page(page)
#             except (ValueError, TypeError):
#                 page_obj = paginator.get_page(1)
#
#             return render(request, 'recommend.html', {
#                 'userInfo': userInfo,
#                 'recomData': page_obj,
#                 'search_query': search_query,
#                 'current_time': current_time,
#                 'total_count': len(filtered_data)  # 添加总数据量
#             })
#
#         except Exception as e:
#             print(f"推荐视图处理出错: {str(e)}")
#             return render(request, 'recommend.html', {
#                 'error': '获取推荐数据失败'
#             })


def dp_page(request):
    if request.method == 'GET':
        uname = request.session.get('username')
        userInfo = User.objects.get(username=uname)
        return render(request, 'dp_page.html', {
            'userInfo': userInfo
        })


@require_http_methods(["POST"])
def toggle_favorite(request):
    try:
        data = json.loads(request.body)
        job_id = data.get('job_id')
        action = data.get('action')
        username = request.session.get('username')  # 获取当前登录用户的用户名

        if not job_id or action not in ['add', 'remove'] or not username:
            return JsonResponse({
                'success': False,
                'message': '无效的请求参数或未登录'
            }, status=400)

        user = User.objects.get(username=username)
        job = get_object_or_404(RecomData, id=job_id)

        if action == 'add':
            # 创建收藏
            favorite, created = Favorite.objects.get_or_create(
                user=user,
                job=job
            )
            is_favorited = True
        else:
            # 删除收藏
            Favorite.objects.filter(user=user, job=job).delete()
            is_favorited = False

        return JsonResponse({
            'success': True,
            'message': '收藏成功' if is_favorited else '取消收藏成功',
            'is_favorited': is_favorited
        })

    except RecomData.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '职位不存在'
        }, status=404)
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '用户不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_favorites(request):
    try:
        username = request.session.get('username')
        if not username:
            return JsonResponse({
                'success': False,
                'message': '未登录'
            }, status=401)

        user = User.objects.get(username=username)
        favorites = Favorite.objects.filter(user=user).select_related('job')
        favorite_jobs = []

        for favorite in favorites:
            job = favorite.job
            favorite_jobs.append({
                'id': job.id,
                'title': job.title,
                'salary': job.salary,
                'company': job.company,
                'address': job.address,
                'created_at': favorite.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({
            'success': True,
            'favorites': favorite_jobs
        })

    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': '用户不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


client = OpenAI(
    api_key="sk-151eeb6bfc644d1892771c67da4bf236",
    base_url="https://api.deepseek.com"
)


# 渲染页面的视图函数
def dp_page(request):
    context = {
        'userInfo': {
            'username': request.user.username if request.user.is_authenticated else 'Guest'
        }
    }
    return render(request, 'dp_page.html', context)


@csrf_exempt
def chat_with_deepseek(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant. Please format your responses with:\n" +
                                       "1. Proper line breaks between paragraphs\n" +
                                       "2. Use markdown formatting for headers (###) and lists (-)\n" +
                                       "3. Use **bold** for emphasis\n" +
                                       "4. Add proper spacing between sections\n"
                        },
                        {"role": "user", "content": user_message}
                    ],
                    stream=False
                )

                # 格式化响应文本
                ai_response = response.choices[0].message.content
                formatted_response = ai_response.replace('\n', '<br>')  # 转换换行符为HTML换行

                return JsonResponse({
                    'status': 'success',
                    'response': formatted_response
                })
            except Exception as api_error:
                return JsonResponse({
                    'status': 'error',
                    'message': f'API调用错误：{str(api_error)}'
                }, status=500)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'系统错误：{str(e)}'
            }, status=500)
    return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=400)


def create_city_data():
    # 城市列表
    cities = ['beijing', 'shanghai', 'guangzhou', 'shenzhen', 'hangzhou', 'chengdu']
    # 编程语言列表
    languages = ['java', 'cpp', 'python', 'php']

    # 创建测试数据
    for city in cities:
        for lang in languages:
            cityData.objects.get_or_create(
                city=city,
                programming_language=lang,
                defaults={'job_count': random.randint(50, 500)}
            )
