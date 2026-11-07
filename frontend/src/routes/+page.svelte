<script lang="ts">
  import { onMount } from 'svelte';
  import { api, type Idea, type Status } from '$lib/api';
  import { isAuthenticated, checkAuth, setToken } from '$lib/auth';

  const statuses: Status[] = ['Inbox', 'Active', 'Parked', 'Completed'];

  // Auth State
  let email = '';
  let password = '';
  let mode: 'login' | 'register' = 'login';
  let authError = '';
  let authLoading = false;

  // Home Dashboard State
  let ideas: Idea[] = [];
  let loadingIdeas = true;
  let quickTitle = '';
  let quickDesc = '';
  let quickSaving = false;
  let quickSuccess = '';
  let quickError = '';

  $: counts = Object.fromEntries(statuses.map(s => [s, ideas.filter(i => i.status === s).length]));
  $: recentIdeas = ideas.slice(0, 4);

  async function loadDashboard() {
    loadingIdeas = true;
    try {
      ideas = await api<Idea[]>('/api/ideas');
    } catch {
      // If token expired or network error
    } finally {
      loadingIdeas = false;
    }
  }

  async function submitAuth() {
    authLoading = true;
    authError = '';
    try {
      if (mode === 'register') {
        await api('/api/auth/register', {
          method: 'POST',
          body: JSON.stringify({ email, password })
        });
      }
      const body = new URLSearchParams({ username: email, password });
      const result = await api<{ access_token: string }>('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body
      });
      setToken(result.access_token);
      await loadDashboard();
    } catch (e) {
      authError = e instanceof Error ? e.message : 'Unable to continue';
    } finally {
      authLoading = false;
    }
  }

  async function quickCapture() {
    if (!quickTitle.trim()) return;
    quickSaving = true;
    quickError = '';
    quickSuccess = '';
    try {
      const newIdea = await api<Idea>('/api/ideas', {
        method: 'POST',
        body: JSON.stringify({
          title: quickTitle.trim(),
          description: quickDesc.trim() || null,
          tags: ['quick-capture'],
          status: 'Inbox'
        })
      });
      ideas = [newIdea, ...ideas];
      quickTitle = '';
      quickDesc = '';
      quickSuccess = 'Idea saved to Inbox!';
      setTimeout(() => { quickSuccess = ''; }, 3000);
    } catch (e) {
      quickError = e instanceof Error ? e.message : 'Failed to save idea';
    } finally {
      quickSaving = false;
    }
  }

  async function updateStatus(idea: Idea, newStatus: Status) {
    try {
      const updated = await api<Idea>(`/api/ideas/${idea.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          title: idea.title,
          description: idea.description,
          tags: idea.tags,
          status: newStatus
        })
      });
      ideas = ideas.map(i => i.id === updated.id ? updated : i);
    } catch {
      // Fallback
    }
  }

  onMount(() => {
    if (checkAuth()) {
      loadDashboard();
    }
  });
</script>

<svelte:head>
  <title>{$isAuthenticated ? 'Home · IdeaBox' : 'Log in · IdeaBox'}</title>
</svelte:head>

{#if !$isAuthenticated}
  <!-- Unauthenticated: Login / Register View -->
  <main class="auth-shell">
    <section class="auth-card">
      <div class="auth-brand">IdeaBox</div>
      <h1>{mode === 'login' ? 'Log in' : 'Create account'}</h1>
      <p class="muted">{mode === 'login' ? 'Access your private workspace.' : 'Start capturing ideas in seconds.'}</p>
      
      <form on:submit|preventDefault={submitAuth}>
        <label>
          Email
          <input type="email" bind:value={email} required autocomplete="email" placeholder="you@example.com" />
        </label>
        <label>
          Password
          <input type="password" bind:value={password} required minlength="8" autocomplete={mode === 'login' ? 'current-password' : 'new-password'} placeholder="At least 8 characters" />
        </label>
        {#if authError}<p class="error" role="alert">{authError}</p>{/if}
        <button type="submit" disabled={authLoading}>
          {authLoading ? 'Working…' : mode === 'login' ? 'Continue' : 'Create account'}
        </button>
      </form>

      <button type="button" class="link-button auth-switch" on:click={() => { mode = mode === 'login' ? 'register' : 'login'; authError = ''; }}>
        {mode === 'login' ? 'Need an account? Register' : 'Already have an account? Log in'}
      </button>
    </section>
  </main>
{:else}
  <!-- Authenticated: Home Screen Dashboard -->
  <main class="app-shell">
    <section class="home-hero">
      <h1>Dashboard</h1>
      <p>Quickly capture what's on your mind or browse your collection.</p>
    </section>

    <!-- Fast Idea Capture Box -->
    <section class="quick-capture-card" aria-label="Quick capture idea">
      <h2>
        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="16" />
          <line x1="8" y1="12" x2="16" y2="12" />
        </svg>
        Quick Idea Capture
      </h2>
      <form class="quick-capture-form" on:submit|preventDefault={quickCapture}>
        <input 
          bind:value={quickTitle} 
          required 
          maxlength="200" 
          placeholder="What's the idea?" 
          aria-label="Idea title" 
        />
        <input 
          bind:value={quickDesc} 
          maxlength="1000" 
          placeholder="Optional notes or details…" 
          aria-label="Idea notes" 
        />
        <div class="quick-capture-actions">
          <div>
            {#if quickSuccess}<span class="quick-capture-status">{quickSuccess}</span>{/if}
            {#if quickError}<span class="error">{quickError}</span>{/if}
          </div>
          <button type="submit" disabled={quickSaving || !quickTitle.trim()}>
            {quickSaving ? 'Saving…' : 'Capture Idea'}
          </button>
        </div>
      </form>
    </section>

    <!-- Overview Counters -->
    <div class="section-header">
      <h2>Overview</h2>
      <a href="/ideas" class="link-button">View All ({ideas.length}) →</a>
    </div>

    <section class="stats" aria-label="Idea counts">
      <a href="/ideas" class="stat">
        <span>Total Ideas</span>
        <strong>{ideas.length}</strong>
      </a>
      {#each statuses as status}
        <a href="/ideas?status={status}" class="stat">
          <span>{status}</span>
          <strong>{counts[status] ?? 0}</strong>
        </a>
      {/each}
    </section>

    <!-- Recent Ideas Preview -->
    <div class="section-header">
      <h2>Recent Ideas</h2>
      {#if ideas.length > 4}
        <a href="/ideas" class="link-button">Browse catalog →</a>
      {/if}
    </div>

    {#if loadingIdeas}
      <p class="muted">Loading dashboard…</p>
    {:else if !recentIdeas.length}
      <section class="empty">
        <h2>Your idea box is empty</h2>
        <p class="muted">Use the quick capture above to save your first idea!</p>
      </section>
    {:else}
      <section class="idea-grid" aria-label="Recent ideas">
        {#each recentIdeas as idea}
          <article class="idea-card">
            <div class="card-top">
              <span class="badge status-{idea.status.toLowerCase()}">{idea.status}</span>
            </div>
            <h2>{idea.title}</h2>
            {#if idea.description}<p class="muted">{idea.description}</p>{/if}
            {#if idea.tags.length}
              <div class="tags">
                {#each idea.tags as tag}<span>#{tag}</span>{/each}
              </div>
            {/if}
            <footer>
              <select 
                value={idea.status} 
                aria-label={`Status for ${idea.title}`} 
                on:change={(e) => updateStatus(idea, (e.currentTarget as HTMLSelectElement).value as Status)}
              >
                {#each statuses as status}<option>{status}</option>{/each}
              </select>
              <a href="/ideas" class="link-button">Edit in Ideas →</a>
            </footer>
          </article>
        {/each}
      </section>
    {/if}
  </main>
{/if}
