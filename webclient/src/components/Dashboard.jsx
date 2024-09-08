import React from 'react';

function Dashboard() {
  return (
    <div className="w-full h-screen p-4">
      <div className="grid grid-cols-3 gap-4 h-full">
        {/* Left column */}
        <div className="col-span-1 bg-gray-200 p-4 rounded-lg">
          Left Column
        </div>
        
        <div className="col-span-2 grid grid-cols-2 gap-4">
          {[...Array(8)].map((_, index) => (
            <div key={index} className="bg-gray-200 p-4 rounded-lg hover:bg-gray-300 hover:shadow-md transition-all duration-300 ease-linear">
              Grid Item {index + 1}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;