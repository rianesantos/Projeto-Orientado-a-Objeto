import { useEffect, useState } from "react";
import api from "../services/api";
import PageWrapper from "../components/PageWrapper";
import NotificationItem from "../components/NotificationItem";
import LoadingSpinner from "../components/LoadingSpinner";
import { FiBell } from "react-icons/fi";

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    api.get("/notifications/1")
      .then((res) => {
        setNotifications(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading notifications:", err);
        setError(true);
        setLoading(false);
      });
  }, []);

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white flex items-center gap-2">
          <FiBell className="text-purple-400" />
          Notificações
        </h1>
        <p className="text-purple-400 mt-2 text-lg">Acompanhe alertas, atualizações e mensagens importantes</p>
      </div>

      {loading && <LoadingSpinner message="Carregando notificações..." />}
      {error && <p className="text-red-500">Falha ao carregar notificações.</p>}

      {!loading && !error && notifications.length > 0 && (
        <ul className="space-y-4">
          {notifications.map((note) => (
            <NotificationItem key={note.id} note={note} />
          ))}
        </ul>
      )}

      {!loading && !error && notifications.length === 0 && (
        <p className="text-gray-400">Nenhuma notificação no momento.</p>
      )}
    </PageWrapper>
  );
}

export default Notifications;
