import {
  FiAlertCircle,
  FiCheckCircle,
  FiInfo,
  FiXCircle,
} from "react-icons/fi";

function NotificationItem({ note }) {
  const getIcon = (type) => {
    switch (type) {
      case "alert":
        return <FiAlertCircle className="text-yellow-400 text-xl" />;
      case "success":
        return <FiCheckCircle className="text-green-400 text-xl" />;
      case "info":
        return <FiInfo className="text-blue-400 text-xl" />;
      case "error":
        return <FiXCircle className="text-red-400 text-xl" />;
      default:
        return <FiInfo className="text-gray-400 text-xl" />;
    }
  };

  return (
    <li className="flex items-start gap-4 bg-gray-900 border border-gray-700 p-4 rounded-xl shadow-md hover:shadow-lg transition hover:scale-[1.01]">
      {getIcon(note.type)}
      <div>
        <p className="text-white font-semibold">{note.message}</p>
        <p className="text-sm text-gray-400 mt-1">
          Tipo: {note.type} • Fonte: {note.source} • {note.timestamp}
        </p>
      </div>
    </li>
  );
}

export default NotificationItem;
