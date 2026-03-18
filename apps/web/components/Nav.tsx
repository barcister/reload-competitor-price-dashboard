import Link from 'next/link';

const links = [
  ['/', 'Dashboard'],
  ['/phones', 'Phones'],
  ['/provider-status', 'Provider Status'],
  ['/manual-review', 'Manual Review']
];

export function Nav() {
  return (
    <nav style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
      {links.map(([href, label]) => (
        <Link key={href} href={href}>{label}</Link>
      ))}
    </nav>
  );
}
