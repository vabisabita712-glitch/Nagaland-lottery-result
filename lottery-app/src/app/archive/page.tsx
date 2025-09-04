const ArchivePage = () => {
  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold">Past Results</h2>
      <ul className="space-y-4">
        <li className="p-4 bg-white rounded-lg shadow">
          <p className="font-semibold text-xl">September 3, 2025</p>
          <p className="text-gray-600">Morning: 12345, Day: 67890, Evening: 11223</p>
        </li>
        <li className="p-4 bg-white rounded-lg shadow">
          <p className="font-semibold text-xl">September 2, 2025</p>
          <p className="text-gray-600">Morning: 54321, Day: 09876, Evening: 32211</p>
        </li>
        <li className="p-4 bg-white rounded-lg shadow">
          <p className="font-semibold text-xl">September 1, 2025</p>
          <p className="text-gray-600">Morning: 67890, Day: 12345, Evening: 44556</p>
        </li>
      </ul>
    </div>
  );
};

export default ArchivePage;
