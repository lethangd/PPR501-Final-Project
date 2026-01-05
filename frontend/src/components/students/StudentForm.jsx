/**
 * StudentForm Component
 * 
 * Form để thêm mới hoặc chỉnh sửa thông tin sinh viên.
 */

import React from 'react';
import { 
  UserPlusIcon, 
  PencilSquareIcon,
  TrashIcon,
  ArrowPathIcon,
  XMarkIcon 
} from '@heroicons/react/24/outline';
import { Card, CardHeader, CardBody, CardFooter } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

/**
 * @param {Object} props
 * @param {Object} props.form - Form state
 * @param {boolean} props.isEditing - Đang edit hay tạo mới
 * @param {boolean} props.loading - Loading state
 * @param {boolean} props.canSubmit - Có thể submit không
 * @param {Function} props.onFieldChange - Handler khi field thay đổi
 * @param {Function} props.onCreate - Handler tạo mới
 * @param {Function} props.onUpdate - Handler cập nhật
 * @param {Function} props.onDelete - Handler xóa
 * @param {Function} props.onReset - Handler reset form
 */
export function StudentForm({
  form,
  isEditing,
  loading,
  canSubmit,
  onFieldChange,
  onCreate,
  onUpdate,
  onDelete,
  onReset,
}) {
  const handleChange = (field) => (e) => {
    onFieldChange(field, e.target.value);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              {isEditing ? '✏️ Chỉnh sửa sinh viên' : '➕ Thêm sinh viên mới'}
            </h2>
            <p className="mt-1 text-sm text-gray-500">
              {isEditing 
                ? `Đang chỉnh sửa: ${form.student_id}`
                : 'Điền thông tin sinh viên. Chỉ mã SV là bắt buộc.'}
            </p>
          </div>
          {isEditing && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onReset}
              icon={<XMarkIcon className="h-4 w-4" />}
            >
              Hủy
            </Button>
          )}
        </div>
      </CardHeader>

      <CardBody>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Mã sinh viên */}
          <Input
            label="Mã sinh viên *"
            placeholder="VD: SV0001"
            value={form.student_id}
            onChange={handleChange('student_id')}
            disabled={isEditing}
            hint={isEditing ? 'Không thể thay đổi mã SV' : 'Bắt buộc, không trùng lặp'}
          />

          {/* Họ */}
          <Input
            label="Họ"
            placeholder="VD: Nguyễn"
            value={form.last_name}
            onChange={handleChange('last_name')}
          />

          {/* Tên */}
          <Input
            label="Tên"
            placeholder="VD: Văn A"
            value={form.first_name}
            onChange={handleChange('first_name')}
          />

          {/* Email */}
          <Input
            label="Email"
            type="email"
            placeholder="VD: email@example.com"
            value={form.email}
            onChange={handleChange('email')}
          />

          {/* Ngày sinh */}
          <Input
            label="Ngày sinh"
            type="date"
            value={form.birth_date}
            onChange={handleChange('birth_date')}
          />

          {/* Quê quán */}
          <Input
            label="Quê quán"
            placeholder="VD: Hà Nội"
            value={form.hometown}
            onChange={handleChange('hometown')}
          />

          {/* Điểm Toán */}
          <Input
            label="Điểm Toán"
            type="number"
            min="0"
            max="10"
            step="0.1"
            placeholder="0 - 10"
            value={form.math_score}
            onChange={handleChange('math_score')}
          />

          {/* Điểm Văn */}
          <Input
            label="Điểm Văn"
            type="number"
            min="0"
            max="10"
            step="0.1"
            placeholder="0 - 10"
            value={form.literature_score}
            onChange={handleChange('literature_score')}
          />

          {/* Điểm Tiếng Anh */}
          <Input
            label="Điểm Tiếng Anh"
            type="number"
            min="0"
            max="10"
            step="0.1"
            placeholder="0 - 10"
            value={form.english_score}
            onChange={handleChange('english_score')}
          />
        </div>
      </CardBody>

      <CardFooter>
        <div className="flex flex-wrap gap-3">
          {isEditing ? (
            <>
              <Button
                variant="primary"
                onClick={onUpdate}
                disabled={!canSubmit}
                loading={loading}
                icon={<PencilSquareIcon className="h-4 w-4" />}
              >
                Cập nhật
              </Button>
              <Button
                variant="danger"
                onClick={onDelete}
                disabled={loading}
                icon={<TrashIcon className="h-4 w-4" />}
              >
                Xóa
              </Button>
            </>
          ) : (
            <Button
              variant="success"
              onClick={onCreate}
              disabled={!canSubmit}
              loading={loading}
              icon={<UserPlusIcon className="h-4 w-4" />}
            >
              Thêm sinh viên
            </Button>
          )}
          
          <Button
            variant="secondary"
            onClick={onReset}
            disabled={loading}
            icon={<ArrowPathIcon className="h-4 w-4" />}
          >
            {isEditing ? 'Hủy chỉnh sửa' : 'Xóa form'}
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}
