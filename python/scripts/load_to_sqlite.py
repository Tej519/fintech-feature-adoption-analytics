"""
Load CSV data into SQLite - No MySQL, No passwords!
"""

import sqlite3
import pandas as pd
import os

def load_data():
    """Load CSV data into SQLite"""
    
    print("=" * 60)
    print("LOADING DATA TO SQLITE")
    print("=" * 60)
    
    # Check if CSV files exist
    if not os.path.exists('data/raw/users_raw.csv'):
        print("❌ users_raw.csv not found!")
        print("   Run: python python/scripts/generate_dataset.py")
        return
    
    if not os.path.exists('data/raw/events_raw.csv'):
        print("❌ events_raw.csv not found!")
        print("   Run: python python/scripts/generate_dataset.py")
        return
    
    # Database path
    db_path = 'data/processed/fintech.db'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    print("\n📊 Reading CSV files...")
    users_df = pd.read_csv('data/raw/users_raw.csv')
    events_df = pd.read_csv('data/raw/events_raw.csv')
    
    print(f"✅ Loaded {len(users_df):,} users")
    print(f"✅ Loaded {len(events_df):,} events")
    
    # Connect to SQLite (this creates the file)
    print("\n💾 Creating SQLite database...")
    conn = sqlite3.connect(db_path)
    
    # Write to SQLite
    print("📤 Writing users to database...")
    users_df.to_sql('users', conn, if_exists='replace', index=False)
    
    print("📤 Writing events to database...")
    events_df.to_sql('events', conn, if_exists='replace', index=False)
    
    # Create indexes for performance
    print("🔍 Creating indexes...")
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_kyc ON users(kyc_completed)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_autopay ON users(autopay_adopted)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_device ON users(device_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
    conn.commit()
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM events")
    event_count = cursor.fetchone()[0]
    
    # Show sample data
    cursor.execute("SELECT user_id, city, device_type, features_adopted, transaction_count FROM users LIMIT 3")
    sample_users = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATA LOADED SUCCESSFULLY!")
    print("=" * 60)
    print(f"   Database: {db_path}")
    print(f"   Users: {user_count:,}")
    print(f"   Events: {event_count:,}")
    print("\n📋 Sample Users:")
    for row in sample_users:
        print(f"   {row[0]}, {row[1]}, {row[2]}, Features: {row[3]}, Txns: {row[4]}")
    
    print("\n🚀 Next steps:")
    print("   1. Create views: sqlite3 data/processed/fintech.db < sql/sqlite_metrics_views.sql")
    print("   2. Test: sqlite3 data/processed/fintech.db 'SELECT * FROM v_activation_metrics;'")
    print("   3. Connect Power BI to SQLite")

if __name__ == "__main__":
    load_data()