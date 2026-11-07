const API_URL = import.meta.env.VITE_API_URL ?? '';
export type Status = 'Inbox' | 'Parked' | 'Active' | 'Completed';
export type Idea = { id: number; title: string; description: string | null; tags: string[]; status: Status; created_at: string; updated_at: string };

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  if (options.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  const token = typeof localStorage !== 'undefined' ? localStorage.getItem('access_token') : null;
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? 'Something went wrong');
  }
  return response.status === 204 ? (undefined as T) : response.json();
}
