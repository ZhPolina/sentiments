TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER `update_rating` AFTER INSERT ON `reviews` FOR EACH ROW BEGIN\n	UPDATE places\n	SET rating = (\n		SELECT MAX(avg_rating) FROM (\n			SELECT id_places, emotion, AVG(rating) AS avg_rating FROM reviews WHERE id_places = NEW.id_places GROUP BY emotion\n		) AS max_rating\n        WHERE max_rating.emotion = emotion\n	)\n    WHERE id_places = NEW.id_places;\n    \n	UPDATE places\n	SET avg_emotion = (\n		SELECT emotion FROM (\n			SELECT id_places, emotion, AVG(rating) AS avg_rating FROM reviews WHERE id_places = NEW.id_places GROUP BY emotion ORDER BY avg_rating DESC LIMIT 1\n		) AS max_rating\n        WHERE max_rating.emotion = emotion\n	)\n	WHERE id_places = NEW.id_places;\nEND'
sql_modes=524288
definers='root@localhost'
client_cs_names='utf8mb4'
connection_cl_names='utf8mb4_general_ci'
db_cl_names='utf8_general_ci'
created=168098780239
