CREATE TABLE car_sales (
    sales_id INT PRIMARY KEY,
    date_of_purchase DATE,
    customer_id INT,
    fuel TEXT,
    premium INT,
    vehicle_segment TEXT,
    selling_price INT,
    power_steering BOOLEAN,
    airbags BOOLEAN,
    sunroof BOOLEAN,
    matte_finish BOOLEAN,
    music_system BOOLEAN,
    customer_gender TEXT,
    customer_income_group TEXT,
    customer_region TEXT,
    customer_marital_status BOOLEAN
);

INSERT INTO car_sales VALUES(12345, '1/16/2018', 400, 'CNG', 958, 'A', 958, '0', '0', '0', '1', '1', 'Male', '0- $25K', 'North', '0');
INSERT INTO car_sales VALUES(12346, '01/04/18', 401, 'CNG', 1272, 'A', 1272, '1', '0', '0', '0', '1', 'Male', '$25-$70K', 'South', '0');
INSERT INTO car_sales VALUES(12347, '01/07/18', 402, 'CNG', 2150, 'A', 2150, '0', '1', '1', '1', '0', 'Male', '>$70K', 'East', '1');
INSERT INTO car_sales VALUES(12348, '01/07/18', 403, 'CNG', 2123, 'A', 2123, '1', '0', '1', '1', '1', 'Male', '$25-$70K', 'West', '1');
INSERT INTO car_sales VALUES(12349, '01/01/18', 404, 'CNG', 1110, 'A', 1110, '1', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12350, '1/22/2018', 405, 'CNG', 1571, 'A', 1571, '0', '0', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12351, '1/19/2018', 406, 'CNG', 1030, 'A', 1030, '1', '1', '1', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12352, '1/23/2018', 407, 'CNG', 1732, 'A', 1732, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12353, '01/01/18', 408, 'CNG', 2175, 'A', 2175, '0', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12354, '1/20/2018', 409, 'CNG', 1725, 'A', 1725, '0', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12355, '1/28/2018', 410, 'CNG', 1805, 'A', 1805, '0', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12356, '1/17/2018', 411, 'CNG', 1552, 'A', 1552, '1', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12357, '1/29/2018', 412, 'CNG', 1888, 'A', 1888, '0', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12358, '1/18/2018', 413, 'CNG', 1355, 'A', 1355, '1', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12359, '1/19/2018', 414, 'CNG', 2356, 'A', 2356, '0', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12360, '01/06/18', 415, 'CNG', 2102, 'A', 2102, '1', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12361, '1/27/2018', 416, 'CNG', 1258, 'A', 1258, '1', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12362, '1/21/2018', 417, 'CNG', 2326, 'A', 2326, '0', '1', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(420, '1/24/2018', 418, 'CNG', 584, 'A', 584, '1', '1', '1', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12364, '01/08/18', 419, 'CNG', 2397, 'A', 2397, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12365, '1/23/2018', 420, 'CNG', 1493, 'A', 1493, '1', '0', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12366, '01/02/18', 420, 'CNG', 661, 'A', 661, '0', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12367, '01/03/18', 420, 'CNG', 685, 'A', 685, '1', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12368, '01/08/18', 420, 'CNG', 1006, 'A', 1006, '1', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12369, '1/16/2018', 420, 'CNG', 1160, 'A', 1160, '1', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12370, '1/25/2018', 420, 'CNG', 1602, 'A', 1602, '0', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12371, '1/25/2018', 420, 'CNG', 2355, 'A', 2355, '0', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12372, '01/05/18', 420, 'CNG', 1921, 'A', 1921, '1', '1', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12373, '1/21/2018', 420, 'CNG', 2200, 'A', 2200, '0', '1', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12374, '1/27/2018', 420, 'CNG', 2357, 'A', 2357, '0', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12375, '1/22/2018', 420, 'CNG', 1047, 'A', 1047, '0', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(840, '01/04/18', 420, 'CNG', 2089, 'A', 2089, '0', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12377, '1/15/2018', 420, 'CNG', 1780, 'A', 1780, '0', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12378, '1/26/2018', 420, 'CNG', 1035, 'A', 1035, '1', '0', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12379, '1/29/2018', 420, 'CNG', 526, 'A', 526, '1', '1', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12380, '1/20/2018', 420, 'CNG', 1827, 'A', 1827, '0', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12381, '1/24/2018', 420, 'CNG', 2003, 'A', 2003, '1', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12382, '01/08/18', 420, 'CNG', 1960, 'A', 1960, '0', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12383, '01/03/18', 420, 'CNG', 1197, 'A', 1197, '0', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12384, '1/21/2018', 420, 'CNG', 614, 'A', 614, '0', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12385, '01/09/18', 420, 'CNG', 568, 'A', 568, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12386, '01/12/18', 420, 'CNG', 2149, 'A', 2149, '1', '0', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12387, '1/27/2018', 420, 'CNG', 1797, 'A', 1797, '1', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12388, '1/14/2018', 420, 'CNG', 1246, 'A', 1246, '1', '0', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12389, '1/24/2018', 420, 'CNG', 1295, 'A', 1295, '1', '1', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12390, '1/21/2018', 420, 'CNG', 642, 'A', 642, '0', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12391, '01/06/18', 420, 'CNG', 1979, 'A', 1979, '1', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12392, '1/13/2018', 420, 'CNG', 2327, 'A', 2327, '0', '0', '1', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12393, '01/05/18', 420, 'CNG', 1025, 'A', 1025, '1', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12394, '1/23/2018', 420, 'CNG', 529, 'A', 529, '0', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12395, '1/16/2018', 420, 'CNG', 2072, 'A', 2072, '0', '0', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12396, '1/18/2018', 420, 'CNG', 2103, 'A', 2103, '0', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12397, '1/15/2018', 420, 'CNG', 1929, 'A', 1929, '0', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12398, '1/13/2018', 420, 'CNG', 2143, 'A', 2143, '1', '0', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12399, '01/11/18', 420, 'CNG', 2132, 'A', 2132, '0', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12400, '1/13/2018', 420, 'CNG', 1459, 'A', 1459, '1', '0', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12401, '1/17/2018', 420, 'CNG', 1831, 'A', 1831, '1', '1', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12402, '1/30/2018', 420, 'CNG', 1171, 'A', 1171, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12403, '01/10/18', 420, 'CNG', 1692, 'A', 1692, '1', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12404, '01/11/18', 420, 'CNG', 1262, 'A', 1262, '0', '1', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12405, '1/23/2018', 420, 'CNG', 2451, 'A', 2451, '0', '1', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12406, '01/03/18', 420, 'CNG', 1906, 'A', 1906, '0', '0', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12407, '1/24/2018', 420, 'CNG', 2095, 'A', 2095, '1', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12408, '1/20/2018', 420, 'CNG', 1597, 'A', 1597, '1', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12409, '1/15/2018', 420, 'CNG', 2362, 'A', 2362, '1', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12410, '1/17/2018', 420, 'CNG', 1612, 'A', 1612, '1', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12411, '1/19/2018', 420, 'CNG', 711, 'A', 711, '0', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12412, '1/29/2018', 420, 'CNG', 1771, 'A', 1771, '1', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12413, '1/20/2018', 420, 'CNG', 1301, 'A', 1301, '0', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12414, '1/16/2018', 420, 'CNG', 2411, 'A', 2411, '1', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12415, '01/10/18', 420, 'CNG', 1065, 'A', 1065, '0', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12416, '1/13/2018', 420, 'CNG', 2393, 'A', 2393, '1', '1', '1', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12417, '01/05/18', 420, 'CNG', 1837, 'A', 1837, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12418, '01/01/18', 420, 'CNG', 1598, 'A', 1598, '0', '0', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12419, '1/30/2018', 420, 'CNG', 1072, 'A', 1072, '1', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12420, '1/25/2018', 420, 'CNG', 591, 'A', 591, '0', '0', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12421, '1/18/2018', 420, 'CNG', 1617, 'A', 1617, '1', '1', '1', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12422, '01/04/18', 420, 'CNG', 1174, 'A', 1174, '1', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12423, '1/28/2018', 420, 'CNG', 2241, 'A', 2241, '1', '1', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12424, '1/31/2018', 420, 'CNG', 2248, 'A', 2248, '1', '1', '0', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12425, '1/27/2018', 420, 'CNG', 2121, 'A', 2121, '1', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12426, '1/25/2018', 420, 'CNG', 1994, 'A', 1994, '0', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12427, '01/01/18', 420, 'CNG', 2442, 'A', 2442, '1', '1', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12428, '1/23/2018', 420, 'CNG', 1763, 'A', 1763, '0', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12429, '1/28/2018', 420, 'CNG', 1494, 'A', 1494, '0', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12430, '01/03/18', 420, 'CNG', 2039, 'A', 2039, '1', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12431, '1/27/2018', 420, 'CNG', 898, 'A', 898, '1', '0', '0', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12432, '01/12/18', 420, 'CNG', 823, 'A', 823, '0', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12433, '01/11/18', 420, 'CNG', 1144, 'A', 1144, '0', '1', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12434, '1/23/2018', 420, 'CNG', 1051, 'A', 1051, '0', '0', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12435, '01/10/18', 420, 'CNG', 1212, 'A', 1212, '0', '0', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12436, '1/13/2018', 420, 'CNG', 1829, 'A', 1829, '0', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12437, '1/15/2018', 420, 'CNG', 1548, 'A', 1548, '0', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12438, '01/06/18', 420, 'CNG', 1663, 'A', 1663, '1', '1', '0', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12439, '1/23/2018', 420, 'CNG', 1313, 'A', 1313, '0', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12440, '01/04/18', 420, 'CNG', 1915, 'A', 1915, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12441, '01/08/18', 420, 'CNG', 1888, 'A', 1888, '0', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12442, '1/19/2018', 420, 'CNG', 694, 'A', 694, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12443, '01/05/18', 420, 'CNG', 637, 'A', 637, '0', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12444, '02/10/18', 420, 'CNG', 1959, 'A', 1959, '1', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12445, '02/08/18', 420, 'CNG', 1673, 'A', 1673, '0', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12446, '02/01/18', 420, 'CNG', 934, 'A', 934, '1', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12447, '2/23/2018', 420, 'CNG', 2391, 'A', 2391, '1', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12448, '2/20/2018', 420, 'CNG', 2246, 'A', 2246, '1', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12449, '02/03/18', 420, 'CNG', 1328, 'A', 1328, '0', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12450, '2/13/2018', 420, 'CNG', 2455, 'A', 2455, '1', '1', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12451, '2/25/2018', 420, 'CNG', 1611, 'A', 1611, '0', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12452, '02/03/18', 420, 'CNG', 2256, 'A', 2256, '1', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12453, '2/26/2018', 420, 'CNG', 1284, 'A', 1284, '0', '0', '0', '0', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12454, '02/05/18', 420, 'CNG', 2067, 'A', 2067, '1', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12455, '02/11/18', 420, 'CNG', 1477, 'A', 1477, '1', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12456, '2/18/2018', 420, 'CNG', 865, 'A', 865, '0', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12457, '02/01/18', 420, 'CNG', 1662, 'A', 1662, '0', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12458, '02/03/18', 420, 'CNG', 1870, 'A', 1870, '0', '0', '0', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12459, '02/05/18', 420, 'CNG', 626, 'A', 626, '1', '1', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12460, '02/11/18', 420, 'CNG', 1658, 'A', 1658, '1', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12461, '2/16/2018', 420, 'CNG', 1168, 'A', 1168, '0', '1', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12462, '02/02/18', 420, 'CNG', 1083, 'A', 1083, '0', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12463, '02/06/18', 420, 'CNG', 2253, 'A', 2253, '0', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12464, '02/05/18', 420, 'CNG', 708, 'A', 708, '1', '1', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12465, '2/14/2018', 420, 'CNG', 2254, 'A', 2254, '1', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12466, '2/15/2018', 420, 'CNG', 1092, 'A', 1092, '0', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12467, '2/26/2018', 420, 'CNG', 778, 'A', 778, '1', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12468, '2/15/2018', 420, 'CNG', 1041, 'A', 1041, '0', '0', '1', '1', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12469, '02/03/18', 420, 'CNG', 2310, 'A', 2310, '0', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12470, '2/25/2018', 420, 'CNG', 2339, 'A', 2339, '1', '1', '1', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12471, '02/12/18', 420, 'CNG', 2218, 'A', 2218, '0', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12472, '02/11/18', 420, 'CNG', 1628, 'A', 1628, '1', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12473, '2/16/2018', 420, 'CNG', 850, 'A', 850, '1', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12474, '2/14/2018', 420, 'CNG', 618, 'A', 618, '0', '1', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12475, '2/22/2018', 420, 'CNG', 2128, 'A', 2128, '0', '0', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12476, '2/16/2018', 420, 'CNG', 1213, 'A', 1213, '1', '0', '0', '1', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12477, '02/04/18', 420, 'CNG', 749, 'A', 749, '1', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12478, '2/14/2018', 420, 'CNG', 2420, 'A', 2420, '0', '0', '1', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12479, '02/08/18', 420, 'CNG', 1231, 'A', 1231, '0', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12480, '2/27/2018', 420, 'CNG', 510, 'A', 510, '0', '1', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12481, '2/14/2018', 420, 'CNG', 2376, 'A', 2376, '0', '1', '1', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12482, '2/27/2018', 420, 'CNG', 1746, 'A', 1746, '1', '1', '0', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12483, '2/21/2018', 420, 'CNG', 1533, 'A', 1533, '0', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12484, '2/19/2018', 420, 'CNG', 901, 'A', 901, '1', '1', '1', '0', '0', 'Male', '$25-$70K', 'North', '0');
INSERT INTO car_sales VALUES(12485, '02/04/18', 420, 'CNG', 2021, 'A', 2021, '0', '0', '1', '1', '0', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12486, '2/22/2018', 420, 'CNG', 1570, 'A', 1570, '0', '0', '0', '0', '1', 'Male', '$25-$70K', 'North', '1');
INSERT INTO car_sales VALUES(12487, '2/19/2018', 420, 'CNG', 2338, 'A', 2338, '0', '0', '
