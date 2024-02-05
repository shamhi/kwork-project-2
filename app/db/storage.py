import aiosqlite


class Database:
    def __init__(self, connection: aiosqlite.Connection):
        self.db: aiosqlite.Connection = connection

    async def create_table(self):
        await self.db.execute(sql="""CREATE TABLE IF NOT EXISTS users(
                id BIGINT,
                referral BIGINT,
                money BIGINT
        )""")
        await self.db.commit()

    async def check_user(self, user_id):
        user = await self.db.execute(sql="SELECT id FROM users WHERE id=?", parameters=(user_id,))
        data = await user.fetchone()

        return False if not data else True

    async def add_user(self, user_id):
        if not await self.check_user(user_id=user_id):
            await self.db.execute(sql="INSERT INTO users VALUES (?, ?, ?)", parameters=(user_id, 0, 0))
            await self.db.commit()

    async def add_referral(self, user_id, referral):
        await self.db.execute(sql="UPDATE users SET referral=? WHERE id=?", parameters=(referral, user_id))
        await self.db.commit()

    async def add_money(self, user_id, money):
        await self.db.execute(sql="UPDATE users SET money=money+? WHERE id=?", parameters=(money, user_id))
        await self.db.commit()

    async def minus_money(self, user_id, money):
        await self.db.execute(sql="UPDATE users SET money=money-? WHERE id=?", parameters=(money, user_id))
        await self.db.commit()

    async def get_referral(self, user_id):
        user = await self.db.execute(sql="SELECT referral FROM users WHERE id=?", parameters=(user_id,))
        data = await user.fetchone()

        if not data:
            return None

        return data[0]

    async def get_money(self, user_id):
        user = await self.db.execute(sql="SELECT money FROM users WHERE id=?", parameters=(user_id,))
        data = await user.fetchone()

        if not data:
            return None

        return data[0]
