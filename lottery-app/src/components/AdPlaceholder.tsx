const AdPlaceholder = ({ className = '' }: { className?: string }) => {
  return (
    <div
      className={`bg-gray-200 border border-dashed border-gray-400 flex items-center justify-center text-gray-500 ${className}`}
      style={{ minHeight: '100px' }}
    >
      Ad Placeholder
    </div>
  );
};

export default AdPlaceholder;
