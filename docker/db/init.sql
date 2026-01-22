-- ============================================================
-- Initialize schema and seed data
-- ============================================================
-- NOTE: This runs only on first init of the Postgres volume.

-- ============================================================
-- 1) Tạo bảng PROVINCES và seed 63 tỉnh thành Việt Nam
-- ============================================================

CREATE TABLE IF NOT EXISTS provinces (
  id SERIAL PRIMARY KEY,
  code VARCHAR(10) UNIQUE NOT NULL,
  name VARCHAR(100) UNIQUE NOT NULL,
  region VARCHAR(20) NOT NULL
);

-- Seed 63 tỉnh thành Việt Nam (Ordered by region)

-- MIỀN BẮC (Bắc)
INSERT INTO provinces (code, name, region) VALUES
('HN', 'Hà Nội', 'Bắc'),
('HP', 'Hải Phòng', 'Bắc'),
('QN', 'Quảng Ninh', 'Bắc'),
('BG', 'Bắc Giang', 'Bắc'),
('BK', 'Bắc Kạn', 'Bắc'),
('BN', 'Bắc Ninh', 'Bắc'),
('CB', 'Cao Bằng', 'Bắc'),
('DB', 'Điện Biên', 'Bắc'),
('HG', 'Hà Giang', 'Bắc'),
('HNM', 'Hà Nam', 'Bắc'),
('HD', 'Hải Dương', 'Bắc'),
('HB', 'Hòa Bình', 'Bắc'),
('HY', 'Hưng Yên', 'Bắc'),
('LC', 'Lai Châu', 'Bắc'),
('LS', 'Lạng Sơn', 'Bắc'),
('LO', 'Lào Cai', 'Bắc'),
('ND', 'Nam Định', 'Bắc'),
('NB', 'Ninh Bình', 'Bắc'),
('PT', 'Phú Thọ', 'Bắc'),
('SL', 'Sơn La', 'Bắc'),
('TB', 'Thái Bình', 'Bắc'),
('TN', 'Thái Nguyên', 'Bắc'),
('TQ', 'Tuyên Quang', 'Bắc'),
('VP', 'Vĩnh Phúc', 'Bắc'),
('YB', 'Yên Bái', 'Bắc');

-- MIỀN TRUNG (Trung)
INSERT INTO provinces (code, name, region) VALUES
('DN', 'Đà Nẵng', 'Trung'),
('HT', 'Hà Tĩnh', 'Trung'),
('KH', 'Khánh Hòa', 'Trung'),
('NA', 'Nghệ An', 'Trung'),
('PY', 'Phú Yên', 'Trung'),
('QB', 'Quảng Bình', 'Trung'),
('QM', 'Quảng Nam', 'Trung'),
('QG', 'Quảng Ngãi', 'Trung'),
('QT', 'Quảng Trị', 'Trung'),
('TH', 'Thanh Hóa', 'Trung'),
('HU', 'Thừa Thiên Huế', 'Trung'),
('BD', 'Bình Định', 'Trung'),
('BTH', 'Bình Thuận', 'Trung'),
('DL', 'Đà Lạt', 'Trung'),
('GL', 'Gia Lai', 'Trung'),
('KT', 'Kon Tum', 'Trung'),
('NT', 'Ninh Thuận', 'Trung'),
('DK', 'Đắk Lắk', 'Trung'),
('DN2', 'Đắk Nông', 'Trung');

