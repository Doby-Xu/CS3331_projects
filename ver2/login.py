# -*- coding: utf-8 -*-
"""
登录/注册类

@author: Doby Xu
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np


np.save('./database/users.npy',[])
np.save('./database/signup.npy', [])


#用户账号类
class ID:
    def __init__(self, name, pw, is_admin):
        self.user_name = name
        self.password = pw
        self.is_admin = is_admin


#待审核用户账号类
class SignUpID:
    def __init__(self, name, pw, real_name = "", addr = ""):
        self.user_name = name
        self.password = pw
        self.real_name = real_name
        self.addr = addr
    
        
#用户账号数据库
#
#
class UserDataBase:
    def __init__(self):
        #已注册用户
        self.users = list(np.load('./database/users.npy', allow_pickle=True))
        #待审核用户
        self.signup = list(np.load('./database/signup.npy', allow_pickle=True))
    
    #登录
    #核查用户名和密码
    #返回
    #用户名无效     -2
    #密码不匹配     -1
    #普通用户登录    0
    #管理员登录      1
    def sign_in(self, user_name, password):
        no = -1
        for i in range(len(self.users)):
            if user_name == self.users[i].user_name:
                #print("匹配成功，序号"+str(i))
                no = i
                break
        if no == -1:
            
            return -2
        
        if password != self.users[no].password:
            return -1
        else:
            return self.users[no].is_admin
            
    def get_signup_name(self):
        res = []
        for i in range(len(self.signup)):
            res.append(self.signup[i].user_name)
        return res
    
    def update(self):
        np.save('./database/users.npy', self.users)
        np.save('./database/signup.npy', self.signup)
        
    def sign_up(self, user_name, password, real_name = "", addr = ""):
        new_id = SignUpID(user_name, password, real_name, addr)
        #为待审核用户赋予编号
        new_id.no = len(self.signup)
        self.signup.append(new_id)
        self.update()
        return 1
        
    #审核通过时调用
    def approve(self, no):
        if no<0 or no >= len(self.signup):
            return 0
        new_ID = ID(self.signup[no].user_name, self.signup[no].password, 0)
        
        new_ID.no = len(self.users)
        self.users.append(new_ID)
        
        del self.signup[no]
        while (no<len(self.signup)):
            self.signup[no].no-=1
            no+=1
            
        self.update()
        return 1
        
    #审核不通过时调用
    def reject(self, no):
        if no<0 or no >= len(self.signup):
            return 0
        del self.signup[no]
        while (no<len(self.signup)):
            self.signup[no].no-=1
            no+=1
            
        self.update()
        return 1
        
ud = UserDataBase()          

class SignIn:
    
    def main_page(self, win = None):
        if win:
            win.destroy()
        win = tk.Tk()
        self.win = win
        win.geometry('220x100')
        win.resizable()
        win.title('你帮我助——登录界面')
        
        def sign_in():
            ud.update()
            res = ud.sign_in(e_user_name.get(), e_password.get())
            if res == -2:
                messagebox.showinfo(title=':(', message='用户不存在')
            elif res == -1:
                messagebox.showinfo(title=':(', message='用户名或密码错误')
            elif res == 0:
                print("登录成功，打开用户窗口")
                self.win.destroy()
                #user = User()
                #user.main_page_user()
                
            elif res == 1:
                print("登录成功，打开管理员窗口")
                self.win.destroy()
                #admin = Admin()
                #admin.main_page_admin()
                
        
            
        l_user_name = tk.Label(self.win,text="用户名：")
        l_user_name.grid(row = 0, column = 0, sticky="w")
        e_user_name = tk.Entry(self.win)    
        e_user_name.grid(row = 0, column = 1)
        
        
        l_password = tk.Label(self.win,text="密码：")
        l_password.grid(row = 1, column = 0, sticky="w")
        e_password = tk.Entry(self.win)    
        e_password.grid(row = 1, column = 1)
        
        #登录按钮
        b = tk.Button(self.win, text="登录", width=5, 
                               command = lambda:sign_in())
        b.grid(row = 2, column = 0)
        
        
        b_sign_up = tk.Button(self.win, text="注册", width=5, 
                               command = lambda:self.sign_up())
        b_sign_up.grid(row = 2, column = 1)
        
        win.mainloop()
        
    def sign_up(self):
        win = tk.Tk()
        
        win.geometry('450x300')
        win.resizable()
        win.title('你帮我助——注册界面')
        
        def click():
            if e_pw1.get() != e_pw2.get():
                messagebox.showinfo(title=':(', message='两次输入密码不一致')
                return
            if len(e_pw1.get())<6:
                messagebox.showinfo(title=':(', message='密码长度应大于6位')
                return
            if e_user_name.get() == "":
                messagebox.showinfo(title=':(', message='请输入用户名')
                return
            for i in range(len(self.users)):
                if e_user_name.get() == self.users[i].user_name:
                    #print("匹配成功，序号"+str(i))
                    messagebox.showinfo(title=':(', message='用户名已存在')
                    return
                
            ud.sign_up(e_user_name.get(), e_pw1.get(), e_real_name.get(), e_addr.get())
            messagebox.showinfo(title='', message='注册成功，请等待管理员审核')
            win.destroy()
        
        
        l_user_name = tk.Label(win,text="请输入用户名：")
        l_user_name.grid(row = 0, column = 0)
        e_user_name = tk.Entry(win)    
        e_user_name.grid(row = 0, column = 1)
        
        l_pw1 = tk.Label(win,text="请输入密码：")
        l_pw1.grid(row = 1, column = 0)
        e_pw1 = tk.Entry(win)    
        e_pw1.grid(row = 1, column = 1)
        
        l_pw2 = tk.Label(win,text="请再次输入密码：")
        l_pw2.grid(row = 2, column = 0)
        e_pw2 = tk.Entry(win)    
        e_pw2.grid(row = 2, column = 1)
        
        l_real_name = tk.Label(win,text="请输入业主真实姓名：")
        l_real_name.grid(row = 3, column = 0)
        e_real_name = tk.Entry(win)    
        e_real_name.grid(row = 3, column = 1)
        
        l_addr = tk.Label(win,text="请输入业主地址：")
        l_addr.grid(row = 4, column = 0)
        e_addr = tk.Entry(win)    
        e_addr.grid(row = 4, column = 1)
        
        b_sign_up = tk.Button(win, text="确定", width=5, 
                               command = lambda:click())
        b_sign_up.grid(row = 5, column = 1)


if __name__ == '__main__':
    
    #管理员是一个特殊的账户，特殊关照
    id_admin = ID("admin", "123456", 1)
    id_admin.no = 0
    
    np.save('./database/users.npy',[id_admin])
    np.save('./database/signup.npy', [])
    
    ud = UserDataBase()
    
    def print_id(id_list):
        for i in range(len(id_list)):
            print("用户名\t"+id_list[i].user_name+"\t\t密码\t"+id_list[i].password+"\t\t编号\t"+str(id_list[i].no))
            
    print(ud.sign_up("小王", "456789"))     
    print(ud.sign_up("小潇", "wdas89"))
    print(ud.sign_up("小李", "456789", "李铁根", "x10"))  
    
    print("待批准列表：")
    print_id(ud.signup)
    
    print("批准ing")
    
    #print(ud.approve(0))
    #print(ud.approve(1))
    
    print("待批准列表：")
    print_id(ud.signup)
    
    print("用户列表：")
    print_id(ud.users)
    
    print(ud.sign_in("admin", "123456"))
    print(ud.sign_in("小镇", "123456"))
    print(ud.sign_in("admin", "12345"))
    print(ud.sign_in("小王", "456789"))
    #1 -2 -1 0
    
    #测试成功
    #s = SignIn()
    #s.main_page()
    
    
            
    
