SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `flask` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `flask`;

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES
(0, 'ezheleznikova', 'GeZaLo02', 'elena744zh@yandex.ru'),
(1, 'pzheleznikova', 'GeZaLo02', 'pzheleznikova@gmail.com');

DROP TABLE IF EXISTS `places`;
CREATE TABLE `places` (
  `id_places` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `link` varchar(100) NOT NULL,
  `image` varchar(50) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `rating` float DEFAULT NULL,
  `avg_emotion` enum('positive','negative','neutral') DEFAULT NULL,
  `City` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `places` (`id_places`, `name`, `link`, `image`, `description`, `rating`, `avg_emotion`, `City`) VALUES
(1, 'Ботанический сад', 'http://192.168.0.146:81/img', 'IMG_20220512_123059.jpg', 'Ботанический сад Петра Великого — один из старейших ботанических садов России, расположенный на Аптекарском острове в Санкт-Петербурге. Занимает территорию между Аптекарской набережной Большой Невки, набережной Карповки, Аптекарским проспектом и улицей Профессора Попова.', 0.961544, 'negative', 'Санкт-Петербург'),
(2, 'Эрмитаж', 'https://www.hermitagemuseum.org/', 'ermitazh.jpg', 'Российский государственный музей изобразительного и декоративно-прикладного искусств, одно из крупнейших в мире учреждений подобного рода.', 0.996186, 'positive', 'Санкт-Петербург'),
(3, 'Мурманская областная филармония', 'https://murmansound.ru/', 'murmansk_philharmonic.jpeg', 'Концертный зал филармонии имеет классический вид, выполнен в светлых тонах. Зал имеет конфигурацию амфитеатра: каждый последующий ряд расположен выше предыдущего. Концертный зал в здании расположен в 2-двух уровнях, на 3-4 этажах. Входы и выходы в концертный зал находятся на 3 этаже: слева и по центру зала, и на 4 этаже: слева и справа зала. Посадочных мест на 558 зрителей. Часть первого ряда предназначена для зрителей на колясках.', NULL, NULL, 'Мурманск');

DROP TABLE IF EXISTS `reviews`;
CREATE TABLE `reviews` (
  `id_review` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `review` varchar(1000) NOT NULL,
  `id_places` int(11) NOT NULL,
  `publication_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `emotion` enum('negative','positive','neutral') NOT NULL,
  `rating` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

INSERT INTO `reviews` (`id_review`, `id_user`, `review`, `id_places`, `publication_date`, `emotion`, `rating`) VALUES
(1, 1, 'Нам очень понравилось! Были семьёй с 4м ребёнком, февральские праздники, людей было достаточно много, но это не помешало получить удовольствие от прогулки. Была выставка сирени, оранжерея - отдельное удовольствие✨ особенно когда за окном зима и снег, а ты будто во влажных тропиках. Кайф. Сходили в музей, интересная экспозиция (правда, здание в плачевном состоянии).', 1, '2022-03-21', 'positive', 0.430157),
(2, 3, 'Великолепно! Очень красиво!', 1, '2023-03-14', 'positive', 1),
(3, 0, 'Ботанический сад всегда прекрасен. А сейчас ещё и азалии! Нам повезло, мы были в будний день, спокойно купили билеты, прогулялись по саду, съели вкусный штрудель в кафе на территории парка. И конечно, субтропический маршрут доставил много приятных минут. Экскурсовод рассказывала интересно. Растения ухоженные. Получили массу удовольствия', 1, '2022-03-21', 'negative', 0.370235),
(102, 1, 'Хорошее место:)', 2, '2023-04-06', 'positive', 0.996186),
(103, 0, 'Нормально.', 2, '2023-04-06', 'neutral', 0.787941);
DROP TRIGGER IF EXISTS `update_rating`;
DELIMITER $$
CREATE TRIGGER `update_rating` AFTER INSERT ON `reviews` FOR EACH ROW BEGIN
	UPDATE places
	SET rating = (
		SELECT MAX(avg_rating) FROM (
			SELECT id_places, emotion, AVG(rating) AS avg_rating FROM reviews WHERE id_places = NEW.id_places GROUP BY emotion
		) AS max_rating
        WHERE max_rating.emotion = emotion
	)
    WHERE id_places = NEW.id_places;
    
	UPDATE places
	SET avg_emotion = (
		SELECT emotion FROM (
			SELECT id_places, emotion, AVG(rating) AS avg_rating FROM reviews WHERE id_places = NEW.id_places GROUP BY emotion ORDER BY avg_rating DESC LIMIT 1
		) AS max_rating
        WHERE max_rating.emotion = emotion
	)
	WHERE id_places = NEW.id_places;
END
$$
DELIMITER ;


ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `places`
  ADD PRIMARY KEY (`id_places`);

ALTER TABLE `reviews`
  ADD UNIQUE KEY `id_review` (`id_review`,`id_places`),
  ADD KEY `id_places` (`id_places`);


ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

ALTER TABLE `places`
  MODIFY `id_places` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `reviews`
  MODIFY `id_review` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=140;


ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`id_places`) REFERENCES `places` (`id_places`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
