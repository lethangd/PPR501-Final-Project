/**
 * XML Parser Utility
 * 
 * Module này cung cấp các functions để parse XML response
 * từ API thành JavaScript objects.
 */

/**
 * Lấy text content từ một XML element
 * @param {Element|null} element - XML element
 * @returns {string} Text content hoặc empty string
 */
export function getTextContent(element) {
  if (!element) return '';
  return (element.textContent ?? '').trim();
}

/**
 * Parse một student element từ XML sang object
 * @param {Element} studentNode - XML element <student>
 * @returns {Object} Student object
 */
export function parseStudentNode(studentNode) {
  const get = (tagName) => getTextContent(studentNode.querySelector(tagName));
  
  return {
    student_id: get('student_id'),
    last_name: get('last_name'),
    first_name: get('first_name'),
    email: get('email'),
    birth_date: get('birth_date'),
    hometown: get('hometown'),
    math_score: get('math_score'),
    literature_score: get('literature_score'),
    english_score: get('english_score'),
  };
}

/**
 * Parse XML string chứa danh sách students
 * @param {string} xmlText - XML string từ API
 * @returns {Array<Object>} Mảng các student objects
 * @throws {Error} Nếu XML không hợp lệ
 */
export function parseStudentsXml(xmlText) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(xmlText, 'application/xml');
  
  // Kiểm tra lỗi parse
  const errorNode = doc.querySelector('parsererror');
  if (errorNode) {
    throw new Error('Invalid XML response from API');
  }
  
  // Parse tất cả student nodes
  const studentNodes = doc.querySelectorAll('students > student');
  return Array.from(studentNodes).map(parseStudentNode);
}

/**
 * Parse XML string chứa một student
 * @param {string} xmlText - XML string từ API
 * @returns {Object} Student object
 * @throws {Error} Nếu XML không hợp lệ
 */
export function parseStudentXml(xmlText) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(xmlText, 'application/xml');
  
  const errorNode = doc.querySelector('parsererror');
  if (errorNode) {
    throw new Error('Invalid XML response from API');
  }
  
  const studentNode = doc.querySelector('student');
  if (!studentNode) {
    throw new Error('No student element found in XML');
  }
  
  return parseStudentNode(studentNode);
}
