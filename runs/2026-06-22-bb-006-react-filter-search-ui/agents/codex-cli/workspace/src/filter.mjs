export function filterItems(items, query = '', tag = 'all') {
  const normalizedQuery = query.toLowerCase();
  const normalizedTag = tag.toLowerCase();

  return items.filter(item => {
    const title = item.title.toLowerCase();
    const description = item.description.toLowerCase();
    const matchesQuery = title.includes(normalizedQuery) || description.includes(normalizedQuery);
    const matchesTag = normalizedTag === 'all' || item.tags.some(itemTag => itemTag.toLowerCase() === normalizedTag);

    return matchesQuery && matchesTag;
  });
}
export function emptyStateText() { return 'No matching agents'; }
