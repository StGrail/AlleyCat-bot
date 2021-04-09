import asyncio
import datetime
import asyncpg

from utils import config


class Database:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            database=config.DATABASE
        )
        return cls(pool)

    # таблица для регистрации всех гонщиков
    # Поменять время на timestamp иизменить это в коде
    async def create_table_racers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Racers (
                id INT NOT NULL,
                Name VARCHAR (255) NOT NULL,
                Gender VARCHAR (255),
                Bicycle VARCHAR (255),
                Start_time VARCHAR (255),
                Finish_time VARCHAR (255),
                Total_time VARCHAR (255),
                PRIMARY KEY (id)
                );
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num + 1}" for num, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    # добавление гонщика
    async def add_racer(self, id: int, name: str):
        sql = """
        INSERT INTO Racers (id, Name) VALUES ($1, $2)
        """
        await self.pool.execute(sql, id, name)

    # выбор всех гонщиков
    async def select_all_racers(self):
        sql = """
        SELECT * FROM Racers
        """
        return await self.pool.fetch(sql)

    # выбор одного гонщика
    async def select_racer(self, **kwargs):
        sql = """
        SELECT * FROM Racers WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    # всего гонщиков
    async def count_racers(self):
        return await self.pool.fetchval("SELECT COUNT (*) FROM Racers")

    # обновление пола при регистрации
    async def update_racer_gender(self, gender: str, id: int):
        sql = '''
        UPDATE Racers SET Gender = $1 WHERE id = $2
        '''
        return await self.pool.execute(sql, gender, id)

    # обновление типа велосипеда
    async def update_racer_bicycle(self, bicycle: str, id: int):
        sql = '''
        UPDATE Racers SET Bicycle = $1 WHERE id = $2
        '''
        return await self.pool.execute(sql, bicycle, id)

    # время старта
    async def start_time(self, start_time: str, id: int):
        sql = '''
        UPDATE Racers SET Start_time = $1 WHERE id = $2
        '''
        return await self.pool.execute(sql, start_time, id)

    async def get_start_time(self, id: int):
        sql = '''
        SELECT Start_time
        FROM Racers
        WHERE id = $1
        ;
        '''
        return await self.pool.fetchrow(sql, id)

    # время финиша
    async def finish_time(self, finish_time: str, id: int):
        sql = '''
        UPDATE Racers SET Finish_time = $1 WHERE id = $2
        '''
        return await self.pool.execute(sql, finish_time, id)

    # время гонки
    async def total_time(self, total_time: str, id: int):
        sql = '''
        UPDATE Racers SET Total_time = $1 WHERE id = $2
        '''
        return await self.pool.execute(sql, total_time, id)

    async def male_fixie_winners(self):
        sql = '''
        SELECT name, total_time
        FROM racers
        WHERE gender = 'male' AND bicycle = 'fixie'
        ORDER BY total_time
        LIMIT 3;
        '''
        return await self.pool.fetch(sql)

    async def female_fixie_winners(self):
        sql = '''
        SELECT name, total_time 
        FROM racers 
        WHERE gender = 'female' AND bicycle = 'fixie'
        ORDER BY total_time
        LIMIT 3;
        '''
        return await self.pool.fetchval(sql)

    async def male_multispeed_winners(self):
        sql = '''
        SELECT name, total_time 
        FROM racers 
        WHERE gender = 'male' AND bicycle = 'multispeed'
        ORDER BY total_time
        LIMIT 3;
        '''
        return await self.pool.fetchval(sql)

    async def female_multispeed_winners(self):
        sql = '''
        SELECT name, total_time
        FROM racers 
        WHERE gender = 'female' AND bicycle = 'multispeed'
        ORDER BY total_time
        LIMIT 3;
        '''
        return await self.pool.fetchval(sql)

    async def all_racers_time(self):
        sql = '''
        SELECT name, total_time 
        FROM racers 
        ORDER BY total_time
        '''
        return await self.pool.fetch(sql)

    async def delete_racers(self):
        await self.pool.execute('DELETE FROM Racers WHERE True')

    async def delete_table(self):
        await self.pool.execute('DROP TABLE Racers')
