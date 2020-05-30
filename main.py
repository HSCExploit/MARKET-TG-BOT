#!/usr/bin/python
# -*- coding: utf-8 -*-
# Coded By HSC_EXPLOIT
import time
from threading import Thread
import telebot
from telebot import types
import json
import os
import sqlite3
import sys
import random
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

bot_token = '1207362313:AAHDYedQQ7NkDYxC6W17GT13oRf7pbUt_Cs'
admins = ['397808645']
check_id = '397808645'
coders = ['423795868']
groups = ['Courses', 'Accounts', 'Docs', 'Else']
bot = telebot.TeleBot(bot_token)
start_user_text = '''
Здравствуйте! Я бот продажник!
Для просмотра ваших команд введите: /help
'''
help_user_text = '''
Просмотреть список всех товаров - /products
Количество товаров в магазине - /prnum
Написать в тех-поддержку - /support
'''
start_admin_text = '''
Здравствуйте, администратор!
Для просмотра ваших команд введите: /help
'''
help_admin_text ='''
Посмотреть список товаров - /products
Удалить товар - /del *id товара*
Добавить товар - /add *Название* *описание* *стоимость*
'''

# Coded By HSC_EXPLOIT


@bot.message_handler(commands=['start'])
def start_message(message):
  if (str(message.chat.id) in admins):
    bot.send_message(message.from_user.id, start_admin_text)
  else:
    bot.send_message(message.from_user.id, start_user_text)



@bot.message_handler(commands=['help'])
def help_message(message):
  if (str(message.chat.id) in admins):
    bot.send_message(message.from_user.id, help_admin_text)
  else:
    bot.send_message(message.from_user.id, help_user_text)



@bot.message_handler(commands=['prnum'])
def view_pr_num(message):
  db_connect = sqlite3.connect('db.sqlite')
  cursor = db_connect.cursor()
  cursor.execute("SELECT * FROM Products")
  all_pr = cursor.fetchall()
  bot.send_message(message.from_user.id, str(len(all_pr)) + f' Товара(ов) доступно на данный момент.')
  db_connect.commit()
  db_connect.close()
  
# Coded By HSC_EXPLOIT
@bot.message_handler(commands=['my_id'])
def get_my_id(message):
  bot.send_message(message.from_user.id, str(message.chat.id))



@bot.message_handler(commands=['groups'])
def view_groups(message):
  if (str(message.chat.id) in admins):
    bot.send_message(message.from_user.id, str(groups))

@bot.message_handler(commands=['support'])
def support(message):
  bot.send_message(message.from_user.id, 'Для получения помощи пишите: @levchikBB')

@bot.message_handler(commands=['clear_wait'])
def clear_w(message):
  if (str(message.chat.id) in coders):
    db_connect = sqlite3.connect('db.sqlite')
    cursor = db_connect.cursor()
    cursor.execute("DELETE FROM Wait")
    db_connect.commit()
    db_connect.close()
    bot.send_message(message.from_user.id, 'Очередь проверки оплаты очищена')
  else:
    pass
#DELETE FROM table1
# Coded By HSC_EXPLOIT
@bot.message_handler(commands=['products'])
def view_products(message):
  if (str(message.chat.id) in admins):
    db_connect = sqlite3.connect('db.sqlite')
    cursor = db_connect.cursor()
    ###cursor.execute("CREATE TABLE Products(Id INT, Type TEXT, Name TEXT, Desc TEXT, Price INT)")


    #      ID    Type Name Desc Price
    random_id = random.randint(1000, 9999)
    random_id2 = random.randint(1,100)
    random_id = random_id + random_id2
    #cursor.execute(f"INSERT INTO Products VALUES({random_id}, 'Courses', 'Курс python3', 'Самый лучший курс!!!', 1600)")
    cursor.execute("SELECT * FROM Products")
    data = cursor.fetchall()
    num_d = 0
    if (len(data) == 0):
      bot.send_message(message.from_user.id, 'Товары отсутствуют.')
    else:
      for i in range(len(data)):
        bot.send_message(message.from_user.id, f'ID: {str(data[num_d][0])}\nГруппа: {str(data[num_d][1])}\nНазвание: {str(data[num_d][2])}\nОписание: {str(data[num_d][3])}\nЦена: {str(data[num_d][4])}р\nСсылка: {str(data[num_d][5])}')
        num_d = num_d + 1
      #print(str(data))
      db_connect.close()
  else:
    db_connect = sqlite3.connect('db.sqlite')
    cursor = db_connect.cursor()
    ###cursor.execute("CREATE TABLE Products(Id INT, Type TEXT, Name TEXT, Desc TEXT, Price INT)")


    #      ID    Type Name Desc Price
    random_id = random.randint(1000, 9999)
    random_id2 = random.randint(1,100)
    random_id = random_id + random_id2
    #cursor.execute(f"INSERT INTO Products VALUES({random_id}, 'Courses', 'Курс python3', 'Самый лучший курс!!!', 1600)")
    cursor.execute("SELECT * FROM Products")
    data = cursor.fetchall()
    num_d = 0
    if (len(data) == 0):
      bot.send_message(message.from_user.id, 'Товары отсутствуют.')
    else:
      for i in range(len(data)):
        user_id = message.chat.id
        keyboard = types.InlineKeyboardMarkup()
        kb1 = types.InlineKeyboardButton(text="Купить", callback_data='buy '+str(data[num_d][0]) + ' ' + str(data[num_d][4]))
        keyboard.add(kb1)
        bot.send_message(message.from_user.id, f'ID: {str(data[num_d][0])}\nГруппа: {str(data[num_d][1])}\nНазвание: {str(data[num_d][2])}\nОписание: {str(data[num_d][3])}\nЦена: {str(data[num_d][4])}р', reply_markup = keyboard)
        num_d = num_d + 1
      db_connect.close()

