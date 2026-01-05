/**
 * Helpers Utility
 * 
 * Các helper functions dùng chung trong ứng dụng.
 */

/**
 * Chuyển đổi string thành số, trả về null nếu không hợp lệ
 * @param {string|number} value - Giá trị cần convert
 * @returns {number|null} Số hoặc null
 */
export function parseNumber(value) {
  if (value === null || value === undefined) return null;
  
  const str = String(value).trim();
  if (!str) return null;
  
  const num = Number(str);
  return Number.isFinite(num) ? num : null;
}

/**
 * Chuẩn hóa string, trả về null nếu empty
 * @param {string} value - String cần chuẩn hóa
 * @returns {string|null} String đã trim hoặc null
 */
export function normalizeString(value) {
  if (!value) return null;
  const trimmed = String(value).trim();
  return trimmed || null;
}

/**
 * Format điểm số để hiển thị
 * @param {number|string} score - Điểm số
 * @returns {string} Điểm đã format hoặc '—' nếu không có
 */
export function formatScore(score) {
  if (score === null || score === undefined || score === '') {
    return '—';
  }
  const num = Number(score);
  if (!Number.isFinite(num)) return '—';
  return num.toFixed(1);
}

/**
 * Format ngày sinh để hiển thị
 * @param {string} dateStr - Date string (YYYY-MM-DD)
 * @returns {string} Date đã format hoặc '—'
 */
export function formatDate(dateStr) {
  if (!dateStr) return '—';
  try {
    const date = new Date(dateStr);
    return date.toLocaleDateString('vi-VN');
  } catch {
    return dateStr;
  }
}

/**
 * Lấy tên đầy đủ của sinh viên
 * @param {Object} student - Student object
 * @returns {string} Full name hoặc fallback
 */
export function getFullName(student) {
  const parts = [student.last_name, student.first_name].filter(Boolean);
  return parts.join(' ') || '(Chưa có tên)';
}

/**
 * Kiểm tra student có đủ thông tin cơ bản không
 * @param {Object} student - Student object
 * @returns {boolean} True nếu có ít nhất tên hoặc email
 */
export function hasBasicInfo(student) {
  return !!(student.first_name || student.last_name || student.email);
}
