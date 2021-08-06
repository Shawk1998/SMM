from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


def index(request, username):
    return render(request, 'index.html', context={"username": username})


def detail(request):
    return render(request, 'detail.html')


def login(request):
    # 显示登录界面
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        # 获取提交的用户和密码
        username = request.POST.get("username")
        password = request.POST.get("password")

    result = user_login(username, password)
    # 如果失败
    if result['result'] == 0:
        return render(request, 'login.html', context={
            "msg": result['msg'],
            "un": username,
            "pd": password})
    elif result['result'] == 1:
        # return render(request, 'index.html', context={"msg": result['msg']})
        return redirect(reverse('userindex', kwargs={'username': username}))


# 从文件读取学生信息
def read_student_from_file(path: str):
    """
       从文件中读取学生信息
       数据如下： [{}{}{}{}{}]
       :return:
       """
    # 定义集合存储数据
    students = []
    infos = ['sno', 'name', 'gender', 'birthday', 'mobile', 'email', 'address']
    # 读取
    try:
        with open(path, mode='r', encoding='utf-8-sig') as fd:
            current_line = fd.readline()
            while current_line:
                # 切分属性信息
                student = current_line.strip().replace("\n", "").split(",")
                # 定义临时集合
                temp_student = {}
                for index in range(len(infos)):
                    temp_student[infos[index]] = student[index]
                # 附加到集合中
                students.append(temp_student)
                # 读取下一行
                current_line = fd.readline()
            # 返回
            return students

    except Exception as e:
        print("读取文件出现异常，具体为：" + str(e))


# 从文件读取用户信息
def read_user_from_file(path: str):
    """
       从文件中读取学生信息
       数据如下： [{}{}{}{}{}]
       :return:
       """
    # 定义集合存储数据
    users = []
    infos = ['username', 'password', 'status']
    # 读取
    try:
        with open(path, mode='r', encoding='utf-8-sig') as fd:
            current_line = fd.readline()
            while current_line:
                # 切分属性信息
                user = current_line.strip().replace("\n", "").split(",")
                # 定义临时集合
                temp_user = {}
                for index in range(len(infos)):
                    temp_user[infos[index]] = user[index]
                # 附加到集合中
                users.append(temp_user)
                # 读取下一行
                current_line = fd.readline()
            # 返回
            return users

    except Exception as e:
        print("读取文件出现异常，具体为：" + str(e))


def user_login(username: str, password: str):
    """
    用户完成身份验证
    :param username:用户名
    :param password: 密码
    :return:
    """
    # 读取所有用户
    path = r'D:\py\SMM\student\static\files\user.txt'
    users = read_user_from_file(path)
    # 定义一个返回结果
    result_dict = {"result": 1, 'msg': '登陆成功'};
    # 开始身份验证
    for index in range(len(users)):
        # 判断用户名和密码
        if users[index]["username"].strip().upper() == username.strip().upper():
            if users[index]["status"] == '0':
                result_dict["result"] = 0
                result_dict["msg"] = "账号已禁用！"
                return result_dict
            elif users[index]["password"] == password:
                return result_dict
            else:
                result_dict["result"] = 0
                result_dict["msg"] = "密码错误！"
                return result_dict
    # 如果最后一个也验证完了，则返回用户不存在
    result_dict["result"] = 0
    result_dict["msg"] = "用户不存在！"
    return result_dict


def get_student_by_sno(sno):
    stuList = []
    # 获取学员信息
    path = r"D:\py\SMM\student\static\files\Student.txt"
    students = read_student_from_file(path)
    # for index in range(len(students)):
    #     # 精准查询
    #     if students[index]['sno'] == str(sno):
    #         stuList.append(students[index])
    # return stuList

    for student in students:
        # 模糊查询
        if sno in student['sno']:
            stuList.append(student)
    return stuList


def user_index(request, username):
    path = r"D:\py\SMM\student\static\files\Student.txt"
    students = read_student_from_file(path)
    if request.method == "GET":
    # 获取学员信息
        return render(request, 'index.html', context={'username': username, 'students': students})
    elif request.method == "POST":
        sno = request.POST.get("sno")
        if sno == '':
            return render(request, 'index.html', context={'username': username, 'students': students})
        else:
            results = get_student_by_sno(sno)
            print(results)
            return render(request, "index.html", context={'username': username, 'students': results, 'querysno': sno})


def detail(request):
    """
    展示学生明细信息
    :param request:
    :return:
    """
    # 触发一个查询 --SNo
    sno = request.GET.get('sno')
    username= request.GET.get('username')
    # 查询
    student = get_student_by_sno(sno)
    print(student)
    # 把数据传递到页面
    return render(request, 'detail.html', context={'student': student,'username':username})


if __name__ == '__main__':

        print(get_student_by_sno(95001))
