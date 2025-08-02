from __future__ import annotations
from models.database import Database
from models.denomination import Denomination
from models.count import Count


class CountRecord(Database):
    def __init__(
        self,
        denomination: Denomination,
        count: Count,
        quantity: float,
        count_record_id: int | None = None,
    ) -> None:
        super().__init__()
        self.denomination: Denomination = denomination
        self.count: Count = count
        self.quantity: int = quantity
        self.count_record_id: int | None = count_record_id

    # ORM Methods
    def exists(self) -> bool:
        if self.count_record_id:
            sql: str = (
                "SELECT EXISTS(SELECT 1 FROM count_records WHERE count_record_id = ?) AS count_record_exists"
            )
            params: tuple = (self.count_record_id,)
            result = self.query(sql, params)

            row = result[0]
            return bool(row["count_record_exists"])
        return False

    def save(self) -> int | None:
        if self.exists():
            self._update()
        else:
            new_count_record_id = self._insert()
            self.count_record_id = new_count_record_id
            return new_count_record_id

    def _update(self) -> None:
        sql: str = (
            "UPDATE count_records SET denomination = ?, count = ?, quantity = ? WHERE count_record_id = ?"
        )
        params: tuple = (
            self.denomination.denomination_id,
            self.count.count_id,
            self.quantity,
            self.count_record_id,
        )
        self.query(sql, params)

    def _insert(self) -> int:
        sql: str = "INSERT INTO count_records (denomination, count, quantity) VALUES (?, ?, ?)"
        params: tuple = (self.denomination.denomination_id, self.count.count_id, self.quantity)
        return self.query(sql, params)

    # Utility Methods
    @classmethod
    def load_by_count_record_id(cls, count_record_id: int) -> CountRecord | None:
        db = Database()
        sql: str = "SELECT * FROM count_records WHERE count_record_id = ?"
        params: tuple = (count_record_id,)
        result = db.query(sql, params)

        if result:
            # Using the results to build a count record object
            row = result[0]
            return cls(
                Denomination.load_by_denomination_id(row["denomination"]),
                Count.load_by_count_id(row["count"]),
                row["quantity"],
                count_record_id=row["count_record_id"],
            )
        return None

    @classmethod
    def get_all_count_records(cls) -> list[CountRecord | None]:
        db = Database()
        sql: str = "SELECT * FROM count_records"
        result = db.query(sql)

        count_records = list()
        for row in result:
            count_records.append(
                cls(
                    Denomination.load_by_denomination_id(row["denomination"]),
                    Count.load_by_count_id(row["count"]),
                    row["quantity"],
                    count_record_id=row["count_record_id"],
                )
            )

        return count_records

    @classmethod
    def get_count_records_by_count(cls, count: Count) -> list[CountRecord | None]:
        db = Database()
        sql: str = "SELECT * FROM count_records WHERE count = ?"
        params: tuple = (count.count_id,)
        result = db.query(sql, params)

        count_records = list()
        for row in result:
            count_records.append(
                cls(
                    Denomination.load_by_denomination_id(row["denomination"]),
                    count.count_id,
                    row["quantity"],
                    count_record_id=row["count_record_id"],
                )
            )

        return count_records

    def calculate_total_value(self) -> float:
        return float(self.quantity * self.denomination.value)
