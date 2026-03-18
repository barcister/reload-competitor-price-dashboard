import { Nav } from '../../components/Nav';
import { getJson } from '../../lib/api';

export default async function ManualReviewPage() {
  const reviews = await getJson('/manual-review');
  return (
    <main>
      <Nav />
      <h2>Manual Review Queue</h2>
      <ul>
        {reviews.map((r: any) => <li key={r.id}>#{r.id} - {r.reason} ({r.status})</li>)}
      </ul>
    </main>
  );
}
