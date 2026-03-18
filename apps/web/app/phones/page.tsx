import Link from 'next/link';

import { Nav } from '../../components/Nav';
import { getJson } from '../../lib/api';

export default async function PhonesPage() {
  const phones = await getJson('/phones');
  return (
    <main>
      <Nav />
      <h2>Phone List / Search</h2>
      <table width="100%" cellPadding={8}>
        <thead>
          <tr>
            <th>Phone model</th><th>Storage</th><th>Condition</th><th>Battery band</th><th>Compare</th>
          </tr>
        </thead>
        <tbody>
          {phones.map((p: any) => (
            <tr key={p.id}>
              <td>{p.model_name}</td>
              <td>{p.storage_gb} GB</td>
              <td>{p.condition_grade}</td>
              <td>{p.battery_health_band}</td>
              <td><Link href={`/phones/${p.id}`}>Open</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
