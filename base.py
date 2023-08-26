from pyrogram import Client,filters
from pyrogram.types import User, Message,ReplyKeyboardMarkup
import redis
import csv

# fix forwards
# fix int & str      %
# database        %
# bottoms for motel and tutorial



api_id = 1500016
api_hash = "e07225f6d40b6208ea372b72c613d04c"
bot_token = "6439983840:AAHnoeQBI8lXEu5EYC5VDp0v1cv8_fTBYlg"
# proxy = { "scheme": "socks5","hostname": "localhost","port": 10808}

sut = redis.Redis(host='localhost', port=6379, decode_responses=True)

ids = []
person = []
let_go = False

bot = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    # proxy=proxy,
    bot_token=bot_token
)

def add_to_database(dd):
    with open('database.csv','w',encoding='utf-8',newline='') as database:
        csv_writer = csv.writer(database)
        csv_writer.writerow(dd)
        database.close()
    

def forward_to_admins(file, chat):
    bot.forward_messages('-858662794',chat,file)






@bot.on_message(filters.command('start') & filters.private)
def hello(bot, message):
    global let_go

    with open(r'database.csv',encoding='utf-8') as database:
        checkin = csv.reader(database)
        for id in checkin:
            ids.append(int(id[0]))
        database.close

    print(ids)
    if message.chat.id in ids:
        bot.send_message(message.chat.id, 'مشتی، شما که قبلا ثبت نام کردی!')
    else:
        bot.send_message(message.chat.id, 'سلام به کمپ تابستانه انجمن علمی برق خوش اومدید. 🤖🙋🏻‍♂️🙋🏻‍♀️')
        bot.send_message(message.chat.id, 'برای شروع اسم و فامیلت رو به صورت کامل بهم بگو')
        sut.set(message.chat.id,'name')
        person.append(message.chat.id)
        person.append('tell username: ' + message.from_user.username)

        let_go = True
        

@bot.on_message(filters.photo & filters.private)
def getpics(bot, message):
    global let_go
    if let_go == True:

        track = sut.get(message.chat.id)
        if track == 'id_img':
            # forward_to_admins(message.id, message.chat.id)

            person.append(message.id)
            bot.send_message(message.chat.id, 'و یه عکس هم از کارت ملی')
            sut.set(message.chat.id, 'meli_img')

        elif track == 'meli_img':
            # forward_to_admins(message.id, message.chat.id)

            person.append(message.id)
            bot.send_message(message.chat.id, 'خببب، حالا یه عکس هم از خودت برامون بفرست')
            sut.set(message.chat.id, 'pic')

        elif track == 'pic':
            
            bot.send_message(message.chat.id, 'خیلی هم عالی! ثبت نامت با موفقت انجام شد.')

            person.append(message.id)

            # forward_to_admins(message.id, message.chat.id)
            for i in person[-3::]:
                forward_to_admins(i, message.chat.id)
                
            for i in person[0:-3]:
                bot.send_message('-858662794', i)

            add_to_database(str(person[0]))
            sut.set(message.chat.id, 'done')






