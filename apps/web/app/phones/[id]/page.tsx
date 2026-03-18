import { Nav } from '../../../components/Nav';
import { getJson } from '../../../lib/api';

export default async function PhoneComparePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const compare = await getJson(`/offers/${id}/compare`);
  const history = await getJson(`/offers/${id}/history`);

  return (
    <main>
      <Nav />
      <h2>Comparison Detail #{id}</h2>
      <p>Median market price: {compare.median_market_price} CHF</p>
      <p>Price spread: {compare.price_spread} CHF</p>
      {compare.comparability_warning && <p style={{ color: 'orange' }}>{compare.comparability_warning}</p>}

      <table width="100%" cellPadding={8}>
        <thead>
          <tr>
            <th>Rank</th><th>Raw title</th><th>Normalized title</th><th>Item</th><th>Shipping</th><th>Effective</th><th>Confidence</th><th>Source</th>
          </tr>
        </thead>
        <tbody>
          {compare.offers.map((offer: any) => (
            <tr key={offer.offer_id}>
              <td>{offer.rank}</td>
              <td>{offer.raw_title}</td>
              <td>{offer.normalized_title}</td>
              <td>{offer.item_price}</td>
              <td>{offer.shipping_price}</td>
              <td>{offer.effective_total_price}</td>
              <td>{Math.round(offer.matching_confidence * 100)}%</td>
              <td><a href={offer.source_url}>source</a></td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Price history (simple chart data)</h3>
      <pre>{JSON.stringify(history, null, 2)}</pre>
    </main>
  );
}
