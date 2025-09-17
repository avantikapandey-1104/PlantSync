import React, { useState, useEffect } from 'react';

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/notifications/', {
        headers: {
          'Content-Type': 'application/json',
          // Add auth token header if needed
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to fetch notifications');
      }
      const data = await response.json();
      setNotifications(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (id) => {
    try {
      const response = await fetch(`/notifications/${id}/read/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add auth token header if needed
        },
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Failed to mark notification as read');
      }
      await fetchNotifications();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Notifications</h2>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      {loading ? (
        <p>Loading notifications...</p>
      ) : (
        <ul>
          {notifications.length === 0 && <li>No notifications</li>}
          {notifications.map((notification) => (
            <li
              key={notification.id}
              className={`border-b py-2 flex justify-between items-center ${
                notification.is_read ? 'bg-gray-100' : 'bg-white'
              }`}
            >
              <div>
                <p className="font-semibold">{notification.title}</p>
                <p className="text-sm text-gray-600">{notification.message}</p>
                <p className="text-xs text-gray-400">{new Date(notification.created_at).toLocaleString()}</p>
              </div>
              {!notification.is_read && (
                <button
                  onClick={() => markAsRead(notification.id)}
                  className="text-blue-600 hover:underline"
                >
                  Mark as read
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Notifications;
