-- task1

-- SELECT category_id, COUNT(film_id)
-- FROM film_category
-- GROUP BY category_id
-- ORDER BY COUNT(film_id) DESC;

-- task2

-- SELECT first_name, last_name, SUM(rental_duration)
-- FROM film
-- JOIN film_actor fa on film.film_id = fa.film_id
-- JOIN actor a on a.actor_id = fa.actor_id
-- GROUP BY first_name, last_name
-- ORDER BY SUM(rental_duration) DESC
-- LIMIT 10;

-- task3

-- SELECT name , SUM(amount)
-- FROM category
-- JOIN film_category fc on category.category_id = fc.category_id
-- JOIN film f on f.film_id = fc.film_id
-- JOIN inventory i on f.film_id = i.film_id
-- JOIN rental r on i.inventory_id = r.inventory_id
-- JOIN payment p on r.rental_id =   p.rental_id
-- GROUP BY category.name
-- ORDER BY SUM(amount) DESC
-- LIMIT 1;

-- task4

-- SELECT title
-- FROM film
-- WHERE film_id  <>ALL (SELECT film_id FROM inventory)
-- GROUP BY title
-- ORDER BY title;

-- task5

-- WITH temp_table AS
--     (SELECT first_name, last_name, COUNT(f.film_id) as film_counter
--     FROM actor
--     JOIN film_actor fa on actor.actor_id = fa.actor_id
--     JOIN film f on f.film_id = fa.film_id
--     JOIN film_category fc on f.film_id = fc.film_id
--     JOIN category c on c.category_id = fc.category_id
--     WHERE c.name = 'Children'
--     GROUP BY first_name, last_name
--     ORDER BY COUNT(f.film_id) DESC)
-- SELECT *
-- FROM temp_table
-- WHERE film_counter in (
--     SELECT film_counter
--     FROM temp_table
--     ORDER BY film_counter DESC
--     LIMIT 3)
-- ORDER BY film_counter DESC, first_name, last_name;

-- task6 haven't done yet

-- SELECT address_id,
-- CASE active
--     WHEN 1 THEN COUNT(active)
--     WHEN 0 THEN COUNT(active)
-- END AS counter
-- FROM customer
-- GROUP BY address_id, active

-- CASE active
--     WHEN 1 THEN aactive+1
--     WHEN 0 THEN inactive
-- END AS counter

-- WITH temp_table AS
--     (SELECT city.city
--     FROM city
--     JOIN address a on city.city_id = a.city_id
--     JOIN customer c on a.address_id = c.address_id
--     GROUP BY city.city
--     ORDER BY city)
-- ALTER TABLE temp_table ADD COLUMN aactive INT
-- ALTER TABLE temp_table ADD COLUMN inactive INT


-- SELECT city.city, COUNT(active) AS active1, COUNT(active) AS active0
-- FROM city
-- JOIN address a ON city.city_id = a.city_id
-- JOIN customer c ON a.address_id = c.address_id
-- WHERE active = 1
-- GROUP BY city.city
-- ORDER BY active1 DESC;
--

-- task7

-- (SELECT name, SUM(rental_duration)
-- FROM category
-- JOIN film_category fc on category.category_id = fc.category_id
-- JOIN film f on f.film_id = fc.film_id
-- JOIN inventory i on f.film_id = i.film_id
-- JOIN rental r on i.inventory_id = r.inventory_id
-- JOIN customer c on c.customer_id = r.customer_id
-- JOIN address a on a.address_id = c.address_id
-- JOIN city c2 on c2.city_id = a.city_id
-- WHERE c2.city LIKE 'a%'
-- GROUP BY name
-- ORDER BY SUM(rental_duration) DESC
-- LIMIT 1)
-- UNION ALL
-- (SELECT name, SUM(rental_duration)
-- FROM category
-- JOIN film_category fc on category.category_id = fc.category_id
-- JOIN film f on f.film_id = fc.film_id
-- JOIN inventory i on f.film_id = i.film_id
-- JOIN rental r on i.inventory_id = r.inventory_id
-- JOIN customer c on c.customer_id = r.customer_id
-- JOIN address a on a.address_id = c.address_id
-- JOIN city c2 on c2.city_id = a.city_id
-- WHERE c2.city LIKE '%-%'
-- GROUP BY name
-- ORDER BY SUM(rental_duration) DESC
-- LIMIT 1);