@bot.callback_query_handler(func=lambda c:True)
def buttons_responce(responce):
    user_id = str(responce.message.chat.id)
    keyboard = types.InlineKeyboardMarkup()
    responce_data = responce.data
    responce_data = responce_data.split(' ')
    if responce_data[0] == 'buy':
      id_comment = responce_data[1]
      pay_buttons = types.InlineKeyboardMarkup()
      qiwi_button = types.InlineKeyboardButton(text="Qiwi", callback_data='qiwi ' + user_id + ' ' + responce_data[1] + ' ' + responce_data[2])
      yandex_button = types.InlineKeyboardButton(text="Яндекс Деньги", callback_data='yad ' + user_id + ' ' + responce_data[1] + ' ' + responce_data[2])
      sber_button = types.InlineKeyboardButton(text="Сбербанк Онлайн", callback_data='sber ' + user_id + ' ' + responce_data[1] + ' ' + responce_data[2])
      pay_buttons.add(yandex_button)
      pay_buttons.add(sber_button)
      pay_buttons.add(qiwi_button)
      bot.send_message(user_id, 'Выберите способ оплаты: ', reply_markup = pay_buttons)
    else:
      if responce_data[0] == 'qiwi':
        str_meth = 'Qiwi'
        responce_data_qiwi_ns = responce.data
        responce_data_qiwi = responce_data_qiwi_ns.split(' ')
        #bot.send_message(user_id, str(responce_data_qiwi))
        check_buttons = types.InlineKeyboardMarkup()
        check_pay = types.InlineKeyboardButton(text="Проверить оплату", callback_data='check ' + user_id + ' ' + responce_data_qiwi[0] + ' ' + responce_data_qiwi[1] + ' ' + responce_data_qiwi[2] + ' ' + responce_data_qiwi[3])
        check_buttons.add(check_pay)
        bot.send_message(user_id, 'Переведите ' + responce_data_qiwi[3] + ' рублей на кошелек +79780128538 c комментарием: ' + str(user_id) + ' ' + responce_data_qiwi[2] + '\nПосле оплаты нажмите кнопку "Проверить оплату". Проверка оплаты занимает от 1 минуты до 24 часов. Если оплата не была проверена - обратитесь в тех-поддержку.', reply_markup = check_buttons)


