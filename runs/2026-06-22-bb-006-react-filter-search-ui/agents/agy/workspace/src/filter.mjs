export function filterItems(items, query = '', tag = 'all') {
  const lowerQuery = (query || '').toLowerCase();
  return items.filter(item => {
    // Tag filtering
    if (tag && tag !== 'all') {
      if (!item.tags || !item.tags.includes(tag)) {
        return false;
      }
    }
    // Search query filtering (searches title and description case-insensitively)
    const title = (item.title || '').toLowerCase();
    const description = (item.description || '').toLowerCase();
    return title.includes(lowerQuery) || description.includes(lowerQuery);
  });
}
export function emptyStateText() { return 'No matching agents'; }
