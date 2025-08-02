from bcrypt import gensalt, hashpw, checkpw
from models.database import Database


class User(Database):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        is_admin: bool,
        user_id: int | None = None
    ) -> None:
        super().__init__()
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.username: str = username
        self.is_admin: bool = is_admin
        self.user_id: int | None = user_id

    # ORM Methods
    def exists(self) -> bool:
        if self.user_id:
            sql: str = (
                "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?) AS user_exists"
            )
            params: tuple = (self.user_id,)
            result = self.query(sql, params)

            row = result[0]
            return bool(row["user_exists"])
        return False

    def save(self, new_password: str | None = None) -> int | None:
        if self.exists():
            self._update(new_password)
        else:
            if not new_password:
                raise ValueError("New password is required to insert user.")
            new_user_id = self._insert(new_password)
            self.user_id = new_user_id
            return new_user_id

    def _update(self, new_password: str | None = None) -> None:
        if new_password:
            hashed_new_password: bytes = self.hash_password(new_password)
            sql: str = (
                "UPDATE users SET first_name = ?, last_name = ?, username = ?, password = ?, is_admin = ? WHERE user_id = ?"
            )
            params: tuple = (
                self.first_name,
                self.last_name,
                self.username,
                hashed_new_password,
                int(self.is_admin),
                self.user_id,
            )
        else:
            sql: str = (
                "UPDATE users SET first_name = ?, last_name = ?, username = ?, is_admin = ? WHERE user_id = ?"
            )
            params: tuple = (
                self.first_name,
                self.last_name,
                self.username,
                int(self.is_admin),
                self.user_id,
            )

        self.query(sql, params)

    def _insert(self, password: str) -> int:
        hashed_password: bytes = self.hash_password(password)

        sql: str = (
            "INSERT INTO users (first_name, last_name, username, password, is_admin) VALUES (?, ?, ?, ?, ?)"
        )
        params: tuple = (
            self.first_name,
            self.last_name,
            self.username,
            hashed_password,
            int(self.is_admin),
        )
        return self.query(sql, params)

    # Utility Methods
    @classmethod
    def load_by_username(cls, username: str) -> "User" | None:
        db = Database()
        sql: str = "SELECT * FROM users WHERE username = ?"
        params: tuple = (username,)
        result = db.query(sql, params)

        if result:
            # Using the results to build a user object
            row = result[0]
            return cls(
                row["first_name"],
                row["last_name"],
                row["username"],
                bool(row["is_admin"]),
                user_id=row["user_id"]
            )
        return None
    
    @classmethod
    def load_by_user_id(cls, user_id: int) -> "User" | None:
        db = Database()
        sql: str = "SELECT * FROM users WHERE user_id = ?"
        params: tuple = (user_id,)
        result = db.query(sql, params)

        if result:
            # Using the results to build a user object
            row = result[0]
            return cls(
                row["first_name"],
                row["last_name"],
                row["username"],
                bool(row["is_admin"]),
                user_id=row["user_id"]
            )
        return None
    
    @classmethod
    def get_all_users(cls) -> list["User" | None]:
        db = Database()
        sql: str = "SELECT * FROM users"
        result = db.query(sql)

        users = list()
        for row in result:
            users.append(cls(row["first_name"], row["last_name"], row["username"], bool(row["is_admin"]), user_id=row["user_id"]))

        return users

    # Authentication Methods
    @staticmethod
    def hash_password(password: str) -> bytes:
        return hashpw(password.encode(), gensalt())

    @staticmethod
    def verify_password(hashed_password: str | bytes, password: str) -> bool:
        # Making sure the hashed password is a byte
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode()

        return checkpw(password.encode(), hashed_password)

    @classmethod
    def login(cls, username: str, password: str) -> "User" | None:
        # Getting the hashed password from the DB
        db = Database()
        sql: str = "SELECT password FROM users WHERE username = ?"
        params: tuple = (username,)
        result = db.query(sql, params)

        if not result:
            return None  # No user found

        row = result[0]
        hashed_password = row["password"]
        # Checking the password is correct
        if cls.verify_password(hashed_password, password):
            return cls.load_by_username(username)  # Login successful
        else:
            return None  # Incorrect password
