export function filterItems(items, query = '', tag = 'all') {
  const q = (query || '').toLowerCase();
  return items.filter(item => {
    const matchesQuery = !q ||
      String(item.title).toLowerCase().includes(q) ||
      String(item.description).toLowerCase().includes(q);
    const matchesTag = tag === 'all' || (item.tags || []).includes(tag);
    return matchesQuery && matchesTag;
  });
}
export function emptyStateText() { return 'No matching agents'; }