# Coded By HSC_EXPLOIT






      else:
        if responce_data[0] == 'yad':
          str_meth = 'Яндекс Деньги'
          responce_data_yad_ns = responce.data
          responce_data_yad = responce_data_yad_ns.split(' ')
          #bot.send_message(user_id, str(responce_data_qiwi))
          check_buttons = types.InlineKeyboardMarkup()
          check_pay = types.InlineKeyboardButton(text="Проверить оплату", callback_data='check ' + user_id + ' ' + responce_data_yad[0] + ' ' + responce_data_yad[1] + ' ' + responce_data_yad[2] + ' ' + responce_data_yad[3])
          check_buttons.add(check_pay)
          bot.send_message(user_id, 'Переведите ' + responce_data_yad[3] + ' рублей на кошелек 410014115168263 c комментарием: ' + str(user_id) + ' ' + responce_data_yad[2] + '\nПосле оплаты нажмите кнопку "Проверить оплату". Проверка оплаты занимает от 1 минуты до 24 часов. Если оплата не была проверена - обратитесь в тех-поддержку.', reply_markup = check_buttons)
        else:
          if responce_data[0] == 'sber':
            str_meth = 'Сбербанк Онлайн'
            responce_data_sb_ns = responce.data
            responce_data_sb = responce_data_sb_ns.split(' ')
            #bot.send_message(user_id, str(responce_data_qiwi))
            check_buttons = types.InlineKeyboardMarkup()
            check_pay = types.InlineKeyboardButton(text="Проверить оплату", callback_data='check ' + user_id + ' ' + responce_data_sb[0] + ' ' + responce_data_sb[1] + ' ' + responce_data_sb[2] + ' ' + responce_data_sb[3])
            check_buttons.add(check_pay)
            bot.send_message(user_id, 'Переведите ' + responce_data_sb[3] + ' рублей на карту 5469 5200 1944 7127 c комментарием: ' + str(user_id) + ' ' + responce_data_sb[2] + '\nПосле оплаты нажмите кнопку "Проверить оплату". Проверка оплаты занимает от 1 минуты до 24 часов. Если оплата не была проверена - обратитесь в тех-поддержку.', reply_markup = check_buttons)
          else:
            if responce_data[0] == 'check':
              id_s = random.randint(10000, 99999) + random.randint(1, 1000)
              try:
                user = responce_data[1]
                method = responce_data[2]
                pr_id = responce_data[4]
                price_n = responce_data[5]
              except:
                bot.send_message(user_id, 'Не нужно кликать на кнопку несколько раз!')
              #bot.send_message(user_id, f'Пользователь: {user} Метод: {method} Товар: {pr_id} Стоимость: {price_n}')
              try:
                db_c = sqlite3.connect('db.sqlite')
                cursor_с = db_c.cursor()
                cursor_с.execute(f"SELECT * FROM Wait WHERE User={user_id}")
                wait_data = cursor_с.fetchall()

                xnum = 0
                for i in range(len(wait_data)):
                  if responce_data[4] in wait_data[xnum]:
                    xin = 1
                  else:
                    xin = 0
                  xnum = xnum +1
                if len(wait_data) < 1 or xin == 0:
                  if method == 'sber':
                    str_meth_s = 'Сбербанк Онлайн'
                  else:
                    if method == 'qiwi':
                      str_meth_s = 'Qiwi'
                    else:
                      if method == 'yad':
                        str_meth_s = 'Яндекс Деньги'

                  r_id = random.randint(10000, 99999) + random.randint(1, 1000)
                  cursor_с.execute(f"INSERT INTO Wait VALUES({r_id}, '{user_id}', '{pr_id}', '{price_n}', '{method}')")
                  
                  bot.send_message(user_id, f'Запрос на проверку оплаты отправлен!\nНомер запроса: ' + str(r_id) + '\nСумма: ' + str(price_n) + '\nСпособ оплаты: ' + str_meth_s + '\nID товара: ' + str(pr_id))
                  db_c.commit()
                  db_c.close()





                  check_moder_buttons = types.InlineKeyboardMarkup()
                  disallow_button = types.InlineKeyboardButton(text="Отклонить", callback_data=f'disallow {user} {r_id} {pr_id}')
                  allow_button = types.InlineKeyboardButton(text="Принять", callback_data=f'allow {user} {r_id} {pr_id}')
                  check_moder_buttons.add(disallow_button)
                  check_moder_buttons.add(allow_button)
                  bot.send_message(check_id, f'Пользователь: {user_id} запросил проверку оплаты.\nID товара: {pr_id}\nID запроса проверки: {r_id}\nСумма: {price_n}\nСпособ оплаты: {str_meth_s}', reply_markup = check_moder_buttons)
                else:
                  bot.send_message(user_id, f'Запрос на проверку уже обрабатывается.')
                  db_c.commit()
                  db_c.close()
              except:
                bot.send_message(user_id, 'Не нужно кликать на кнопку несколько раз!')
            else:
              if responce_data[0] == 'allow':
                db_c = sqlite3.connect('db.sqlite')
                cursor_с = db_c.cursor()
                cursor_с.execute(f"SELECT * FROM Products WHERE Id={responce_data[3]}")
                allow_data = cursor_с.fetchall()
                url_allow = allow_data[0][5]
                bot.send_message(responce_data[1], 'Ваша оплата одобрена!\nСсылка на товар: ' + url_allow)
                cursor_с.execute(f"DELETE FROM Wait WHERE ID = {responce_data[2]}")
                db_c.commit()
                db_c.close()
                bot.send_message(check_id, 'Оплата одобрена! Пользователю отправлена ссылка на товар.')
              else:
                if responce_data[0] == 'disallow':
                  db_c = sqlite3.connect('db.sqlite')
                  cursor_с = db_c.cursor()
                  bot.send_message(responce_data[1], 'Ваша оплата отклонена.')
                  cursor_с.execute(f"DELETE FROM Wait WHERE ID = {responce_data[2]}")
                  db_c.commit()
                  db_c.close()
                  bot.send_message(check_id, 'Оплата отклонена. Пользователю отправлено оповещение об отклонении оплаты.')
