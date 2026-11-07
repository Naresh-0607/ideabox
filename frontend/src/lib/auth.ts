import { writable } from 'svelte/store';

export const isAuthenticated = writable<boolean>(false);

export function checkAuth(): boolean {
  if (typeof localStorage === 'undefined') return false;
  const token = localStorage.getItem('access_token');
  const authed = !!token;
  isAuthenticated.set(authed);
  return authed;
}

export function setToken(token: string) {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('access_token', token);
  }
  isAuthenticated.set(true);
}

export function logout() {
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem('access_token');
  }
  isAuthenticated.set(false);
  location.href = '/';
}
