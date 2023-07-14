
CREATE TABLE reservations(
reservation_number INT NOT NULL,
room_number INT NOT NULL,
guest_id INT NOT NULL,
arrival_date DATE NOT NULL,
departure_date DATE NOT NULL,
paid ENUM('YES', 'NO') NOT NULL,
PRIMARY KEY (reservation_number)
);
