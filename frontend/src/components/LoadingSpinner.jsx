function LoadingSpinner({ message = "Loading..." }) {
  return (
    <div className="flex items-center gap-2 text-blue-600 animate-pulse">
      <svg
        className="w-5 h-5 animate-spin"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
      >
        <circle cx="12" cy="12" r="10" strokeWidth="4" strokeOpacity="0.25" />
        <path
          d="M12 2a10 10 0 0 1 10 10"
          strokeWidth="4"
          strokeLinecap="round"
        />
      </svg>
      <span className="font-medium">{message}</span>
    </div>
  );
}

export default LoadingSpinner;
