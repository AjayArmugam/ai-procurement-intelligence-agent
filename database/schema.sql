-- PostgreSQL schema placeholder for procurement data.
CREATE TABLE vendors(
    vendor_id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invoices(
    invoice_id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    vendor_id INTEGER REFERENCES vendors(vendor_id),

    amount DECIMAL(12,2),

    invoice_date DATE,
    due_date DATE,

    status VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_orders(
    po_id SERIAL PRIMARY KEY,

    po_number VARCHAR(50) UNIQUE,

    vendor_id INTEGER REFERENCES vendors(vendor_id),

    amount DECIMAL(12,2),

    po_date DATE,

    status VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments(
    payment_id SERIAL PRIMARY KEY,

    invoice_id INTEGER REFERENCES invoices(invoice_id),

    amount DECIMAL(12,2),

    payment_date DATE,

    payment_status VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);