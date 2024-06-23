from config import Config, Txt
from motor.motor_asyncio import AsyncIOMotorClient


class Database:

    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        

    def new_user(self, id):
        return dict(id=id)

    async def add_user(self, id):
        if not await self.is_user_exist(id):
            user = self.new_user(int(id))
            await self.col.insert_one(user)

    async def get_user(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user or None
   
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
      
    
    
       
db = Database(Config.DB_URL, Config.DB_NAME)