#5469 5200 1944 7127

# Coded By HSC_EXPLOIT

        #db_c = sqlite3.connect('db.sqlite')
        #cursor_с = db_c.cursor()
        #id_r = random.randint(1000, 9999)
        #id_r = id_r + random.randint(0, 100)
        #cursor_с.execute(f"INSERT INTO Wait VALUES({id_r}, '{str(user_id)}', '{responce.data}')")
        #db_c.commit()
        #db_c.close()
       # kb = types.InlineKeyboardMarkup()
        #kb1 = types.InlineKeyboardButton(text="Принять", callback_data=str(id_r)+' acc ' + str(user_id))
        #kb2 = types.InlineKeyboardButton(text="Отклонить", callback_data=str(id_r)+' dеc ' + str(user_id))
        #kb.add(kb1)
        #kb.add(kb2)
        #bot.send_message('423795868', 'Пользователь ' + str(user_id) + ' запросил проверку оплаты товара с ID: ' + str(c.data), reply_markup = kb)


#@bot.message_handler(commands=['add_mode'])
#def add_text(message):
	#bot.send_message(message.from_user.id, "Режим админа активирован!")
@bot.message_handler(content_types=['text'])
def add_products(message):
  if '/add' in message.text:
    if (str(message.chat.id) in admins):
      try:
        m = message.text
        add_command = m.split(' ')
        group = add_command[1]
        name = add_command[2]
        name = name.replace('_', ' ')
        desc = add_command[3]
        desc = desc.replace('_', ' ')
        price = add_command[4]
        url = add_command[5]
        random_id = random.randint(1000, 9999)
        random_id2 = random.randint(1,100)
        random_id = random_id + random_id2
        if (str(group) in groups):
          bot.send_message(message.from_user.id, f'Группа: {group}\nНазвание: {name}\nОписание: {desc}\nЦена: {price}\nURL: {url}\nID: {random_id}')
          bot.send_message(message.from_user.id, f'Товар будет добавлен товар в группу: {group}')
          db_connect = sqlite3.connect('db.sqlite')
          cursor = db_connect.cursor()
          cursor.execute(f"INSERT INTO Products VALUES({random_id}, '{group}', '{name}', '{desc}', {price}, '{url}')")
          db_connect.commit()
          db_connect.close()
        else:
          bot.send_message(message.from_user.id, f'Такой группы не существует!\nСписок существующих групп: {groups}')
      except Exception as exc: 
        print(exc)
        bot.send_message(message.from_user.id, 'Ошибка использования команды!\nПример использования: /add *Группа* *Название* *Описание* *Стоимость* *Ссылка*\nПосмотреть список доступных групп:  /groups')
    else:
      bot.send_message(message.from_user.id, 'Недостаточно прав для использования этой команды!')
  else:
    if '/del' in message.text:
      if str(message.chat.id) in admins:
# Coded By HSC_EXPLOIT
        try:
          m2 = message.text
          m2 = m2.split(' ')
          del_id = str(m2[1]) 
          db_connect = sqlite3.connect('db.sqlite')
          cursor = db_connect.cursor()
          cursor.execute(f"DELETE FROM Products WHERE ID = {del_id}")
          db_connect.commit()
          db_connect.close()
          bot.send_message(message.from_user.id, f'Товар с ID: {del_id} успешно удален!')
          
        except Exception as exc: 
          print(exc)
          bot.send_message(message.from_user.id, 'Ошибка использования команды!\nПример использования: /del *id*\nСписок товаров и их ID: /products')
      else:
        bot.send_message(message.from_user.id, 'Недостаточно прав для использования этой команды!')








bot.polling()
