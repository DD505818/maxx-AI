export async function fetchState() {
  const res = await fetch('/api/state');
  return res.json();
}