@bot.on_message(filters.private)
def getinfo(bot, message):
    global let_go
    if let_go == True:

        track = sut.get(message.chat.id)
        print(track)
        if track == 'name':
            try:
                int(message.text)
                bot.send_message(message.chat.id, 'باید به حروف فارسی وارد کنی')
            except:
                bot.send_message(message.chat.id, 'اسم بابات چیه؟')
                person.append('name: ' + message.text)
                sut.set(message.chat.id, 'fa_name')

        elif track == 'fa_name':
            try:
                int(message.text)
                bot.send_message(message.chat.id, 'باید به حروف فارسی وارد کنی')
            except:
                bot.send_message(message.chat.id, 'حالا شماره ملی؟')
                person.append('dad name: ' + message.text)
                sut.set(message.chat.id, 'id')

        elif track == 'id':
            try:
                int(message.text)
                bot.send_message(message.chat.id, 'خب آدرس تون کجاست؟')
                person.append('id num: ' + message.text)
                sut.set(message.chat.id, 'address')
            except:
                bot.send_message(message.chat.id, 'باید عدد وارد کنی:)')

        elif track == 'address':
            try:
                int(message.text)
                bot.send_message(message.chat.id, 'باید به حروف فارسی وارد کنی')
            except:
                bot.send_message(message.chat.id, 'شماره خودت هم بهم بگو')
                person.append('address: ' + message.text)
                sut.set(message.chat.id, 'ph_num')

        elif track == 'ph_num':
            try:
                int(message.text)
                bot.send_message(message.chat.id, 'شماره والدین هم لازمه:')
                person.append('phone num: ' + message.text)
                sut.set(message.chat.id, 'parents_num')
            except:
                bot.send_message(message.chat.id, 'باید عدد وارد کنی:)')

        elif track == 'parents_num':
            try:
                int(message.text)
                mess = 'اسمت رو تو کدوم دوره ها بنویسم؟'
                mess_bottom = [
                    [
                        ('Arduino'),
                        ('Altium Desin'),
                        ('Robotic'),
                        ('پکیج کامل')
                    ]
                ]
                mess_markup = ReplyKeyboardMarkup(mess_bottom,one_time_keyboard=True,resize_keyboard=True)
                message.reply(text=mess,reply_markup=mess_markup)                

                person.append('parent num: ' + message.text)
                sut.set(message.chat.id, 'tutorial')
            except:
                bot.send_message(message.chat.id, 'باید عدد وارد کنی:)')

        elif track == 'tutorial':

            person.append('tutorial: ' + message.text)
            if message.text == 'پکیج کامل':
                sut.set(message.chat.id, 'tutorial-done')
                bot.send_message(message.chat.id, 'یه بار دیگه بزن')
                pass

            if message.text == 'Arduino':
                mess = 'همین فقط؟'
                mess_bottom = [
                    [
                        ('Altium Desin'),
                        ('Robotic'),
                        ('همون بسه')
                    ]
                ]
                mess_markup = ReplyKeyboardMarkup(mess_bottom,one_time_keyboard=True,resize_keyboard=True)
                message.reply(text=mess,reply_markup=mess_markup)                

                sut.set(message.chat.id, 'tutorial-done')   

            elif message.text == 'Altium Desin':
                mess = 'همین فقط؟'
                mess_bottom = [
                    [
                        ('Arduino'),
                        ('Robotic'),
                        ('همون بسه')
                    ]
                ]
                mess_markup = ReplyKeyboardMarkup(mess_bottom,one_time_keyboard=True,resize_keyboard=True)
                message.reply(text=mess,reply_markup=mess_markup)                

                sut.set(message.chat.id, 'tutorial-done')    

            elif message.text == 'Robotic':
                mess = 'همین فقط؟'
                mess_bottom = [
                    [
                        ('Arduino'),
                        ('Altium Desin'),
                        ('همون بسه')
                    ]
                ]
                mess_markup = ReplyKeyboardMarkup(mess_bottom,one_time_keyboard=True,resize_keyboard=True)
                message.reply(text=mess,reply_markup=mess_markup)                

                sut.set(message.chat.id, 'tutorial-done')  
                
            pass

        elif track == 'tutorial-done':
            mess = 'و اینکه، برای اقامت به خوابگاه نیاز داری؟'
            mess_bottom = [
                [
                    ('بله'),
                    ('خیر')
                ]
            ]
            mess_markup = ReplyKeyboardMarkup(mess_bottom,one_time_keyboard=True,resize_keyboard=True)
            message.reply(text=mess,reply_markup=mess_markup)
            if message.text == 'Altium Desin' or message.text == 'Robotic' or message.text == 'Arduino':
                person.append('tutorial: ' + message.text)
            sut.set(message.chat.id, 'motel')

        elif track == 'motel':
            bot.send_message(message.chat.id, 'عا راستی! از کدوم دانشگاه اومدی؟')
            person.append('motel: ' + message.text)
            sut.set(message.chat.id, 'uni')

        elif track == 'uni':
            bot.send_message(message.chat.id, 'به یه عکس از صفحه اول شناسنامه هم نیاز دارم')
            person.append('uni: ' + message.text)
            sut.set(message.chat.id, 'id_img')


        # else:
        #     bot.send_message(message.chat.id, 'مشتی شما که قبلا ثبت نام کردی!')


bot.run()


