/**
 * EmptyState Component
 * 
 * Hiển thị khi không có data.
 */

import React from 'react';

export function EmptyState({
  icon,
  title = 'Không có dữ liệu',
  description = 'Chưa có dữ liệu để hiển thị.',
  action,
}) {
  return (
    <div className="text-center py-12">
      {icon && (
        <div className="mx-auto h-12 w-12 text-gray-400 mb-4">
          {icon}
        </div>
      )}
      <h3 className="text-sm font-medium text-gray-900">{title}</h3>
      <p className="mt-1 text-sm text-gray-500">{description}</p>
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}
