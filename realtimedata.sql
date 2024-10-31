
USE manhdx;

CREATE TABLE realtimedata (
	    id INT AUTO_INCREMENT PRIMARY KEY,
	    timestamp VARCHAR(18),
	    light_level FLOAT,
	    humidity FLOAT,
	    temperature FLOAT
);

USE manhdx;

INSERT INTO realtimedata (timestamp, light_level, humidity, temperature) VALUES
('2024-10-29 17:41', 41, 85, 28),
('2024-10-29 17:42', 41, 84, 28),
('2024-10-29 17:43', 40, 85, 28),
('2024-10-29 17:44', 40, 84, 28),
('2024-10-29 17:45', 40, 85, 28),
('2024-10-29 17:46', 41, 84, 28),
('2024-10-29 17:47', 40, 83, 28),
('2024-10-29 17:48', 40, 85, 28),
('2024-10-29 17:49', 40, 84, 28),
('2024-10-29 17:50', 40, 84, 28),
('2024-10-29 17:51', 41, 85, 28),
('2024-10-29 17:52', 41, 85, 28),
('2024-10-29 17:53', 40, 85, 28),
('2024-10-29 17:54', 42, 83, 28),
('2024-10-29 17:55', 40, 85, 28),
('2024-10-29 17:56', 42, 85, 28),
('2024-10-29 17:57', 40, 83, 28),
('2024-10-29 17:58', 42, 83, 28),
('2024-10-29 17:59', 41, 84, 28),
('2024-10-29 18:00', 42, 85, 28),
('2024-10-29 18:01', 42, 85, 28),
('2024-10-29 18:02', 42, 85, 28),
('2024-10-29 18:03', 40, 85, 28),
('2024-10-29 18:04', 40, 83, 28),
('2024-10-29 18:05', 41, 83, 28),
('2024-10-29 18:06', 40, 84, 28),
('2024-10-29 18:07', 40, 84, 28),
('2024-10-29 18:08', 40, 84, 28),
('2024-10-29 18:09', 41, 85, 28),
('2024-10-29 18:10', 41, 84, 28),
('2024-10-29 18:11', 41, 84, 28),
('2024-10-29 18:12', 42, 83, 28),
('2024-10-29 18:13', 41, 83, 28),
('2024-10-29 18:14', 42, 85, 28),
('2024-10-29 18:15', 40, 84, 28),
('2024-10-29 18:16', 40, 83, 28),
('2024-10-29 18:17', 42, 83, 28),
('2024-10-29 18:18', 40, 85, 28),
('2024-10-29 18:19', 42, 84, 28),
('2024-10-29 18:20', 41, 83, 28),
('2024-10-29 18:21', 42, 84, 28),
('2024-10-29 18:22', 40, 84, 28),
('2024-10-29 18:23', 41, 85, 28),
('2024-10-29 18:24', 41, 84, 28),
('2024-10-29 18:25', 40, 83, 28),
('2024-10-29 18:26', 40, 83, 28),
('2024-10-29 18:27', 40, 83, 28),
('2024-10-29 18:28', 42, 85, 28),
('2024-10-29 18:29', 40, 83, 28),
('2024-10-29 18:30', 42, 84, 28),
('2024-10-29 18:31', 41, 85, 28),
('2024-10-29 18:32', 42, 83, 28),
('2024-10-29 18:33', 41, 83, 28),
('2024-10-29 18:34', 42, 85, 28),
('2024-10-29 18:35', 42, 83, 28),
('2024-10-29 18:36', 42, 84, 28),
('2024-10-29 18:37', 40, 85, 28),
('2024-10-29 18:38', 41, 85, 28),
('2024-10-29 18:39', 40, 85, 28),
('2024-10-29 18:40', 40, 84, 28),
('2024-10-29 18:41', 42, 83, 28),
('2024-10-29 18:42', 42, 85, 28),
('2024-10-29 18:43', 40, 85, 28),
('2024-10-29 18:44', 40, 85, 28),
('2024-10-29 18:45', 41, 83, 28),
('2024-10-29 18:46', 41, 84, 28),
('2024-10-29 18:47', 40, 85, 28),
('2024-10-29 18:48', 42, 85, 28),
('2024-10-29 18:49', 41, 83, 28),
('2024-10-29 18:50', 42, 84, 28),
('2024-10-29 18:51', 40, 85, 28),
('2024-10-29 18:52', 40, 85, 28),
('2024-10-29 18:53', 40, 85, 28),
('2024-10-29 18:54', 41, 84, 28),
('2024-10-29 18:55', 41, 85, 28),
('2024-10-29 18:56', 42, 85, 28),
('2024-10-29 18:57', 40, 84, 28),
('2024-10-29 18:58', 41, 85, 28),
('2024-10-29 18:59', 40, 85, 28),
('2024-10-29 19:00', 41, 85, 28);
