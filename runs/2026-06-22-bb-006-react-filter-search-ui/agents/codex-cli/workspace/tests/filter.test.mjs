import assert from 'node:assert/strict';
import test from 'node:test';
import { filterItems, emptyStateText } from '../src/filter.mjs';

const items = [
  { title: 'OpenCode', description: 'fast GLM coding lane', tags: ['fast', 'cheap'] },
  { title: 'Codex', description: 'robust reasoning', tags: ['robust'] },
  { title: 'Pi', description: 'cost-process champion', tags: ['cheap'] },
];

test('query searches title and description case-insensitively', () => {
  assert.deepEqual(filterItems(items, 'GLM', 'all').map(x => x.title), ['OpenCode']);
  assert.deepEqual(filterItems(items, 'reason', 'all').map(x => x.title), ['Codex']);
});

test('tag filter combines with query and keeps order', () => {
  assert.deepEqual(filterItems(items, '', 'cheap').map(x => x.title), ['OpenCode', 'Pi']);
  assert.deepEqual(filterItems(items, 'code', 'cheap').map(x => x.title), ['OpenCode']);
});

test('empty state copy is product quality', () => {
  assert.equal(emptyStateText(), 'No matching agents');
});
