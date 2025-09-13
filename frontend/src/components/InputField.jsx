export default function InputField({ type, placeholder, value, onChange }) {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className="w-full p-2 mb-4 border rounded"
      value={value}
      onChange={onChange}
    />
  );
}
