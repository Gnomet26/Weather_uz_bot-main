from threading import Thread
from Weather import ObHavo
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes
from bot_params import bot_token
from Sity_Dict import my_dict


class Weather_Uz_bot:
    def __init__(self):

        self.bot_config = ApplicationBuilder().token(bot_token).build()

        self.buttons = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[["Nukus"],["Toshkent"],["Buxoro"],["Guliston"],["Jizzax"],["Zarafshon"],["Qarshi"],["Navoiy"],["Namangan"],["Andijon"],["Samarqand"],["Termiz"],["Urganch"],["Farg'ona"],["Xiva"]])
        self.control_key = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[["Bugun"],["Haftalik"],["Ortga"]])
        self.bot_config.add_handler(CommandHandler("start",self.start))
        self.bot_config.add_handler(MessageHandler(filters=filters.TEXT,callback=self.user_message))
        self.bot_config.run_polling()

    async def start(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:

        await update.message.reply_html(f"Salom {update.effective_user.first_name} 👋.Men sizga ob-havo yangiliklarini ko'rsatishim mumkin",reply_markup=self.buttons)

    async def user_message(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
        ind = True
        for i in my_dict.keys():
            if(str(update.message.text) == str(i)):
                await update.message.reply_text("Kutib turing...")
                th = Thread(target=await self.send_data(update,context))
                th.start()
                ind = False
                break
            else:
                ind = True

        if(ind):
            await update.message.reply_text("Mening ro'yxatimda bu shahar yo'q ⚠️")

    async def send_data(self,update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
        str_hafta = ""
        data = ObHavo(str(update.message.text))
        for i in data.get_week():
            str_hafta += f"<b>{i[0]}  {i[1]}</b>\nKunduzi  <b>{i[2]}</b> , kechasi  <b>{i[3]}  {i[4]}</b>\n\n"


        str_bugun = f"<b>{data.get_today()[0]}</b>\n\nKunduzi  <b>{data.get_today()[1]}</b> kechasi  <b>{data.get_today()[2]}</b>   <b>{data.get_today()[3]}</b>"


        await update.message.reply_html(text=str_bugun)
        await update.message.reply_html(text="<b>🔽🔽Haftalik ma'lumot🔽🔽</b>")
        await update.message.reply_html(text=str_hafta)
        pass


if __name__ == "__main__":
    Weather_Uz_bot()