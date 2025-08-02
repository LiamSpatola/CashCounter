from models.database import Database


class Currency(Database):
    def __init__(self, symbol: str, name: str, currency_id: int | None) -> None:
        super().__init__()
        self.symbol: str = symbol
        self.name: str = name
        self.currency_id: int | None = currency_id

    # ORM Methods
    def exists(self) -> bool:
        if self.currency_id:
            sql: str = "SELECT EXISTS(SELECT 1 FROM currencies WHERE currency_id = ?) AS currency_exists"
            params: tuple = (self.currency_id,)
            result = self.query(sql, params)

            row = result[0]
            return bool(row["currency_exists"])
        return False

    def save(self) -> int | None:
        if self.exists():
            self._update()
        else:
            new_currency_id = self._insert()
            self.currency_id = new_currency_id
            return new_currency_id
        
    def _update(self) -> None:
        sql: str = "UPDATE currencies SET symbol = ?, name = ? WHERE currency_id = ?"
        params: tuple = (self.symbol, self.name, self.currency_id)
        self.query(sql, params)

    def _insert(self) -> int:
        sql: str = "INSERT INTO currencies (symbol, name) VALUES (?, ?)"
        params: tuple = (self.symbol, self.name)
        return self.query(sql, params)

    # Utility Methods
    @classmethod
    def load_by_currency_id(cls, currency_id) -> "Currency" | None:
        db = Database()
        sql: str = "SELECT * FROM currencies WHERE currency_id = ?"
        params: tuple = (currency_id,)
        result = db.query(sql, params)

        if result:
            # Using the results to build a Currency object
            row = result[0]
            return cls(row["symbol"], row["name"], currency_id=row["currency_id"])
        return None

    @classmethod
    def get_all_currencies(cls) -> list["Currency" | None]:
        db = Database()
        sql: str = "SELECT * FROM currencies"
        result = db.query(sql)

        currencies = list()
        for row in result:
            currencies.append(cls(row["symbol"], row["name"], currency_id=row["currency_id"]))

        return currencies