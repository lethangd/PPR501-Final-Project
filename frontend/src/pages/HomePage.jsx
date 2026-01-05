/**
 * HomePage
 * 
 * Trang chính của ứng dụng quản lý sinh viên.
 * Bao gồm form CRUD và bảng danh sách.
 */

import React, { useState } from 'react';
import { StudentForm, StudentTable } from '../components/students';
import { ConfirmDialog } from '../components/ui';
import { useStudents } from '../hooks/useStudents';

export function HomePage() {
  const {
    students,
    loading,
    selectedId,
    form,
    isEditing,
    canSubmit,
    selectStudent,
    resetForm,
    updateField,
    handleCreate,
    handleUpdate,
    handleDelete,
    loadStudents,
  } = useStudents();

  // State cho confirm dialog
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const onDeleteClick = () => {
    setShowDeleteConfirm(true);
  };

  const onConfirmDelete = async () => {
    await handleDelete();
    setShowDeleteConfirm(false);
  };

  return (
    <div className="space-y-6">
      {/* Form Section */}
      <StudentForm
        form={form}
        isEditing={isEditing}
        loading={loading}
        canSubmit={canSubmit}
        onFieldChange={updateField}
        onCreate={handleCreate}
        onUpdate={handleUpdate}
        onDelete={onDeleteClick}
        onReset={resetForm}
      />

      {/* Table Section */}
      <StudentTable
        students={students}
        selectedId={selectedId}
        loading={loading}
        onSelect={selectStudent}
      />

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showDeleteConfirm}
        onClose={() => setShowDeleteConfirm(false)}
        onConfirm={onConfirmDelete}
        title="Xóa sinh viên"
        message={`Bạn có chắc chắn muốn xóa sinh viên ${form.student_id}? Hành động này không thể hoàn tác.`}
        confirmText="Xóa"
        loading={loading}
      />
    </div>
  );
}
