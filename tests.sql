SELECT name FROM airports WHERE elevation BETWEEN -50 AND 50	flight_4
SELECT name FROM airports WHERE elevation BETWEEN -50 AND 50	flight_4
SELECT country FROM airports ORDER BY elevation DESC LIMIT 1	flight_4
SELECT country FROM airports ORDER BY elevation DESC LIMIT 1	flight_4
SELECT count(*) FROM airports WHERE name LIKE '%International%'	flight_4
SELECT count(*) FROM airports WHERE name LIKE '%International%'	flight_4
SELECT count(DISTINCT city) FROM airports WHERE country  =  'Greenland'	flight_4
SELECT count(DISTINCT city) FROM airports WHERE country  =  'Greenland'	flight_4
SELECT count(*) FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid WHERE T1.name  =  'American Airlines'	flight_4
SELECT count(*) FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid WHERE T1.name  =  'American Airlines'	flight_4
SELECT count(*) FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid WHERE country  =  'Canada'	flight_4
SELECT count(*) FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid WHERE country  =  'Canada'	flight_4
SELECT name ,  city ,  country FROM airports ORDER BY elevation LIMIT 1	flight_4
SELECT name ,  city ,  country FROM airports ORDER BY elevation LIMIT 1	flight_4
SELECT name ,  city ,  country FROM airports ORDER BY elevation DESC LIMIT 1	flight_4
SELECT name ,  city ,  country FROM airports ORDER BY elevation DESC LIMIT 1	flight_4
SELECT T1.name ,  T1.city ,  T2.dst_apid FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid GROUP BY T2.dst_apid ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name ,  T1.city ,  T2.dst_apid FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid GROUP BY T2.dst_apid ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name ,  T2.alid FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid GROUP BY T2.alid ORDER BY count(*) DESC LIMIT 10	flight_4
SELECT T1.name ,  T2.alid FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid GROUP BY T2.alid ORDER BY count(*) DESC LIMIT 10	flight_4
SELECT T1.name ,  T1.city ,  T2.src_apid FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid GROUP BY T2.src_apid ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name ,  T1.city ,  T2.src_apid FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid GROUP BY T2.src_apid ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT count(DISTINCT dst_apid) FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid WHERE T1.name  =  'American Airlines'	flight_4
SELECT count(DISTINCT dst_apid) FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid WHERE T1.name  =  'American Airlines'	flight_4
SELECT country FROM airlines GROUP BY country ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT country FROM airlines GROUP BY country ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT country FROM airlines WHERE active  =  'Y' GROUP BY country ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT country FROM airlines WHERE active  =  'Y' GROUP BY country ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT country ,  count(*) FROM airlines GROUP BY country ORDER BY count(*) DESC	flight_4
SELECT country ,  count(*) FROM airlines GROUP BY country ORDER BY count(*) DESC	flight_4
SELECT count(*) ,  country FROM airports GROUP BY country ORDER BY count(*) DESC	flight_4
SELECT count(*) ,  country FROM airports GROUP BY country ORDER BY count(*) DESC	flight_4
SELECT count(*) ,  city FROM airports WHERE country  =  'United States' GROUP BY city ORDER BY count(*) DESC	flight_4
SELECT count(*) ,  city FROM airports WHERE country  =  'United States' GROUP BY city ORDER BY count(*) DESC	flight_4
SELECT city FROM airports WHERE country  =  'United States' GROUP BY city HAVING count(*)  >  3	flight_4
SELECT city FROM airports WHERE country  =  'United States' GROUP BY city HAVING count(*)  >  3	flight_4
SELECT count(*) FROM (SELECT city FROM airports GROUP BY city HAVING count(*)  >  3)	flight_4
SELECT count(*) FROM (SELECT city FROM airports GROUP BY city HAVING count(*)  >  3)	flight_4
SELECT city ,  count(*) FROM airports GROUP BY city HAVING count(*)  >  1	flight_4
SELECT city ,  count(*) FROM airports GROUP BY city HAVING count(*)  >  1	flight_4
SELECT city FROM airports GROUP BY city HAVING count(*)  >  2 ORDER BY count(*)	flight_4
SELECT city FROM airports GROUP BY city HAVING count(*)  >  2 ORDER BY count(*)	flight_4
SELECT count(*) ,  T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid GROUP BY T1.name	flight_4
SELECT count(*) ,  T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid GROUP BY T1.name	flight_4
SELECT count(*) ,  T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid GROUP BY T1.name ORDER BY count(*) DESC	flight_4
SELECT count(*) ,  T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid GROUP BY T1.name ORDER BY count(*) DESC	flight_4
SELECT avg(elevation) ,  country FROM airports GROUP BY country	flight_4
SELECT avg(elevation) ,  country FROM airports GROUP BY country	flight_4
SELECT city FROM airports GROUP BY city HAVING count(*)  =  2	flight_4
SELECT city FROM airports GROUP BY city HAVING count(*)  =  2	flight_4
SELECT T1.country ,  T1.name ,  count(*) FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid GROUP BY T1.country ,  T1.name	flight_4
SELECT T1.country ,  T1.name ,  count(*) FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid GROUP BY T1.country ,  T1.name	flight_4
SELECT count(*) FROM routes AS T1 JOIN airports AS T2 ON T1.dst_apid  =  T2.apid WHERE T2.country  =  'Italy'	flight_4
SELECT count(*) FROM routes AS T1 JOIN airports AS T2 ON T1.dst_apid  =  T2.apid WHERE T2.country  =  'Italy'	flight_4
SELECT count(*) FROM routes AS T1 JOIN airports AS T2 ON T1.dst_apid  =  T2.apid JOIN airlines AS T3 ON T1.alid  =  T3.alid WHERE T2.country  =  'Italy' AND T3.name  =  'American Airlines'	flight_4
SELECT count(*) FROM routes AS T1 JOIN airports AS T2 ON T1.dst_apid  =  T2.apid JOIN airlines AS T3 ON T1.alid  =  T3.alid WHERE T2.country  =  'Italy' AND T3.name  =  'American Airlines'	flight_4
SELECT count(*) FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid WHERE T1.name  =  'John F Kennedy International Airport'	flight_4
SELECT count(*) FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid WHERE T1.name  =  'John F Kennedy International Airport'	flight_4
SELECT count(*) FROM routes WHERE dst_apid IN (SELECT apid FROM airports WHERE country  =  'Canada') AND src_apid IN (SELECT apid FROM airports WHERE country  =  'United States')	flight_4
SELECT count(*) FROM routes WHERE dst_apid IN (SELECT apid FROM airports WHERE country  =  'Canada') AND src_apid IN (SELECT apid FROM airports WHERE country  =  'United States')	flight_4
SELECT rid FROM routes WHERE dst_apid IN (SELECT apid FROM airports WHERE country  =  'United States') AND src_apid IN (SELECT apid FROM airports WHERE country  =  'United States')	flight_4
SELECT rid FROM routes WHERE dst_apid IN (SELECT apid FROM airports WHERE country  =  'United States') AND src_apid IN (SELECT apid FROM airports WHERE country  =  'United States')	flight_4
SELECT T1.name FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid GROUP BY T1.name ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name FROM airlines AS T1 JOIN routes AS T2 ON T1.alid  =  T2.alid GROUP BY T1.name ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid WHERE T1.country  =  'China' GROUP BY T1.name ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.src_apid WHERE T1.country  =  'China' GROUP BY T1.name ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid WHERE T1.country  =  'China' GROUP BY T1.name ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT T1.name FROM airports AS T1 JOIN routes AS T2 ON T1.apid  =  T2.dst_apid WHERE T1.country  =  'China' GROUP BY T1.name ORDER BY count(*) DESC LIMIT 1	flight_4
SELECT order_id FROM orders ORDER BY date_order_placed DESC LIMIT 1	tracking_orders
SELECT order_id FROM orders ORDER BY date_order_placed DESC LIMIT 1	tracking_orders
SELECT order_id ,  customer_id FROM orders ORDER BY date_order_placed LIMIT 1	tracking_orders
SELECT order_id ,  customer_id FROM orders ORDER BY date_order_placed LIMIT 1	tracking_orders
SELECT order_id FROM shipments WHERE shipment_tracking_number = "3452"	tracking_orders
SELECT order_id FROM shipments WHERE shipment_tracking_number = "3452"	tracking_orders
SELECT order_item_id FROM order_items WHERE product_id = 11	tracking_orders
SELECT order_item_id FROM order_items WHERE product_id = 11	tracking_orders
SELECT DISTINCT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "Packing"	tracking_orders
SELECT DISTINCT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "Packing"	tracking_orders
SELECT DISTINCT T1.customer_details FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "On Road"	tracking_orders
SELECT DISTINCT T1.customer_details FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "On Road"	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id  =  T2.customer_id GROUP BY T1.customer_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id  =  T2.customer_id GROUP BY T1.customer_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT T1.customer_id FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id  =  T2.customer_id GROUP BY T1.customer_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT T1.customer_id FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id  =  T2.customer_id GROUP BY T1.customer_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT T2.order_id ,  T2.order_status FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T1.customer_name = "Jeramie"	tracking_orders
SELECT T2.order_id ,  T2.order_status FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T1.customer_name = "Jeramie"	tracking_orders
SELECT T2.date_order_placed FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T1.customer_name = "Jeramie"	tracking_orders
SELECT T2.date_order_placed FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T1.customer_name = "Jeramie"	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.date_order_placed >= "2009-01-01" AND T2.date_order_placed <= "2010-01-01"	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.date_order_placed >= "2009-01-01" AND T2.date_order_placed <= "2010-01-01"	tracking_orders
SELECT DISTINCT T2.product_id FROM orders AS T1 JOIN order_items AS T2 ON T1.order_id = T2.order_id WHERE T1.date_order_placed >= "1975-01-01" AND T1.date_order_placed <= "1976-01-01"	tracking_orders
SELECT DISTINCT T2.product_id FROM orders AS T1 JOIN order_items AS T2 ON T1.order_id = T2.order_id WHERE T1.date_order_placed >= "1975-01-01" AND T1.date_order_placed <= "1976-01-01"	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "On Road" INTERSECT SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "Shipped"	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "On Road" INTERSECT SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "Shipped"	tracking_orders
SELECT T1.customer_id FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "On Road" INTERSECT SELECT T1.customer_id FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "Shipped"	tracking_orders
SELECT T1.customer_id FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "On Road" INTERSECT SELECT T1.customer_id FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id WHERE T2.order_status = "Shipped"	tracking_orders
SELECT T1.date_order_placed FROM orders AS T1 JOIN shipments AS T2 ON T1.order_id = T2.order_id WHERE T2.shipment_tracking_number = 3452	tracking_orders
SELECT T1.date_order_placed FROM orders AS T1 JOIN shipments AS T2 ON T1.order_id = T2.order_id WHERE T2.shipment_tracking_number = 3452	tracking_orders
SELECT T1.date_order_placed FROM orders AS T1 JOIN shipments AS T2 ON T1.order_id = T2.order_id WHERE T2.invoice_number = 10	tracking_orders
SELECT T1.date_order_placed FROM orders AS T1 JOIN shipments AS T2 ON T1.order_id = T2.order_id WHERE T2.invoice_number = 10	tracking_orders
SELECT count(*) ,  T3.product_id FROM orders AS T1 JOIN order_items AS T2 JOIN products AS T3 ON T1.order_id = T2.order_id AND T2.product_id = T3.product_id GROUP BY T3.product_id	tracking_orders
SELECT count(*) ,  T3.product_id FROM orders AS T1 JOIN order_items AS T2 JOIN products AS T3 ON T1.order_id = T2.order_id AND T2.product_id = T3.product_id GROUP BY T3.product_id	tracking_orders
SELECT T3.product_name ,  count(*) FROM orders AS T1 JOIN order_items AS T2 JOIN products AS T3 ON T1.order_id = T2.order_id AND T2.product_id = T3.product_id GROUP BY T3.product_id	tracking_orders
SELECT T3.product_name ,  count(*) FROM orders AS T1 JOIN order_items AS T2 JOIN products AS T3 ON T1.order_id = T2.order_id AND T2.product_id = T3.product_id GROUP BY T3.product_id	tracking_orders
SELECT order_id FROM shipments WHERE shipment_date > "2000-01-01"	tracking_orders
SELECT order_id FROM shipments WHERE shipment_date > "2000-01-01"	tracking_orders
SELECT order_id FROM shipments WHERE shipment_date  =  (SELECT max(shipment_date) FROM shipments)	tracking_orders
SELECT order_id FROM shipments WHERE shipment_date  =  (SELECT max(shipment_date) FROM shipments)	tracking_orders
SELECT DISTINCT product_name FROM products ORDER BY product_name	tracking_orders
SELECT DISTINCT product_name FROM products ORDER BY product_name	tracking_orders
SELECT DISTINCT order_id FROM orders ORDER BY date_order_placed	tracking_orders
SELECT DISTINCT order_id FROM orders ORDER BY date_order_placed	tracking_orders
SELECT T1.order_id FROM orders AS T1 JOIN order_items AS T2 ON T1.order_id = T2.order_id GROUP BY T1.order_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT T1.order_id FROM orders AS T1 JOIN order_items AS T2 ON T1.order_id = T2.order_id GROUP BY T1.order_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id GROUP BY T1.customer_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 ON T1.customer_id = T2.customer_id GROUP BY T1.customer_id ORDER BY count(*) DESC LIMIT 1	tracking_orders
SELECT invoice_number FROM invoices WHERE invoice_date < "1989-09-03" OR invoice_date > "2007-12-25"	tracking_orders
SELECT invoice_number FROM invoices WHERE invoice_date < "1989-09-03" OR invoice_date > "2007-12-25"	tracking_orders
SELECT DISTINCT invoice_details FROM invoices WHERE invoice_date < "1989-09-03" OR invoice_date > "2007-12-25"	tracking_orders
SELECT DISTINCT invoice_details FROM invoices WHERE invoice_date < "1989-09-03" OR invoice_date > "2007-12-25"	tracking_orders
SELECT T2.customer_name ,  count(*) FROM orders AS T1 JOIN customers AS T2 ON T1.customer_id = T2.customer_id GROUP BY T2.customer_id HAVING count(*)  >=  2	tracking_orders
SELECT T2.customer_name ,  count(*) FROM orders AS T1 JOIN customers AS T2 ON T1.customer_id = T2.customer_id GROUP BY T2.customer_id HAVING count(*)  >=  2	tracking_orders
SELECT T2.customer_name FROM orders AS T1 JOIN customers AS T2 ON T1.customer_id = T2.customer_id GROUP BY T2.customer_id HAVING count(*)  <=  2	tracking_orders
SELECT T2.customer_name FROM orders AS T1 JOIN customers AS T2 ON T1.customer_id = T2.customer_id GROUP BY T2.customer_id HAVING count(*)  <=  2	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 JOIN order_items AS T3 JOIN products AS T4 ON T1.customer_id = T2.customer_id AND T2.order_id = T3.order_id AND T3.product_id = T4.product_id WHERE T4.product_name = "food" GROUP BY T1.customer_id HAVING count(*)  >=  1	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 JOIN order_items AS T3 JOIN products AS T4 ON T1.customer_id = T2.customer_id AND T2.order_id = T3.order_id AND T3.product_id = T4.product_id WHERE T4.product_name = "food" GROUP BY T1.customer_id HAVING count(*)  >=  1	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 JOIN order_items AS T3 JOIN products AS T4 ON T1.customer_id = T2.customer_id AND T2.order_id = T3.order_id AND T3.product_id = T4.product_id WHERE T3.order_item_status = "Cancel" AND T4.product_name = "food" GROUP BY T1.customer_id HAVING count(*)  >=  1	tracking_orders
SELECT T1.customer_name FROM customers AS T1 JOIN orders AS T2 JOIN order_items AS T3 JOIN products AS T4 ON T1.customer_id = T2.customer_id AND T2.order_id = T3.order_id AND T3.product_id = T4.product_id WHERE T3.order_item_status = "Cancel" AND T4.product_name = "food" GROUP BY T1.customer_id HAVING count(*)  >=  1	tracking_orders
SELECT count(*) FROM architect WHERE gender  =  'female'	architecture
SELECT name ,  nationality ,  id FROM architect WHERE gender  =  'male' ORDER BY name	architecture
SELECT max(T1.length_meters) ,  T2.name FROM bridge AS T1 JOIN architect AS T2 ON T1.architect_id  =  T2.id	architecture
SELECT avg(length_feet) FROM bridge	architecture
SELECT name ,  built_year FROM mill WHERE TYPE  =  'Grondzeiler'	architecture
SELECT DISTINCT T1.name ,  T1.nationality FROM architect AS T1 JOIN mill AS t2 ON T1.id  =  T2.architect_id	architecture
SELECT name FROM mill WHERE LOCATION != 'Donceel'	architecture
SELECT DISTINCT T1.type FROM mill AS T1 JOIN architect AS t2 ON T1.architect_id  =  T2.id WHERE T2.nationality  =  'American' OR T2.nationality  =  'Canadian'	architecture
SELECT T1.id ,  T1.name FROM architect AS T1 JOIN bridge AS T2 ON T1.id  =  T2.architect_id GROUP BY T1.id HAVING count(*)  >=  3	architecture
SELECT T1.id ,  T1.name ,  T1.nationality FROM architect AS T1 JOIN mill AS T2 ON T1.id  =  T2.architect_id GROUP BY T1.id ORDER BY count(*) DESC LIMIT 1	architecture
SELECT T1.id ,  T1.name ,  T1.gender FROM architect AS T1 JOIN bridge AS T2 ON T1.id  =  T2.architect_id GROUP BY T1.id HAVING count(*)  =  2 UNION SELECT T1.id ,  T1.name ,  T1.gender FROM architect AS T1 JOIN mill AS T2 ON T1.id  =  T2.architect_id GROUP BY T1.id HAVING count(*)  =  1	architecture
SELECT LOCATION FROM bridge WHERE name  =  'Kolob Arch' OR name  =  'Rainbow Bridge'	architecture
SELECT name FROM mill WHERE name LIKE '%Moulin%'	architecture
SELECT DISTINCT T1.name FROM mill AS T1 JOIN architect AS t2 ON T1.architect_id  =  T2.id JOIN bridge AS T3 ON T3.architect_id  =  T2.id WHERE T3.length_meters  >  80	architecture
SELECT TYPE ,  count(*) FROM mill GROUP BY TYPE ORDER BY count(*) DESC LIMIT 1	architecture
SELECT count(*) FROM architect WHERE id NOT IN ( SELECT architect_id FROM mill WHERE built_year  <  1850 );	architecture
SELECT t1.name FROM bridge AS t1 JOIN architect AS t2 ON t1.architect_id  =  t2.id WHERE t2.nationality  =  'American' ORDER BY t1.length_feet	architecture
SELECT count(*) FROM book_club	culture_company
SELECT count(*) FROM book_club	culture_company
SELECT book_title ,  author_or_editor FROM book_club WHERE YEAR  >  1989	culture_company
SELECT book_title ,  author_or_editor FROM book_club WHERE YEAR  >  1989	culture_company
SELECT DISTINCT publisher FROM book_club	culture_company
SELECT DISTINCT publisher FROM book_club	culture_company
SELECT YEAR ,  book_title ,  publisher FROM book_club ORDER BY YEAR DESC	culture_company
SELECT YEAR ,  book_title ,  publisher FROM book_club ORDER BY YEAR DESC	culture_company
SELECT publisher ,  count(*) FROM book_club GROUP BY publisher	culture_company
SELECT publisher ,  count(*) FROM book_club GROUP BY publisher	culture_company
SELECT publisher FROM book_club GROUP BY publisher ORDER BY count(*) DESC LIMIT 1	culture_company
SELECT publisher FROM book_club GROUP BY publisher ORDER BY count(*) DESC LIMIT 1	culture_company
SELECT category ,  count(*) FROM book_club GROUP BY category	culture_company
SELECT category ,  count(*) FROM book_club GROUP BY category	culture_company
SELECT category FROM book_club WHERE YEAR  >  1989 GROUP BY category HAVING count(*)  >=  2	culture_company
SELECT category FROM book_club WHERE YEAR  >  1989 GROUP BY category HAVING count(*)  >=  2	culture_company
SELECT publisher FROM book_club WHERE YEAR  =  1989 INTERSECT SELECT publisher FROM book_club WHERE YEAR  =  1990	culture_company
SELECT publisher FROM book_club WHERE YEAR  =  1989 INTERSECT SELECT publisher FROM book_club WHERE YEAR  =  1990	culture_company
SELECT publisher FROM book_club EXCEPT SELECT publisher FROM book_club WHERE YEAR  =  1989	culture_company
SELECT publisher FROM book_club EXCEPT SELECT publisher FROM book_club WHERE YEAR  =  1989	culture_company
SELECT title ,  YEAR ,  director FROM movie ORDER BY budget_million	culture_company
SELECT title ,  YEAR ,  director FROM movie ORDER BY budget_million	culture_company
SELECT COUNT (DISTINCT director) FROM movie	culture_company
SELECT COUNT (DISTINCT director) FROM movie	culture_company
SELECT title ,  director FROM movie WHERE YEAR  <=  2000 ORDER BY gross_worldwide DESC LIMIT 1	culture_company
SELECT title ,  director FROM movie WHERE YEAR  <=  2000 ORDER BY gross_worldwide DESC LIMIT 1	culture_company
SELECT director FROM movie WHERE YEAR  =  2000 INTERSECT SELECT director FROM movie WHERE YEAR  =  1999	culture_company
SELECT director FROM movie WHERE YEAR  =  2000 INTERSECT SELECT director FROM movie WHERE YEAR  =  1999	culture_company
SELECT director FROM movie WHERE YEAR  =  1999 OR YEAR  =  2000	culture_company
SELECT director FROM movie WHERE YEAR  =  1999 OR YEAR  =  2000	culture_company
SELECT avg(budget_million) ,  max(budget_million) ,  min(budget_million) FROM movie WHERE YEAR  <  2000	culture_company
SELECT avg(budget_million) ,  max(budget_million) ,  min(budget_million) FROM movie WHERE YEAR  <  2000	culture_company
SELECT T1.company_name FROM culture_company AS T1 JOIN book_club AS T2 ON T1.book_club_id  =  T2.book_club_id WHERE T2.publisher  =  'Alyson'	culture_company
SELECT T1.company_name FROM culture_company AS T1 JOIN book_club AS T2 ON T1.book_club_id  =  T2.book_club_id WHERE T2.publisher  =  'Alyson'	culture_company
SELECT T1.title ,  T3.book_title FROM movie AS T1 JOIN culture_company AS T2 ON T1.movie_id  =  T2.movie_id JOIN book_club AS T3 ON T3.book_club_id  =  T2.book_club_id WHERE T2.incorporated_in  =  'China'	culture_company
SELECT T1.title ,  T3.book_title FROM movie AS T1 JOIN culture_company AS T2 ON T1.movie_id  =  T2.movie_id JOIN book_club AS T3 ON T3.book_club_id  =  T2.book_club_id WHERE T2.incorporated_in  =  'China'	culture_company
SELECT T2.company_name FROM movie AS T1 JOIN culture_company AS T2 ON T1.movie_id  =  T2.movie_id WHERE T1.year  =  1999	culture_company
SELECT T2.company_name FROM movie AS T1 JOIN culture_company AS T2 ON T1.movie_id  =  T2.movie_id WHERE T1.year  =  1999	culture_company
