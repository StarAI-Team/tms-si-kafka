CREATE TABLE IF NOT EXISTS transporter (
    user_id TEXT PRIMARY KEY,
    company_email TEXT UNIQUE NOT NULL,
    company_location TEXT NOT NULL,
    company_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    id_number TEXT UNIQUE NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,  
    registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registration_status TEXT DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS transporter_account_information (
    user_id TEXT PRIMARY KEY,
    account_name TEXT NOT NULL,
    account_number TEXT UNIQUE NOT NULL,
    bank_name TEXT NOT NULL,
    company_contact TEXT NOT NULL,
    directorship TEXT NOT NULL,
    proof_of_current_address TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES transporter(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transporter_documentation (
    user_id TEXT PRIMARY KEY,
    certificate_of_incorporation TEXT NOT NULL,
    operators_expiry DATE NOT NULL,
    operators_licence TEXT NOT NULL,
    permit_expiry DATE NOT NULL,
    permits TEXT NOT NULL,
    tax_clearance TEXT NOT NULL,
    tax_expiry DATE NOT NULL,
    tracking_licence TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES transporter(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transporter_fleet (
    user_id TEXT PRIMARY KEY,
    certificate_of_fitness TEXT NOT NULL,
    num_of_trucks TEXT NOT NULL,
    number_of_trucks INT NOT NULL,
    reg_books TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES transporter(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transporter_profile (
    user_id TEXT PRIMARY KEY,
    profile_picture TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES transporter(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shipper (
    user_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    id_number TEXT NOT NULL,
    company_name TEXT NOT NULL,
    company_location TEXT NOT NULL,
    company_email TEXT NOT NULL,
    registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    registration_status TEXT DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS shipper_company_details (
    user_id TEXT PRIMARY KEY,
    company_contact TEXT NOT NULL,
    bank_name TEXT NOT NULL,
    account_name TEXT NOT NULL,
    account_number TEXT NOT NULL,
    directorship TEXT NOT NULL,
    proof_of_current_address TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES shipper(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shipper_documentation (
    user_id TEXT PRIMARY KEY,
    tax_expiry DATE NOT NULL,
    certificate_of_incorporation TEXT NOT NULL,
    tax_clearance TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES shipper(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shipper_profile (
    user_id TEXT PRIMARY KEY,
    profile_picture TEXT NOT NULL,
    password TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES shipper(user_id) ON DELETE CASCADE
);

-- Table: loads
CREATE TABLE IF NOT EXISTS loads (
    user_id TEXT PRIMARY KEY,
    load_name VARCHAR(255) NOT NULL,
    stars INTEGER,
    price DECIMAL(10, 2),
    route TEXT,
    status VARCHAR(50),
    perfect_match BOOLEAN,
    private BOOLEAN,
    transport_date DATE,
    rate DECIMAL(10, 2),
    quantity INTEGER,
    load_type VARCHAR(50)
);

-- Table: booked_trucks
CREATE TABLE IF NOT EXISTS booked_trucks (
    user_id TEXT PRIMARY KEY,
    truck_reg VARCHAR(20) UNIQUE NOT NULL,
    truck_type VARCHAR(50),
    trailer1_reg VARCHAR(20),
    trailer2_reg VARCHAR(20),
    driver_name VARCHAR(100) NOT NULL,
    id_number VARCHAR(20) UNIQUE NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    license_number VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL
);

-- Table: load_pool
CREATE TABLE IF NOT EXISTS load_pool (
    user_id TEXT PRIMARY KEY,
    load_id TEXT NOT NULL,
    route TEXT NOT NULL,
    transport_date DATE NOT NULL,
    rate DECIMAL(10, 2),
    load_type VARCHAR(50)
);

-- Table: documents
CREATE TABLE IF NOT EXISTS documents (
    user_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL
);

-- Table: load_history
CREATE TABLE IF NOT EXISTS load_history (
    user_id TEXT PRIMARY KEY,
    load_id INTEGER REFERENCES loads(user_id),
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    transport_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL
);
