import { Nav } from '../components/Nav';
import { getJson } from '../lib/api';

export default async function DashboardPage() {
  const summary = await getJson('/dashboard/summary');
  return (
    <main>
      <Nav />
      <h1>Swiss Phone Price Intelligence</h1>
      <ul>
        <li>Providers: {summary.provider_count}</li>
        <li>Offers: {summary.offer_count}</li>
        <li>Average Effective Price: {summary.average_effective_price ?? 'n/a'} CHF</li>
      </ul>
    </main>
  );
}
