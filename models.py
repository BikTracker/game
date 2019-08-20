import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Document, Instance, fields

try:
    from money_bot import local_config as config
except ImportError:
    from . import example_config as config

db = AsyncIOMotorClient(config.DB_HOST)[config.DB_NAME]
instance = Instance(db)


@instance.register
class User(Document):
    money = fields.IntegerField(default=0)


asyncio.get_event_loop().create_task(main())
