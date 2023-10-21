from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
import datetime
import redis

nameEntry = None
genderVar = None
loginEntry = None
passwordEntry = None

#Заполнение данных в Redis
def fillRedis(userName, userGender, userLogin, userPassword, userDateAuth):
    userData = {
        'Логин' : userLogin,
        'Имя' : userName,
        'Пол' : userGender
    }
    userLoginData = {
        'Логин' : userLogin,
        'Пароль' : userPassword,
        'Дата последней авторизации' : userDateAuth
    }

    redisClient = redis.StrictRedis(host='localhost', port=6379)
    redisClient.select(0)
    redisClient.hmset(f'Data_{userLogin}', userData)
    redisClient.select(1)
    redisClient.hmset(f'LoginData_{userLogin}', userLoginData)


def limitName(text):
    if len(text) < 40 and all(char.isalpha() or char.isspace() for char in text):
        return True
    else:
        return False


def limitLogin(text):
    if len(text) < 15:
        return True
    else:
        return False


def limitPassword(text):
    if len(text) < 30:
        return True
    else:
        return False


def authorization():
    global nameEntry, genderVar, loginEntry, passwordEntry

    userName = nameEntry.get()
    userGender = genderVar.get()
    userLogin = loginEntry.get()
    userPassword = passwordEntry.get()
    if(userName == '' or userLogin == '' or userPassword == ''):
        showerror(title='Ошибка', message='Заполните все данные')
    else:
        showinfo(title='Информация', message='Вы успешно авторизовались')
        userDateAuth = datetime.datetime.now().strftime("%d-%m-%Y")
        fillRedis(userName, userGender, userLogin, userPassword, userDateAuth)
        #print(f'Имя: {userName}\nПол: {userGender}Login: {userLogin}\nPassword: {userPassword}')

def ui():
    global nameEntry, genderVar, loginEntry, passwordEntry

    root = Tk()
    root.title('Окно авторизации')
    root.geometry('450x250+550+200')
    root.resizable(False, False)
    root['bg'] = '#FFE4C4'

    mainLabel = Label(root, text='Авторизация пользователя', font='Arial 15 bold', bg='#FFE4C4')
    mainLabel.pack(pady=10)

    formFrame = Frame(root, bg='#FFE4C4')
    formFrame.pack(expand=True)

    #Имя пользователя
    nameLabel = Label(formFrame, text='Полное ФИО:', font='Arial 12 bold', bg='#FFE4C4')
    nameLabel.grid(row=0, column=0, sticky='w')
    nameEntry = Entry(formFrame, font=('Arial', 12))
    nameEntry.grid(row=0, column=1, padx=10, pady=5)
    #Проверка на ввод не более 40 символов (все буквы)
    checkNameEntry = (root.register(limitName), '%P')
    nameEntry.configure(validate='key', validatecommand=checkNameEntry)

    #Пол пользователя
    genderLabel = Label(formFrame, text='Выберите ваш пол:', font='Arial 12 bold', bg='#FFE4C4')
    genderLabel.grid(row=1, column=0, sticky='w')
    genderVar = StringVar(value='Мужской')
    #Выбор пола пользователя
    malebtn = Radiobutton(formFrame, text='Мужской', value='Мужской', variable=genderVar)
    malebtn.grid(row=1, column=1, sticky='w', padx=(10, 0))
    malebtn.configure(font='Arial 10 bold', bg='#FFE4C4')
    femalebtn = Radiobutton(formFrame, text='Женский', value='Женский', variable=genderVar)
    femalebtn.grid(row=1, column=1, padx=(80, 0))
    femalebtn.configure(font='Arial 10 bold', bg='#FFE4C4')

    #Логин пользователя
    loginLabel = Label(formFrame, text='Логин:', font='Arial 12 bold', bg='#FFE4C4')
    loginLabel.grid(row=2, column=0, sticky='w')
    loginEntry = Entry(formFrame, font=('Arial', 12))
    loginEntry.grid(row=2, column=1, padx=10, pady=5)
    #Проверка на ввод не более 15 символов
    checkLoginEntry = (root.register(limitLogin), '%P')
    loginEntry.configure(validate='key', validatecommand=checkLoginEntry)

    #Пароль пользователя
    passwordLabel = Label(formFrame, text='Пароль:', font='Arial 12 bold', bg='#FFE4C4')
    passwordLabel.grid(row=3, column=0, sticky='w')
    passwordEntry = Entry(formFrame, show='*', font=('Arial', 12))
    passwordEntry.grid(row=3, column=1, padx=10, pady=5, sticky='w')
    #Проверка на ввод не более 30 символов
    checkPasswordEntry = (root.register(limitPassword), '%P')
    passwordEntry.configure(validate='key', validatecommand=checkPasswordEntry)

    button = Button(root, text='Авторизоваться', command=authorization)
    button.pack(pady=10)
    button.config(font='Arial 12 bold', bg='#FFCA8A')

    root.mainloop()


def main():
    ui()

if __name__ == '__main__':
    main()
