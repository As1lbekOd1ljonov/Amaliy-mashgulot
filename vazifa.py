# vazifa 1
from decimal import Decimal, InvalidOperation
import random
from datetime import datetime, timedelta


class TemperatureDescriptor:
    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        try:
            value = Decimal(value).quantize(Decimal("0.0"))
        except InvalidOperation:
            raise ValueError("Harorat qiymati Decimal formatda bo‘lishi kerak.")

        if not (-50 <= value <= 50):
            raise ValueError("Harorat me’yordan chiqib ketdi (-50°C dan 50°C gacha).")

        self._value = value


class Temperature:
    temperature = TemperatureDescriptor()

    def __init__(self, temperature=None):
        if temperature is not None:
            self.temperature = temperature
        self.timestamp = self._generate_random_datetime()

    @staticmethod
    def _generate_random_datetime():
        current_time = datetime.now()
        random_days = random.randint(0, 365)
        random_time = current_time - timedelta(days=random_days)
        return random_time

    def __str__(self):
        return f"Harorat: {self.temperature}°C ({self.timestamp.strftime('%Y-%m-%d')})"


temperatures = []
for _ in range(10):
    temp_value = random.uniform(-10, 40)
    try:
        temp = Temperature(temp_value)
        temperatures.append(temp)
    except ValueError as e:
        print(f"Xatolik: {e}")

for temp in temperatures:
    print(temp)

# ==================================================================================================================

# vazifa 2
from decimal import Decimal, InvalidOperation
import random
from datetime import datetime, timedelta


class InsufficientFundsError(Exception):
    pass


class TransactionDescriptor:

    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        try:
            value = Decimal(value).quantize(Decimal("0.01"))  # Ikkita o‘nlik xona
        except InvalidOperation:
            raise ValueError("Tranzaksiya summasi Decimal formatda bo‘lishi kerak.")

        if value < 0:
            raise ValueError("Tranzaksiya summasi manfiy bo‘lishi mumkin emas.")

        self._value = value


class BankAccount:
    transaction_amount = TransactionDescriptor()

    def __init__(self, initial_balance=0):
        self.balance = Decimal(initial_balance).quantize(Decimal("0.01"))
        self.transactions = []

    def _generate_random_datetime(self):
        current_time = datetime.now()
        random_days = random.randint(0, 30)
        random_time = current_time - timedelta(days=random_days)
        return random_time

    def deposit(self, amount):
        """Pul qo‘shish."""
        self.transaction_amount = amount
        self.balance += self.transaction_amount
        self.transactions.append((self.transaction_amount, self._generate_random_datetime(), "Deposit"))
        print(f"{amount} UZS qo‘shildi. Joriy balans: {self.balance} UZS.")

    def withdraw(self, amount):
        """Pul yechish."""
        self.transaction_amount = amount
        if self.balance < self.transaction_amount:
            raise InsufficientFundsError("Balans yetarli emas!")

        self.balance -= self.transaction_amount
        self.transactions.append((self.transaction_amount, self._generate_random_datetime(), "Withdraw"))
        print(f"{amount} UZS yechildi. Joriy balans: {self.balance} UZS.")

    def show_balance(self):
        """Joriy balansni ko‘rsatish."""
        print(f"Hisobingiz: {self.balance} UZS.")

    def show_transactions(self):
        """Tranzaksiyalarni ko‘rsatish."""
        print("Tranzaksiyalar:")
        for amount, date, txn_type in self.transactions:
            print(f"{txn_type}: {amount} UZS ({date.strftime('%Y-%m-%d')})")


try:
    account = BankAccount(initial_balance=500000)
    account.show_balance()

    account.deposit(100000)
    account.withdraw(200000)
    account.withdraw(600000)

except InsufficientFundsError as e:
    print(f"Xatolik: {e}")

except ValueError as e:
    print(f"Xatolik: {e}")

account.show_transactions()

# ==================================================================================================================

# vazifa 3
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
import random



class TicketPrice:
    """Descriptor: faqat Decimal formatdagi chipta narxini qabul qiladi."""
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, Decimal('0.00'))
    def __set__(self, instance, value):
        try:
            value = Decimal(value)
            if value <= Decimal('0.00'):
                raise ValueError("Chipta narxi manfiy yoki nol bo'lishi mumkin emas!")
            instance.__dict__[self.name] = value
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f"Yaroqsiz chipta narxi: {e}")
    def __set_name__(self, owner, name):
        self.name = name
class Ticket:
    price = TicketPrice()
    def __init__(self, price):
        """Chiptaning narxi va sotish sanasini o‘rnatish."""
        self.price = price
        self.sale_date = self.__generate_random_date()

    @staticmethod
    def __generate_random_date():
        """Tasodifiy sotish sanasini generatsiya qilish."""
        start_date = datetime.now()
        random_days = random.randint(1, 30)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")
    def show_ticket_info(self):
        """Chipta haqida ma'lumotni qaytarish."""
        return f"Chipta narxi: {self.price} UZS. Sotish sanasi: {self.sale_date}."
if __name__ == "__main__":
    print("Chipta sotib olish dasturiga xush kelibsiz!")
    while True:
        try:
            ticket_price = input("Chipta narxini kiriting (UZS): ")
            ticket = Ticket(ticket_price)
            print(ticket.show_ticket_info())
        except ValueError as e:
            print(f"Xato: {e}")
        choice = input("Yana chipta yaratmoqchimisiz? (ha/yo'q): ").strip().lower()
        if choice != 'ha':
            print("Dasturdan chiqmoqdasiz. Xayr!")
            break

# ==================================================================================================================

# vazifa 4
from datetime import datetime, timedelta
import random
from decimal import Decimal, InvalidOperation

class SalaryDescriptor:
    def __init__(self):
        self._value = None

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        try:
            decimal_value = Decimal(value)
            if decimal_value <= 0:
                raise ValueError("Oylik miqdori musbat bo'lishi kerak.")
            self._value = decimal_value
        except (InvalidOperation, ValueError):
            raise ValueError("Oylik miqdori to'g'ri Decimal formatida kiritilishi kerak.")

class EmployeeSalary:
    salary = SalaryDescriptor()

    def __init__(self, salary):
        self.salary = salary
        self.payment_date = self._generate_random_payment_date()

    @staticmethod
    def _generate_random_payment_date():
        today = datetime.now()
        random_days = random.randint(1, 28)
        return today.replace(day=random_days)

    def __str__(self):
        return f"Ishchi oyligi: {self.salary:,} UZS. To'lov sanasi: {self.payment_date.date()}"

try:
    employee = EmployeeSalary("3200000")
    print(employee)
except ValueError as e:
    print(f"Xato: {e}")







