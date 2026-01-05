/**
 * StudentTable Component
 * 
 * Bảng hiển thị danh sách sinh viên với pagination ảo.
 */

import React from 'react';
import clsx from 'clsx';
import { UserGroupIcon } from '@heroicons/react/24/outline';
import { Card, CardHeader, CardBody } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { EmptyState } from '../ui/EmptyState';
import { LoadingOverlay } from '../ui/Spinner';
import { formatScore, formatDate, getFullName } from '../../utils/helpers';

// Cột trong bảng
const COLUMNS = [
  { key: 'student_id', label: 'Mã SV', width: 'w-24' },
  { key: 'full_name', label: 'Họ tên', width: 'w-40' },
  { key: 'email', label: 'Email', width: 'w-48' },
  { key: 'birth_date', label: 'Ngày sinh', width: 'w-28' },
  { key: 'hometown', label: 'Quê quán', width: 'w-32' },
  { key: 'math_score', label: 'Toán', width: 'w-16', align: 'center' },
  { key: 'literature_score', label: 'Văn', width: 'w-16', align: 'center' },
  { key: 'english_score', label: 'Anh', width: 'w-16', align: 'center' },
];

/**
 * Render điểm số với màu sắc
 */
function ScoreCell({ score }) {
  const numScore = parseFloat(score);
  
  if (isNaN(numScore)) {
    return <span className="text-gray-400">—</span>;
  }
  
  let colorClass = 'text-gray-600';
  if (numScore >= 8) colorClass = 'text-emerald-600 font-semibold';
  else if (numScore >= 6.5) colorClass = 'text-primary-600';
  else if (numScore < 5) colorClass = 'text-red-600';
  
  return <span className={colorClass}>{numScore.toFixed(1)}</span>;
}

/**
 * @param {Object} props
 * @param {Array} props.students - Danh sách sinh viên
 * @param {string|null} props.selectedId - ID đang chọn
 * @param {boolean} props.loading - Loading state
 * @param {Function} props.onSelect - Handler khi click row
 */
export function StudentTable({
  students,
  selectedId,
  loading,
  onSelect,
}) {
  if (loading && students.length === 0) {
    return (
      <Card>
        <CardBody>
          <LoadingOverlay message="Đang tải danh sách sinh viên..." />
        </CardBody>
      </Card>
    );
  }

  if (students.length === 0) {
    return (
      <Card>
        <CardBody>
          <EmptyState
            icon={<UserGroupIcon className="h-12 w-12" />}
            title="Chưa có sinh viên"
            description="Thêm sinh viên mới bằng form bên trên."
          />
        </CardBody>
      </Card>
    );
  }

  return (
    <Card className="overflow-hidden">
      <CardHeader className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">
            📋 Danh sách sinh viên
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Tổng số: <Badge variant="primary">{students.length}</Badge> sinh viên.
            Click vào dòng để chỉnh sửa.
          </p>
        </div>
        {loading && (
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Đang tải...
          </div>
        )}
      </CardHeader>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {COLUMNS.map((col) => (
                <th
                  key={col.key}
                  className={clsx(
                    'px-4 py-3 text-xs font-semibold text-gray-600 uppercase tracking-wider',
                    col.width,
                    col.align === 'center' ? 'text-center' : 'text-left'
                  )}
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          
          <tbody className="bg-white divide-y divide-gray-200">
            {students.map((student) => {
              const isSelected = student.student_id === selectedId;
              
              return (
                <tr
                  key={student.student_id}
                  onClick={() => onSelect(student)}
                  className={clsx(
                    'cursor-pointer transition-colors duration-150',
                    isSelected
                      ? 'bg-primary-50 hover:bg-primary-100'
                      : 'hover:bg-gray-50'
                  )}
                >
                  {/* Mã SV */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className={clsx(
                      'font-mono text-sm font-medium',
                      isSelected ? 'text-primary-700' : 'text-gray-900'
                    )}>
                      {student.student_id}
                    </span>
                  </td>
                  
                  {/* Họ tên */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {getFullName(student)}
                    </div>
                  </td>
                  
                  {/* Email */}
                  <td className="px-4 py-3 whitespace-nowrap">
                    <div className="text-sm text-gray-500 truncate max-w-[200px]">
                      {student.email || <span className="text-gray-400">—</span>}
                    </div>
                  </td>
                  
                  {/* Ngày sinh */}
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                    {student.birth_date ? formatDate(student.birth_date) : <span className="text-gray-400">—</span>}
                  </td>
                  
                  {/* Quê quán */}
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                    {student.hometown || <span className="text-gray-400">—</span>}
                  </td>
                  
                  {/* Điểm */}
                  <td className="px-4 py-3 whitespace-nowrap text-center">
                    <ScoreCell score={student.math_score} />
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-center">
                    <ScoreCell score={student.literature_score} />
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-center">
                    <ScoreCell score={student.english_score} />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
