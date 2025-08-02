from datetime import datetime
from models.database import Database
from models.user import User
from models.currency import Currency


class Count(Database):
    def __init__(self, user: User, currency: Currency, date: datetime = datetime.now(), count_id: int | None = None):
        self.user: User = user
        self.currency: Currency = currency
        self.date: datetime = date
        self.count_id: int | None = count_id

    # ORM Methods
    def exists(self) -> bool:
        if self.count_id:
            sql: str = "SELECT EXISTS(SELECT 1 FROM counts WHERE count_id = ?) AS count_exists"
            params: tuple = (self.count_id,)
            result = self.query(sql, params)

            row = result[0]
            return bool(row["count_exists"])
        return False
    
    def save(self) -> int | None:
        if self.exists():
            self._update()
        else:
            new_count_id = self._insert()
            self.count_id = new_count_id
            return new_count_id
        
    def _update(self) -> None:
        sql: str = "UPDATE counts SET user = ?, date = ?, currency = ? WHERE count_id = ?"
        params: tuple = (self.user.user_id, self.date.isoformat(" "), self.currency.currency_id, self.count_id)
        self.query(sql, params)
    
    def _insert(self) -> int:
        sql: str = "INSERT INTO counts (user, date, currency) VALUES (?, ?, ?)"
        params: tuple = (self.user.user_id, self.date.isoformat(" "), self.currency.currency_id)
        return self.query(sql, params)
    
    # Utility Methods
    @classmethod
    def load_by_count_id(cls, count_id: int) -> "Count" | None:
        db = Database()
        sql: str = "SELECT * FROM counts WHERE count_id = ?"
        params: tuple = (count_id,)
        result = db.query(sql, params)

        if result:
            # Using the results to build a count object
            row = result[0]
            return cls(User.load_by_user_id(row["user"]), Currency.load_by_currency_id(row["currency_id"]), datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"), count_id = row["count_id"])
        return None
    
    @classmethod
    def get_all_counts(cls) -> list["Count" | None]:
        db = Database()
        sql: str = "SELECT * FROM counts"
        result = db.query(sql)

        counts = list()
        for row in result:
            counts.append(cls(User.load_by_user_id(row["user"]), Currency.load_by_currency_id(row["currency_id"]), datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"), count_id = row["count_id"]))
        
        return counts
    
    def calculate_total_value(self) -> float:
        # TODO: Implement this code
        pass