(*) số lượng log theo từng giờ
SELECT HOUR(timestamp) AS log_hour, COUNT(*) AS log_count
FROM manhdx.realtimedata
WHERE DATE(timestamp) = '2024-11-04'  -- Filter for a specific date
GROUP BY HOUR(timestamp)
ORDER BY log_hour;

(*) log theo ngày cụ thể
SELECT * FROM realtimedata WHERE DAYOFWEEK(timestamp) IN (6,6); -- 1 is sunday and 7 is saturday
SELECT * FROM realtimedata WHERE timestamp LIKE '%11-01%';

(*) tìm nhiệt độ lớn nhất và nhỏ nhất theo ngày
SELECT DATE(timestamp) AS log_date, MAX(temperature) AS max_temperature, MIN(temperature) AS min_temperature
FROM realtimedata
GROUP BY DATE(timestamp);


(*)  tìm nhiệt độ trung bình
SELECT DATE(timestamp) AS log_date, AVG(temperature) AS avg_temperature
FROM realtimedata
GROUP BY DATE(timestamp);

(*) nhiệt độ trung bình của mỗi giờ trong ngày
SELECT HOUR(timestamp) AS log_hour, AVG(temperature) AS avg_temperature
FROM manhdx.realtimedata
WHERE DATE(timestamp) = '2024-11-01'  -- Specify the desired date here
GROUP BY HOUR(timestamp)
ORDER BY log_hour;

(*) top 10 nhiệt độ lớn nhất trong khoảng thời gian
SELECT *
FROM (
    SELECT *, 
           ROW_NUMBER() OVER (ORDER BY temperature DESC) AS row_num
    FROM manhdx.realtimedata
    WHERE timestamp BETWEEN '2024-11-01 00:00:00' AND '2024-11-01 23:59:59'
) ranked_logs
WHERE row_num <= 10;  -- Replace N with the number of top results you want

(*) tìm log trong khoảng thời gian
SELECT *
FROM realtimedata
WHERE timestamp BETWEEN '2024-01-01' AND '2024-01-31';

(*) đếm log theo từng topic
SELECT topic, COUNT(*) AS log FROM actionhistory GROUP BY topic ORDER BY log DESC;