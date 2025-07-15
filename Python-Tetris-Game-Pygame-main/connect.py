import mysql.connector


class Leaderboard:
    def __init__(self, host="localhost", user="root", password="", database="tetris"):
        """Initialize the leaderboard with a MySQL database."""
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the leaderboard table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INT AUTO_INCREMENT PRIMARY KEY,
            player_name VARCHAR(4) NOT NULL,
            score INT NOT NULL
        );
        """)
        self.conn.commit()

    def add_score(self, player_name, score):
        """Add a new score to the leaderboard."""
        self.cursor.execute("""
        INSERT INTO leaderboard (player_name, score)
        VALUES (%s, %s);
        """, (player_name, score))
        self.conn.commit()

    def get_top_scores(self, limit=10):
        """Retrieve the top scores from the leaderboard."""
        self.cursor.execute("""
        SELECT player_name, score
        FROM leaderboard
        ORDER BY score DESC
        LIMIT %s;
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()


