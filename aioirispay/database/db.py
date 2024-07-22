import json
import os
import datetime

database_path = os.path.dirname(os.path.abspath(__file__))

class Database:
    def __init__(self, path: str = f"{database_path}/db.json"):
        self.path = path
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.data = json.load(f)
        else:
            try:
                with open(self.path, "x") as f:
                    self.data = {}
            except:
                self.load()

    def get(self, owner: str, key: str, default):
        if owner in self.data:
            if key in self.data[owner]:
                return self.data[owner][key]
        return default
    
    def uset(self, owner: str, key: str, value):
        if owner not in self.data:
            self.data[owner] = {}
        self.data[owner][key] = value

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f)
    
    async def willInfo(self, meid: str):
        status = self.get("willInfo", meid, None)
        if status is None:
            return False
        return True
    
    async def updateWillInfo(self, meid: str):
        self.uset("willInfo", meid, True)
        self.save()

    async def get_invoice(self, invoice_id: str):
        return self.get("invoices", invoice_id, None)
    
    async def get_invoices(self, invoice_ids: list[str]):
        return [self.get("invoices", invoice_id, None) for invoice_id in invoice_ids]
    
    async def create_invoice(self, invoice_id: str, amount: int, description: str):
        self.uset("invoices", invoice_id, {"user": None, "amount": amount, "description": description, "status": "active", "create_date": str(datetime.datetime.now()), "pay_date": None})
        self.save()
    
    async def update_invoice(self, invoice_id: str, user: str, status: str):
        invoice = await self.get_invoice(invoice_id)
        amount = invoice["amount"]
        description = invoice["description"]
        create_date = invoice["create_date"]
        self.uset("invoices", invoice_id, {"user": user, "amount": amount, "description": description, "status": status, "create_date": create_date, "pay_date": str(datetime.datetime.now())})
        self.save()
    
    async def clear_invoices(self):
        self.data["invoices"] = {}
        self.save()

    async def get_app_stats(self):
        invoices = self.data["invoices"]
        active, paid, total = 0, 0, 0
        for invoice in invoices:
            invoice = invoices[invoice]
            if invoice["status"] == "active":
                active += 1
            if invoice["status"] == "paid":
                paid += 1
            total += 1
        
        data = {"active": active, "paid": paid, "total": total}
        return data

database = Database()