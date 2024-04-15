import asyncio, aiosqlite


class DataBase:
    def __init__(self, file):
        self.file = file

    async def is_user_in_db(self, id):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(f"SELECT * FROM user WHERE id='{id}'")
            data = await cursor.fetchone()
            await cursor.close()

            try:
                len(data)
                return True
            except TypeError:
                return False
    
    async def new_user(self, id):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(f"INSERT INTO user (id) VALUES ({id})")
            await cursor.close()
            await db.commit()

    async def genre_list(self):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(f"SELECT value FROM service WHERE key='genre_list'")

            data = await cursor.fetchone()
            data = data[0].split(',')
            
            result = []
            for object in data:
                result.append(object)
            await cursor.close()

            return result
    
    async def add_new_book(self, name, author, adder, adder_id, genre, description):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute('INSERT INTO book (name, author, adder, adder_id, genre, description)' +
                                       f'VALUES ("{name}", "{author}", "{adder}", {adder_id}, "{genre}", "{description}")')
            await cursor.close()
            await db.commit()

    async def get_book_list(self):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(f"SELECT name, author, in_id, genre FROM book")

            data = await cursor.fetchall()

            return data
        
    async def get_info_by_book_id(self, book_id):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(f"SELECT author, adder, adder_id, genre, description FROM book WHERE in_id = {book_id}")

            data = await cursor.fetchall()

            return data
        
    async def delete_book(self, book_id):
        async with aiosqlite.connect(self.file) as db:
            cursor = await db.execute(f'DELETE FROM book WHERE in_id = {book_id}')
            await cursor.close()
            await db.commit()
