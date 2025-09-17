import React, { useState, useEffect } from 'react';

function PlantManagement() {
  const [plants, setPlants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    plant_type: '',
    location: '',
    planted_date: '',
    notes: '',
  });
  const [editingPlantId, setEditingPlantId] = useState(null);

  useEffect(() => {
    fetchPlants();
  }, []);

  const fetchPlants = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/userplants/', {
        headers: {
          'Content-Type': 'application/json',
          // Add auth token header if needed
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch plants');
      }
      const data = await response.json();
      setPlants(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const url = editingPlantId ? `/userplants/${editingPlantId}/` : '/userplants/';
      const method = editingPlantId ? 'PUT' : 'POST';
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          // Add auth token header if needed
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) {
        throw new Error('Failed to save plant');
      }
      await fetchPlants();
      setFormData({
        name: '',
        plant_type: '',
        location: '',
        planted_date: '',
        notes: '',
      });
      setEditingPlantId(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEdit = (plant) => {
    setFormData({
      name: plant.name,
      plant_type: plant.plant_type,
      location: plant.location,
      planted_date: plant.planted_date || '',
      notes: plant.notes,
    });
    setEditingPlantId(plant.id);
  };

  const handleDelete = async (id) => {
    setError('');
    try {
      const response = await fetch(`/userplants/${id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          // Add auth token header if needed
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete plant');
      }
      await fetchPlants();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4">My Plants</h2>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      {loading ? (
        <p>Loading plants...</p>
      ) : (
        <>
          <ul className="mb-6">
            {plants.map((plant) => (
              <li key={plant.id} className="border-b py-2 flex justify-between items-center">
                <div>
                  <p className="font-semibold">{plant.name} ({plant.plant_type})</p>
                  <p className="text-sm text-gray-600">{plant.location}</p>
                </div>
                <div className="space-x-2">
                  <button
                    onClick={() => handleEdit(plant)}
                    className="text-blue-600 hover:underline"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(plant.id)}
                    className="text-red-600 hover:underline"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block font-medium">Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block font-medium">Plant Type</label>
              <input
                type="text"
                name="plant_type"
                value={formData.plant_type}
                onChange={handleInputChange}
                required
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block font-medium">Location</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block font-medium">Planted Date</label>
              <input
                type="date"
                name="planted_date"
                value={formData.planted_date}
                onChange={handleInputChange}
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block font-medium">Notes</label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleInputChange}
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <button
              type="submit"
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            >
              {editingPlantId ? 'Update Plant' : 'Add Plant'}
            </button>
          </form>
        </>
      )}
    </div>
  );
}

export default PlantManagement;
