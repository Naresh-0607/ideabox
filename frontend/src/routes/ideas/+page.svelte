<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { api, type Idea, type Status } from '$lib/api';
  import { checkAuth } from '$lib/auth';

  const statuses: Status[] = ['Inbox', 'Active', 'Parked', 'Completed'];
  let ideas: Idea[] = [];
  let title = '';
  let description = '';
  let tags = '';
  let selectedStatus: Status = 'Inbox';
  let search = '';
  let filter = '';
  let tagFilter = '';
  let error = '';
  let editing: Idea | null = null;
  let showForm = false;
  let loading = true;

  // Read initial query param if present
  $: initialStatus = $page.url.searchParams.get('status');
  $: if (initialStatus && statuses.includes(initialStatus as Status) && !filter) {
    filter = initialStatus;
  }

  $: filtered = ideas.filter(i => 
    (!search || i.title.toLowerCase().includes(search.toLowerCase()) || (i.description && i.description.toLowerCase().includes(search.toLowerCase()))) &&
    (!filter || i.status === filter) &&
    (!tagFilter || i.tags.some(t => t.toLowerCase().includes(tagFilter.toLowerCase())))
  );

  $: counts = Object.fromEntries(statuses.map(s => [s, ideas.filter(i => i.status === s).length]));

  async function load() {
    try {
      ideas = await api<Idea[]>('/api/ideas');
    } catch (e) {
      error = e instanceof Error ? e.message : 'Unable to load ideas';
    } finally {
      loading = false;
    }
  }

  function openForm(idea?: Idea) {
    editing = idea ?? null;
    title = idea?.title ?? '';
    description = idea?.description ?? '';
    tags = idea?.tags.join(', ') ?? '';
    selectedStatus = idea?.status ?? 'Inbox';
    showForm = true;
  }

  async function save() {
    error = '';
    try {
      const payload = {
        title,
        description: description || null,
        tags: tags.split(',').map(t => t.trim()).filter(Boolean),
        status: selectedStatus
      };
      if (editing) {
        await api(`/api/ideas/${editing.id}`, { method: 'PUT', body: JSON.stringify(payload) });
      } else {
        await api('/api/ideas', { method: 'POST', body: JSON.stringify(payload) });
      }
      showForm = false;
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Unable to save idea';
    }
  }

  async function remove(idea: Idea) {
    if (!confirm(`Delete "${idea.title}"?`)) return;
    try {
      await api(`/api/ideas/${idea.id}`, { method: 'DELETE' });
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Unable to delete idea';
    }
  }

  async function changeStatus(idea: Idea, status: Status) {
    try {
      await api(`/api/ideas/${idea.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          title: idea.title,
          description: idea.description,
          tags: idea.tags,
          status
        })
      });
      await load();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Unable to update status';
    }
  }

  onMount(() => {
    if (!checkAuth()) {
      goto('/');
      return;
    }
    load();
  });
</script>

<svelte:head>
  <title>All Ideas · IdeaBox</title>
</svelte:head>

<main class="app-shell">
  <header class="topbar">
    <div>
      <h1>All Ideas</h1>
      <p class="muted">{ideas.length} total saved ideas</p>
    </div>
    <div class="actions">
      <button type="button" on:click={() => openForm()}>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        <span>New Idea</span>
      </button>
    </div>
  </header>

  <!-- Filter by clicking status cards -->
  <section class="stats" aria-label="Idea counts">
    {#each statuses as status}
      <button 
        type="button" 
        class="stat" 
        style="text-align: left; cursor: pointer; border-color: {filter === status ? 'var(--accent)' : 'var(--border)'};"
        on:click={() => { filter = filter === status ? '' : status; }}
      >
        <span>{status}</span>
        <strong>{counts[status] ?? 0}</strong>
      </button>
    {/each}
  </section>

  <!-- Search & Filter Controls -->
  <section class="toolbar" aria-label="Filters">
    <input 
      placeholder="Search titles or notes…" 
      bind:value={search} 
      aria-label="Search ideas" 
    />
    <select bind:value={filter} aria-label="Filter by status">
      <option value="">All statuses</option>
      {#each statuses as status}
        <option value={status}>{status}</option>
      {/each}
    </select>
    <input 
      placeholder="Filter by #tag…" 
      bind:value={tagFilter} 
      aria-label="Filter by tag" 
    />
  </section>

  {#if error}<p class="error" role="alert">{error}</p>{/if}

  {#if loading}
    <p class="muted">Loading ideas…</p>
  {:else if !filtered.length}
    <section class="empty">
      <h2>{ideas.length ? 'No matching ideas found' : 'No ideas yet'}</h2>
      <p class="muted">
        {ideas.length 
          ? 'Try adjusting your search query or status filter.' 
          : 'Add your first idea to get started.'}
      </p>
      <button type="button" on:click={() => openForm()}>Create an Idea</button>
    </section>
  {:else}
    <section class="idea-grid" aria-label="Ideas">
      {#each filtered as idea}
        <article class="idea-card">
          <div class="card-top">
            <span class="badge status-{idea.status.toLowerCase()}">{idea.status}</span>
            <button 
              type="button" 
              class="icon-button" 
              aria-label={`Delete ${idea.title}`} 
              on:click={() => remove(idea)}
            >×</button>
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
              on:change={(e) => changeStatus(idea, (e.currentTarget as HTMLSelectElement).value as Status)}
            >
              {#each statuses as status}<option>{status}</option>{/each}
            </select>
            <button type="button" class="link-button" on:click={() => openForm(idea)}>Edit</button>
          </footer>
        </article>
      {/each}
    </section>
  {/if}
</main>

<!-- Add / Edit Modal -->
{#if showForm}
  <div 
    class="modal-backdrop" 
    role="presentation" 
    on:click={(e) => e.target === e.currentTarget && (showForm = false)}
  >
    <section class="modal" aria-label={editing ? 'Edit idea' : 'New idea'}>
      <div class="modal-header">
        <h2>{editing ? 'Edit Idea' : 'New Idea'}</h2>
        <button type="button" class="icon-button" aria-label="Close" on:click={() => showForm = false}>×</button>
      </div>
      <form on:submit|preventDefault={save}>
        <label>
          Title
          <input bind:value={title} required maxlength="200" placeholder="Idea title" />
        </label>
        <label>
          Description
          <textarea bind:value={description} rows="4" maxlength="10000" placeholder="Detailed thoughts, notes, links…"></textarea>
        </label>
        <label>
          Tags
          <input bind:value={tags} placeholder="tech, business, personal (comma separated)" />
        </label>
        <label>
          Status
          <select bind:value={selectedStatus}>
            {#each statuses as status}<option>{status}</option>{/each}
          </select>
        </label>
        <button type="submit">{editing ? 'Save Changes' : 'Create Idea'}</button>
      </form>
    </section>
  </div>
{/if}
