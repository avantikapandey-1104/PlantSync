import React from 'react';

const HomePage = () => {
  return (
    <div className="text-center mt-20">
      <h2 className="text-4xl font-bold mb-4">Welcome to PlantSync</h2>
      <p className="text-lg text-gray-700 mb-8">
        Upload images of your plants to detect diseases using our AI-powered model.
      </p>
      <img
        src="https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=800&q=80"
        alt="Plant"
        className="mx-auto rounded-lg shadow-lg max-w-md object-contain"
      />
    </div>
  );
};

export default HomePage;
