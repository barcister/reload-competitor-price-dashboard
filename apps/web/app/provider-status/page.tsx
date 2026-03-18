import { Nav } from '../../components/Nav';
import { getJson } from '../../lib/api';

export default async function ProviderStatusPage() {
  const providers = await getJson('/providers');
  return (
    <main>
      <Nav />
      <h2>Provider Status</h2>
      <table width="100%" cellPadding={8}>
        <thead><tr><th>Storefront</th><th>Underlying provider</th><th>Type</th><th>Reliability</th><th>Support level</th></tr></thead>
        <tbody>
          {providers.map((p: any) => (
            <tr key={p.id}>
              <td>{p.storefront_name}</td>
              <td>{p.underlying_provider_name || '-'}</td>
              <td>{p.provider_type}</td>
              <td>{p.reliability_status}</td>
              <td>{p.support_level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
