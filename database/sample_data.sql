INSERT INTO vendors
(vendor_name,email,phone,address)
VALUES
('ABC Ltd','abc@gmail.com','9999999991','Hyderabad'),
('MedSupply Inc','med@gmail.com','9999999992','Chennai'),
('Global Tech','tech@gmail.com','9999999993','Bangalore');


INSERT INTO invoices
(invoice_number,vendor_id,amount,invoice_date,due_date,status)
VALUES
('INV-1001',1,12000,'2026-05-01','2026-05-15','PAID'),
('INV-1002',1,18000,'2026-05-05','2026-05-20','UNPAID'),
('INV-1003',2,45000,'2026-05-10','2026-05-25','UNPAID'),
('INV-1004',3,22000,'2026-05-12','2026-05-28','PAID');


INSERT INTO purchase_orders
(po_number,vendor_id,amount,po_date,status)
VALUES
('PO-2001',1,50000,'2026-04-20','APPROVED'),
('PO-2002',2,75000,'2026-04-22','APPROVED'),
('PO-2003',3,30000,'2026-04-25','PENDING');


INSERT INTO payments
(invoice_id,amount,payment_date,payment_status)
VALUES
(1,12000,'2026-05-14','COMPLETED'),
(4,22000,'2026-05-27','COMPLETED');