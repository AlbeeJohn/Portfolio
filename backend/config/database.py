from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class DatabaseManager:
    """MongoDB connection manager with optimization"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None
        
    async def connect(self):
        """Connect to MongoDB with optimized settings"""
        try:
            mongo_url = os.environ['MONGO_URL']
            db_name = os.environ['DB_NAME']
            
            # Connection with optimization settings
            self.client = AsyncIOMotorClient(
                mongo_url,
                maxPoolSize=10,          # Maximum connections in pool
                minPoolSize=1,           # Minimum connections in pool
                maxIdleTimeMS=30000,     # Close connections after 30s idle
                waitQueueTimeoutMS=5000, # Wait max 5s for connection
                serverSelectionTimeoutMS=5000,  # Server selection timeout
                connectTimeoutMS=10000,  # Connection timeout
                socketTimeoutMS=20000,   # Socket timeout
            )
            
            self.database = self.client[db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB successfully")
            
            # Create indexes for better performance
            await self.create_indexes()
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    async def create_indexes(self):
        """Create database indexes for better query performance"""
        try:
            # Portfolio collection indexes
            await self.database.portfolio.create_index("id")
            await self.database.portfolio.create_index("updated_at")
            
            # Contact messages indexes
            await self.database.contact_messages.create_index("id")
            await self.database.contact_messages.create_index("created_at")
            await self.database.contact_messages.create_index("read")
            await self.database.contact_messages.create_index([
                ("created_at", -1),  # Descending order for recent first
                ("read", 1)
            ])
            
            logger.info("✅ Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to create indexes: {e}")
    
    async def disconnect(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("✅ Disconnected from MongoDB")
    
    def get_database(self):
        """Get database instance"""
        if self.database is None:
            raise RuntimeError("Database not connected")
        return self.database

# Global database manager
db_manager = DatabaseManager()

async def get_db():
    """Dependency for getting database"""
    return db_manager.get_database()