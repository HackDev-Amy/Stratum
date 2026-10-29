export default function Card({ title, right, children, className = "" }) {
  return (
    <div className={`glass rounded-2xl p-5 ${className}`}>
      {(title || right) && (
        <div className="flex items-center justify-between mb-4">
          {title && (
            <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">
              {title}
            </h3>
          )}
          {right}
        </div>
      )}
      {children}
    </div>
  );
}