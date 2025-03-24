from django.shortcuts import render, redirect
from myApp.models import *
from django.http import HttpResponseRedirect
from django.contrib import messages

def changePwd(userInfo,passwordInfo):
    oldPwd = passwordInfo['oldpassword']
    newPwd = passwordInfo['newpwd']
    ckPwd = passwordInfo['ckpwd']
    user = User.objects.get(username=userInfo.username)

    if oldPwd != user.password:

        return '原密码错误'
    if newPwd != ckPwd:
        return '两次密码不一致'
    user.password = newPwd
    user.save()