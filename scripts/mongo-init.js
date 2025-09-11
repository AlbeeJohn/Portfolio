// MongoDB initialization script
print('Starting MongoDB initialization...');

// Switch to portfolio database
db = db.getSiblingDB('portfolio_db');

// Create indexes for better performance
print('Creating indexes...');

// Portfolio collection indexes
db.portfolio.createIndex({ "id": 1 }, { unique: true });
db.portfolio.createIndex({ "updated_at": -1 });
db.portfolio.createIndex({ "personal.name": 1 });

// Contact messages indexes
db.contact_messages.createIndex({ "id": 1 }, { unique: true });
db.contact_messages.createIndex({ "created_at": -1 });
db.contact_messages.createIndex({ "read": 1 });
db.contact_messages.createIndex({ "email": 1 });

// Create compound indexes
db.contact_messages.createIndex({ "created_at": -1, "read": 1 });

print('Indexes created successfully');

// Create default admin user (optional)
// db.users.insertOne({
//   username: 'admin',
//   email: 'admin@portfolio.com',
//   role: 'admin',
//   created_at: new Date()
// });

print('MongoDB initialization completed!');