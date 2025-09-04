interface Result {
  time: string;
  drawName: string;
  number: string;
}

const results: Result[] = [
  { time: '1:00 PM', drawName: 'Dear Morning', number: '83C 12345' },
  { time: '6:00 PM', drawName: 'Dear Evening', number: '45D 54321' },
  { time: '8:00 PM', drawName: 'Dear Night', number: '99A 98765' },
];

const ResultsTable = () => {
  return (
    <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      <table className="w-full">
        <thead className="bg-blue-800 text-white">
          <tr>
            <th className="py-4 px-6 text-left text-xl font-semibold">Time</th>
            <th className="py-4 px-6 text-left text-xl font-semibold">Draw Name</th>
            <th className="py-4 px-6 text-left text-xl font-semibold">Winning Number</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {results.map((result) => (
            <tr key={result.drawName} className="hover:bg-gray-50">
              <td className="py-6 px-6 text-2xl font-medium text-gray-800">{result.time}</td>
              <td className="py-6 px-6 text-2xl font-medium text-gray-800">{result.drawName}</td>
              <td className="py-6 px-6 text-4xl font-bold text-red-600 tracking-wider">{result.number}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResultsTable;
