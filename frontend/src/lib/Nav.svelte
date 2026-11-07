<script lang="ts">
  import { page } from '$app/stores';
  import { logout } from '$lib/auth';

  $: currentPath = $page.url.pathname;
</script>

<!-- Top Desktop/Tablet Navbar -->
<header class="app-nav">
  <div class="nav-container">
    <a href="/" class="brand">
      <svg class="brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="4" stroke="var(--accent)" />
        <line x1="7" y1="8" x2="17" y2="8" stroke="var(--text)" />
        <line x1="7" y1="12" x2="17" y2="12" stroke="var(--text)" />
        <line x1="7" y1="16" x2="13" y2="16" stroke="var(--accent)" />
      </svg>
      <span class="brand-name">IdeaBox</span>
    </a>

    <nav class="nav-links desktop-only" aria-label="Main Navigation">
      <a href="/" class="nav-item" class:active={currentPath === '/'}>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 12l9-9 9 9M5 10v10a1 1 0 001 1h3a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1h3a1 1 0 001-1V10" />
        </svg>
        <span>Home</span>
      </a>
      <a href="/ideas" class="nav-item" class:active={currentPath === '/ideas'}>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="16" rx="2" />
          <line x1="7" y1="9" x2="17" y2="9" />
          <line x1="7" y1="13" x2="17" y2="13" />
          <line x1="7" y1="17" x2="12" y2="17" />
        </svg>
        <span>All Ideas</span>
      </a>
    </nav>

    <div class="nav-actions">
      <button type="button" class="ghost logout-btn" on:click={logout}>
        <span>Log out</span>
      </button>
    </div>
  </div>
</header>

<!-- Mobile Bottom Navigation Bar -->
<nav class="mobile-tab-bar mobile-only" aria-label="Mobile Navigation">
  <a href="/" class="tab-item" class:active={currentPath === '/'}>
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M3 12l9-9 9 9M5 10v10a1 1 0 001 1h3a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1h3a1 1 0 001-1V10" />
    </svg>
    <span>Home</span>
  </a>
  <a href="/ideas" class="tab-item" class:active={currentPath === '/ideas'}>
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <line x1="7" y1="9" x2="17" y2="9" />
      <line x1="7" y1="13" x2="17" y2="13" />
      <line x1="7" y1="17" x2="12" y2="17" />
    </svg>
    <span>All Ideas</span>
  </a>
</nav>
