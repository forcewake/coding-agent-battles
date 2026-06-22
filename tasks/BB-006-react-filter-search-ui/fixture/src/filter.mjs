export function filterItems(items, query = '', tag = 'all') {
  // BUG: title-only, case-sensitive, ignores tag.
  return items.filter(item => item.title.includes(query));
}
export function emptyStateText() { return 'Nothing here'; }