-- MIỀN NAM (Nam)
INSERT INTO provinces (code, name, region) VALUES
('HCM', 'TP. Hồ Chí Minh', 'Nam'),
('CT', 'Cần Thơ', 'Nam'),
('AG', 'An Giang', 'Nam'),
('BV', 'Bà Rịa - Vũng Tàu', 'Nam'),
('BL', 'Bạc Liêu', 'Nam'),
('BT', 'Bến Tre', 'Nam'),
('BDG', 'Bình Dương', 'Nam'),
('BP', 'Bình Phước', 'Nam'),
('CM', 'Cà Mau', 'Nam'),
('DNI', 'Đồng Nai', 'Nam'),
('DTP', 'Đồng Tháp', 'Nam'),
('HGI', 'Hậu Giang', 'Nam'),
('KG', 'Kiên Giang', 'Nam'),
('LDG', 'Lâm Đồng', 'Nam'),
('LA', 'Long An', 'Nam'),
('ST', 'Sóc Trăng', 'Nam'),
('TN2', 'Tây Ninh', 'Nam'),
('TG', 'Tiền Giang', 'Nam'),
('TV', 'Trà Vinh', 'Nam'),
('VL', 'Vĩnh Long', 'Nam');

-- ============================================================
-- 2) Tạo bảng STUDENTS với foreign key đến provinces
-- ============================================================

CREATE TABLE IF NOT EXISTS students (
  student_id VARCHAR(20) PRIMARY KEY,
  last_name TEXT NULL,
  first_name TEXT NULL,
  email TEXT NULL,
  birth_date DATE NULL,
  province_id INTEGER NULL REFERENCES provinces(id) ON DELETE SET NULL,
  hometown TEXT NULL,  -- Deprecated, kept for backward compatibility
  math_score NUMERIC(4,2) NULL,
  literature_score NUMERIC(4,2) NULL,
  english_score NUMERIC(4,2) NULL
);

-- ============================================================
-- 3) Import students từ CSV
-- ============================================================

-- Tạo staging table với tất cả TEXT để import CSV
CREATE TEMP TABLE students_staging (
  student_id TEXT,
  last_name TEXT,
  first_name TEXT,
  email TEXT,
  birth_date TEXT,
  hometown TEXT,
  math_score TEXT,
  literature_score TEXT,
  english_score TEXT
);

-- Import CSV vào staging table
COPY students_staging(
  student_id,
  last_name,
  first_name,
  email,
  birth_date,
  hometown,
  math_score,
  literature_score,
  english_score
)
FROM '/docker-entrypoint-initdb.d/students.csv'
WITH (FORMAT csv, HEADER true);

-- Chuyển từ staging sang bảng chính
-- Map hometown string -> province_id (flexible matching)
INSERT INTO students (
  student_id,
  last_name,
  first_name,
  email,
  birth_date,
  province_id,
  hometown,
  math_score,
  literature_score,
  english_score
)
SELECT
  s.student_id,
  NULLIF(TRIM(s.last_name), ''),
  NULLIF(TRIM(s.first_name), ''),
  NULLIF(TRIM(s.email), ''),
  CASE WHEN TRIM(s.birth_date) = '' THEN NULL ELSE s.birth_date::DATE END,
  COALESCE(
    -- Try exact match first
    (SELECT id FROM provinces WHERE name = TRIM(s.hometown)),
    -- Try case-insensitive match
    (SELECT id FROM provinces WHERE LOWER(name) = LOWER(TRIM(s.hometown))),
    -- Try without diacritics (common variations)
    (SELECT id FROM provinces WHERE
      LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(name, 'đ', 'd'), 'Đ', 'D'), 'ô', 'o'), 'ơ', 'o'), 'ư', 'u'))
      = LOWER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(TRIM(s.hometown), 'đ', 'd'), 'Đ', 'D'), 'ô', 'o'), 'ơ', 'o'), 'ư', 'u'))
    ),
    NULL
  ),
  NULLIF(TRIM(s.hometown), ''),
  CASE WHEN TRIM(s.math_score) = '' THEN NULL ELSE s.math_score::NUMERIC(4,2) END,
  CASE WHEN TRIM(s.literature_score) = '' THEN NULL ELSE s.literature_score::NUMERIC(4,2) END,
  CASE WHEN TRIM(s.english_score) = '' THEN NULL ELSE s.english_score::NUMERIC(4,2) END
FROM students_staging s;

-- Xóa staging table
DROP TABLE students_staging;
