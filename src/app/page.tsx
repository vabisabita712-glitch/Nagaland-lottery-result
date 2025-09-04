import ResultsTable from '@/components/ResultsTable';
import AdPlaceholder from '@/components/AdPlaceholder';

export default function Home() {
  return (
    <div className="space-y-8">
      <section className="text-center">
        <h2 className="text-4xl font-extrabold text-gray-900">Today's Results</h2>
        <p className="mt-2 text-lg text-gray-600">
          Official results for the Nagaland State Lottery.
        </p>
      </section>

      <AdPlaceholder className="mx-auto max-w-4xl" />

      <section>
        <ResultsTable />
      </section>

      <AdPlaceholder className="mx-auto max-w-4xl" />
    </div>
  );
}
