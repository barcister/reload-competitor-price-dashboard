const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function getJson(path: string) {
  const res = await fetch(`${API_BASE}${path}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed ${path}`);
  return res.json();
}
