import sqlite3
from typing import Any


class DATA_BASE:
    """
    Represent a data base for save the scores

    Attributes
    ________
    connection: Connection
        represents the connection to the on-disk database.
    cursor: Cursor
        represents a database cursor which is used to execute SQL statements

    Methods
    ________
    create_table():
        create the table player on the data base
    insert_on_table():
        insert the name and the score from the provider args
    get_scores():
        select the 10 high scores from the table
    update_score():
        select the player on the table and update with new score
    """
    def __init__(self, file: str = "pacman.db"):
        """Initialize the connection and curson."""
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()

    def create_table(self) -> None:
        """Create a table on the data base"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player (
            id INTERGER PRIMARY KEY,
            name TEXT,
            score INTERGER
            )
        """)

    def insert_on_table(
        self,
        name: str,
        score: int,
        skip: bool = False
    ) -> None:
        """
        Insert the name and score on te data base, if its exist we update.
        Args:
            name:  str
                The name of the player to insert on the data base
            score: int
                The score of the player to insert on the data base
            skip: bool
                If true the current player is unknow so we will skip the update

        Returns:
            None
        """
        data = self.get_scores()
        for information in data:
            if name in information[0] and not skip:
                if score > information[1]:
                    self.update_score(score, name)
                return
        self.cursor.execute("""
            INSERT INTO player (name, score)
            VALUES (?, ?)
        """, (name, score)
        )
        self.connection.commit()

    def get_scores(self) -> list[Any]:
        """
        Get the 10 higher scores from the table
        Returns:
            The list containing the 10 players.
        """
        self.cursor.execute("""
            SELECT name, score FROM player ORDER BY score DESC LIMIT 10
        """)
        data = self.cursor.fetchall()
        return data

    def update_score(self, score: int, name: str) -> None:
        """
        Update the player score on the data base
        Args:
            score: int
                The provider player new score
            name: str
                The provider player name
        Returns:
            None
        """
        self.cursor.execute("""s
            UPDATE player
            SET score = ?
            WHERE name = ?
        """, (score, name)
        )
