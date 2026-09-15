import sqlite3


class DATA_BASE:
    def __init__(self):
        self.connection = sqlite3.connect("pacman.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player (
            id INTERGER PRIMARY KEY,
            name TEXT,
            score INTERGER
            )
        """)

    def insert_on_table(self, name: str, score: int):
        data = self.get_scores()
        for information in data:
            if name in information[0]:
                if score > information[1]:
                    self.Update_score(score, name)
                return
        self.cursor.execute(f"""
            INSERT INTO player (name, score)
            VALUES (?, ?)
        """, (name, score)
        )
        self.connection.commit()

    def get_scores(self):
        self.cursor.execute("""
            SELECT name, score FROM player ORDER BY score DESC LIMIT 10
        """)
        data = self.cursor.fetchall()
        return data


    def Update_score(self, score, name):
        self.cursor.execute("""
            UPDATE player
            SET score = ?
            WHERE name = ?
        """, (score, name)
        )