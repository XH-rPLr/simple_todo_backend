import motor.motor_asyncio

# Connect to MongoDB
# URL need to be stored on env variable
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')