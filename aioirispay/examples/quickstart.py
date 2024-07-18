from aioirispay import IrisPay
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder


irispay = IrisPay("irispay.session", 0, "your-api-hash", "username")
bot = Bot(token="your-bot-token", default=DefaultBotProperties(parse_mode="HTMLL"))
dp = Dispatcher()

invoiceNumber = 0

def checkPay(invoice_id: str):
    buider = InlineKeyboardBuilder()
    buider.button(text="Check pay", callback_data=f"check:{invoice_id}")

    return buider.as_markup()

@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """
    Command from the app stats.
    """

    info = await irispay.get_app_stats()

    await message.reply(f"Total invoices: {info['total']}\nTotal paid: {info['paid']}\nTotal not paid: {info['active']}")

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    global invoiceNumber
    user = message.from_user

    if user.username is not None:
        user = user.username
    else:
        user = user.id

    invoice = await irispay.create_invoice(1, "Donate from @{user}".format(user=user))
    invoiceNumber = invoiceNumber + 1
    target = await irispay.get_user()

    kb = checkPay(invoice)

    await message.reply("Hello, {user}!\nFrom test donate, go to @iris_black_bot and send 1 iris with comment below.\nComment: {comment}\n\nFrom convenience copy the text below:\n<code>передать 1 {target}\n{invoice}</code>".format(user=message.from_user.first_name, comment=invoice, target=target, invoice=invoice), reply_markup=kb)


@dp.callback_query()
async def callback_query(query: types.CallbackQuery):
    if query.data.startswith("check"):
        invoice = query.data.split(":")[1]
        msg = await query.message.edit_text("🔍 Search payment...")
        info = await irispay.check_pay(invoice)
        if info["status"] == "paid":
            await msg.edit_text("✅ Payment found.\n⭐ Thank you for the donate in size of {amount} toffees!".format(amount=info["amount"]))
        else:
            if info["status"] == "active":
                await msg.edit_text("❌ Invoice not paid.", reply_markup=checkPay(invoice))
            else:
                if info["status"] == "already_paid":
                    await msg.edit_text("❌ Invoice already paid.")
                else:
                    await msg.edit_text("❌ Other.")


async def main():
    await irispay.start()
    await bot.delete_webhook(True)
    await dp.start_polling(bot)

asyncio.run(main())