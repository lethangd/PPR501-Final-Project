/**
 * Student API Service
 * 
 * Module này cung cấp các methods CRUD cho Student entity.
 * Gọi REST API và parse XML response.
 */

import * as api from './api';
import { parseStudentsXml, parseStudentXml } from '../utils/xmlParser';
import { normalizeString, parseNumber } from '../utils/helpers';

/**
 * Chuẩn hóa student data trước khi gửi lên API
 * @param {Object} formData - Dữ liệu từ form
 * @param {boolean} includeStudentId - Có bao gồm student_id không
 * @returns {Object} Payload đã chuẩn hóa
 */
function preparePayload(formData, includeStudentId = false) {
  const payload = {
    last_name: normalizeString(formData.last_name),
    first_name: normalizeString(formData.first_name),
    email: normalizeString(formData.email),
    birth_date: normalizeString(formData.birth_date),
    hometown: normalizeString(formData.hometown),
    math_score: parseNumber(formData.math_score),
    literature_score: parseNumber(formData.literature_score),
    english_score: parseNumber(formData.english_score),
  };
  
  if (includeStudentId) {
    payload.student_id = formData.student_id?.trim()?.toUpperCase();
  }
  
  return payload;
}

/**
 * Lấy danh sách tất cả sinh viên
 * @returns {Promise<Array<Object>>} Mảng students
 */
export async function fetchStudents() {
  const xmlText = await api.get('/students');
  return parseStudentsXml(xmlText);
}

/**
 * Lấy thông tin một sinh viên
 * @param {string} studentId - Mã sinh viên
 * @returns {Promise<Object>} Student object
 */
export async function fetchStudent(studentId) {
  const xmlText = await api.get(`/students/${encodeURIComponent(studentId)}`);
  return parseStudentXml(xmlText);
}

/**
 * Tạo sinh viên mới
 * @param {Object} formData - Dữ liệu sinh viên
 * @returns {Promise<Object>} Student vừa tạo
 */
export async function createStudent(formData) {
  const payload = preparePayload(formData, true);
  
  if (!payload.student_id) {
    throw new Error('Mã sinh viên là bắt buộc');
  }
  
  const xmlText = await api.post('/students', payload);
  return parseStudentXml(xmlText);
}

/**
 * Cập nhật thông tin sinh viên
 * @param {string} studentId - Mã sinh viên
 * @param {Object} formData - Dữ liệu cập nhật
 * @returns {Promise<Object>} Student sau cập nhật
 */
export async function updateStudent(studentId, formData) {
  const payload = preparePayload(formData, false);
  const xmlText = await api.put(`/students/${encodeURIComponent(studentId)}`, payload);
  return parseStudentXml(xmlText);
}

/**
 * Xóa sinh viên
 * @param {string} studentId - Mã sinh viên
 * @returns {Promise<void>}
 */
export async function deleteStudent(studentId) {
  await api.del(`/students/${encodeURIComponent(studentId)}`);
}
