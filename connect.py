import traceback
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='hfp_db',
            user='techa',  # Default MySQL username in XAMPP
            password='Techa.Tech500'   # Default MySQL password in XAMPP is usually empty
        )
        if conn.is_connected():
            print("Successfully connected to MySQL database!")
        return conn
    except Error as e:
        print(f"Error: {e}")
    return None

get_db_connection()



def create_tables():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()

            # Create tables with foreign key constraints
            cur.execute("""
                CREATE TABLE user_registration_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE,
                    name VARCHAR(250),
                    phone VARCHAR(250)
                );
            """)

            cur.execute("""
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    is_approved BOOLEAN DEFAULT FALSE,
                    profile_image TEXT,
                    suspended BOOLEAN DEFAULT FALSE,
                    activation_token TEXT,
                    is_activated BOOLEAN DEFAULT FALSE,
                    registration_request_id INT,
                    name VARCHAR(250),
                    phone VARCHAR(250),
                    FOREIGN KEY (registration_request_id) REFERENCES user_registration_requests(id) ON DELETE CASCADE
                );
            """)

            cur.execute("""
                CREATE TABLE business_registration_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    business_name VARCHAR(100) NOT NULL,
                    shop_no VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(20),
                    description TEXT NOT NULL,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INT,
                    category VARCHAR(50) NOT NULL,
                    block_num VARCHAR(50),
                    email VARCHAR(100),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cur.execute("""
                CREATE TABLE businesses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    owner_id INT,
                    business_name VARCHAR(100) NOT NULL,
                    shop_no VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(20) NOT NULL,
                    description TEXT NOT NULL,
                    is_subscribed BOOLEAN DEFAULT FALSE,
                    media_type ENUM('image', 'video'),
                    media_url TEXT,
                    category VARCHAR(50) NOT NULL,
                    block_num VARCHAR(50),
                    email VARCHAR(100),
                    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cur.execute("""
                CREATE TABLE images_videos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    business_id INT,
                    media_type ENUM('image', 'video'),
                    media_url TEXT NOT NULL,
                    FOREIGN KEY (business_id) REFERENCES businesses(id)
                );
            """)

            cur.execute("""
                CREATE TABLE categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    category_name VARCHAR(255) UNIQUE NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE business_categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    business_id INT,
                    category_id INT,
                    FOREIGN KEY (business_id) REFERENCES businesses(id),
                    FOREIGN KEY (category_id) REFERENCES categories(id),
                    UNIQUE (business_id, category_id)
                );
            """)

            cur.execute("""
                CREATE TABLE admin (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    profile_pic VARCHAR(255)
                );
            """)

            cur.execute("""
                CREATE TABLE subscription_plans (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    plan_name VARCHAR(50) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    duration INT NOT NULL,
                    UNIQUE (plan_name, duration)
                );
            """)           
            
            cur.execute("""INSERT INTO subscription_plans (plan_name, amount, duration) VALUES 
                        ('Monthly', 10000, 1), 
                        ('Yearly', 85000, 12)
                        """)    

            cur.execute("""
                CREATE TABLE subscriptions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    business_id INT,
                    subscription_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status ENUM('pending', 'confirmed'),
                    plan_id INT,
                    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE,
                    FOREIGN KEY (plan_id) REFERENCES subscription_plans(id)
                );
            """)

            cur.execute("""
                CREATE TABLE payments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    subscription_id INT,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    amount DECIMAL(10, 2) NOT NULL,
                    payment_status ENUM('pending', 'completed'),
                    payment_method VARCHAR(50),
                    FOREIGN KEY (subscription_id) REFERENCES subscriptions(id) ON DELETE CASCADE
                );
            """)

            cur.execute("""
                CREATE TABLE claim_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    business_id INT,
                    user_id INT,
                    phone_number VARCHAR(255),
                    email VARCHAR(255),
                    category VARCHAR(255),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reviewed BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (business_id) REFERENCES businesses(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)

            print("Database tables created successfully")
            conn.commit()

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cur.close()
            conn.close()
    else:
        print("Could not open connection to the database")

# Call the function to initialize the database
create_tables()



"""#SQL COMMAND TO DELETE A USER FROM TABLE and also to DELETE A TABLE THAT IS REFERENCE TO OTHERS TABLESBELOW:
DELETE FROM tablename WHERE id = 5;

DROP TABLE IF EXISTS subscription_plans CASCADE;

"""







