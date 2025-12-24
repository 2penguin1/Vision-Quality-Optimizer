from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings
from ssl import CERT_NONE

# MongoDB client and database
client: AsyncIOMotorClient = None
database = None


async def connect_to_db():
    """Connect to MongoDB"""
    global client, database
    try:
        client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tlsAllowInvalidCertificates=True
        )
        database = client[settings.MONGODB_DB_NAME]
        # Verify connection
        await database.command("ping")
        print(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


async def disconnect_from_db():
    """Disconnect from MongoDB"""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")


def get_db():
    """Get the database instance"""
    return database
