-- ============================================================
-- Initialize schema and seed 100 students
-- ============================================================
-- NOTE: This runs only on first init of the Postgres volume.
-- Sử dụng staging table để xử lý empty strings trong CSV

-- 1) Tạo bảng chính với đúng kiểu dữ liệu
CREATE TABLE IF NOT EXISTS students (
  student_id VARCHAR(20) PRIMARY KEY,
  last_name TEXT NULL,
  first_name TEXT NULL,
  email TEXT NULL,
  birth_date DATE NULL,
  hometown TEXT NULL,
  math_score NUMERIC(4,2) NULL,
  literature_score NUMERIC(4,2) NULL,
  english_score NUMERIC(4,2) NULL
);

-- 2) Tạo staging table với tất cả TEXT để import CSV
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

-- 3) Import CSV vào staging table
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

-- 4) Chuyển từ staging sang bảng chính, xử lý empty strings thành NULL
INSERT INTO students (
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
SELECT
  student_id,
  NULLIF(TRIM(last_name), ''),
  NULLIF(TRIM(first_name), ''),
  NULLIF(TRIM(email), ''),
  CASE WHEN TRIM(birth_date) = '' THEN NULL ELSE birth_date::DATE END,
  NULLIF(TRIM(hometown), ''),
  CASE WHEN TRIM(math_score) = '' THEN NULL ELSE math_score::NUMERIC(4,2) END,
  CASE WHEN TRIM(literature_score) = '' THEN NULL ELSE literature_score::NUMERIC(4,2) END,
  CASE WHEN TRIM(english_score) = '' THEN NULL ELSE english_score::NUMERIC(4,2) END
FROM students_staging;

-- 5) Xóa staging table
DROP TABLE students_staging;

