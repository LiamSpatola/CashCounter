from __future__ import annotations
from models.database import Database
from models.currency import Currency


class Denomination(Database):
    def __init__(
        self, currency: Currency, value: float, denomination_id: int | None = None
    ) -> None:
        super().__init__()
        self.currency: Currency = currency
        self.value: float = value
        self.denomination_id: int | None = denomination_id

    # ORM Methods
    def exists(self) -> bool:
        if self.denomination_id:
            sql: str = (
                "SELECT EXISTS(SELECT 1 FROM denominations WHERE denomination_id = ?) AS denomination_exists"
            )
            params: tuple = (self.denomination_id,)
            result = self.query(sql, params)

            row = result[0]
            return bool(row["denomination_exists"])
        return False

    def save(self) -> int | None:
        if self.exists():
            self._update()
        else:
            new_denomination_id = self._insert()
            self.count_id = new_denomination_id
            return new_denomination_id

    def _update(self) -> None:
        sql: str = (
            "UPDATE denominations SET currency = ?, value = ? WHERE denomination_id = ?"
        )
        params: tuple = (self.currency.currency_id, self.value, self.denomination_id)
        self.query(sql, params)

    def _insert(self) -> int:
        sql: str = "INSERT INTO denominations (currency, value) VALUES (?, ?)"
        params: tuple = (self.currency.currency_id, self.value)
        return self.query(sql, params)

    # Utility Methods
    @classmethod
    def load_by_denomination_id(cls, denomination_id: int) -> Denomination | None:
        db = Database()
        sql: str = "SELECT * FROM denominations WHERE denomination_id = ?"
        params: tuple = (denomination_id,)
        result = db.query(sql, params)

        if result:
            # Using the results to build a denomination object
            row = result[0]
            return cls(
                Currency.load_by_currency_id(row["currency"]),
                row["value"],
                denomination_id=row["denomination_id"],
            )
        return None

    @classmethod
    def get_all_denominations(cls) -> list[Denomination | None]:
        db = Database()
        sql: str = "SELECT * FROM denominations"
        result = db.query(sql)

        denominations = list()
        for row in result:
            denominations.append(
                cls(
                    Currency.load_by_currency_id(row["currency"]),
                    row["value"],
                    denomination_id=row["denomination_id"],
                )
            )

        return denominations
    
    @classmethod
    def get_denomination_by_currency(cls, currency: Currency) -> list[Denomination | None]:
        db = Database()
        sql: str = "SELECT * FROM denominations WHERE currency = ?"
        params: tuple = (currency.currency_id,)
        result = db.query(sql, params)

        denominations = list()
        for row in result:
            denominations.append(
                cls(
                    Currency.load_by_currency_id(result["currency"]),
                    row["value"],
                    denomination_id=row["denomination_id"],
                )
            )

        return denominations
