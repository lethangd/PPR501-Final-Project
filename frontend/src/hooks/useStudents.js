/**
 * useStudents Hook
 * 
 * Custom hook để quản lý state và operations cho students.
 * Bao gồm loading state, error handling, và CRUD operations.
 */

import { useState, useCallback, useEffect } from 'react';
import toast from 'react-hot-toast';
import * as studentApi from '../services/studentApi';

// Initial form state
const EMPTY_FORM = {
  student_id: '',
  last_name: '',
  first_name: '',
  email: '',
  birth_date: '',
  hometown: '',
  math_score: '',
  literature_score: '',
  english_score: '',
};

/**
 * Custom hook quản lý students
 * @returns {Object} State và methods
 */
export function useStudents() {
  // State
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedId, setSelectedId] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  
  // Computed
  const selectedStudent = students.find(s => s.student_id === selectedId);
  const isEditing = !!selectedId;
  const canSubmit = isEditing || form.student_id.trim().length > 0;
  
  /**
   * Load danh sách sinh viên
   */
  const loadStudents = useCallback(async () => {
    setLoading(true);
    try {
      const data = await studentApi.fetchStudents();
      setStudents(data);
    } catch (error) {
      toast.error(`Lỗi tải dữ liệu: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, []);
  
  /**
   * Chọn một sinh viên để edit
   * @param {Object} student - Student object
   */
  const selectStudent = useCallback((student) => {
    setSelectedId(student.student_id);
    setForm({
      student_id: student.student_id || '',
      last_name: student.last_name || '',
      first_name: student.first_name || '',
      email: student.email || '',
      birth_date: student.birth_date || '',
      hometown: student.hometown || '',
      math_score: student.math_score || '',
      literature_score: student.literature_score || '',
      english_score: student.english_score || '',
    });
  }, []);
  
  /**
   * Reset form về trạng thái ban đầu
   */
  const resetForm = useCallback(() => {
    setSelectedId(null);
    setForm(EMPTY_FORM);
  }, []);
  
  /**
   * Update một field trong form
   * @param {string} field - Tên field
   * @param {string} value - Giá trị mới
   */
  const updateField = useCallback((field, value) => {
    setForm(prev => ({ ...prev, [field]: value }));
  }, []);
  
  /**
   * Tạo sinh viên mới
   */
  const handleCreate = useCallback(async () => {
    if (!form.student_id.trim()) {
      toast.error('Vui lòng nhập mã sinh viên');
      return;
    }
    
    setLoading(true);
    try {
      await studentApi.createStudent(form);
      toast.success('Thêm sinh viên thành công!');
      resetForm();
      await loadStudents();
    } catch (error) {
      toast.error(`Lỗi: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [form, resetForm, loadStudents]);
  
  /**
   * Cập nhật sinh viên đang chọn
   */
  const handleUpdate = useCallback(async () => {
    if (!selectedId) return;
    
    setLoading(true);
    try {
      await studentApi.updateStudent(selectedId, form);
      toast.success('Cập nhật thành công!');
      await loadStudents();
    } catch (error) {
      toast.error(`Lỗi: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [selectedId, form, loadStudents]);
  
  /**
   * Xóa sinh viên đang chọn
   */
  const handleDelete = useCallback(async () => {
    if (!selectedId) return;
    
    setLoading(true);
    try {
      await studentApi.deleteStudent(selectedId);
      toast.success('Xóa sinh viên thành công!');
      resetForm();
      await loadStudents();
    } catch (error) {
      toast.error(`Lỗi: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }, [selectedId, resetForm, loadStudents]);
  
  // Load data on mount
  useEffect(() => {
    loadStudents();
  }, [loadStudents]);
  
  return {
    // State
    students,
    loading,
    selectedId,
    selectedStudent,
    form,
    isEditing,
    canSubmit,
    
    // Actions
    loadStudents,
    selectStudent,
    resetForm,
    updateField,
    handleCreate,
    handleUpdate,
    handleDelete,
  };
}
