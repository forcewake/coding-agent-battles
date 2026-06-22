import assert from 'node:assert/strict';
import test from 'node:test';
import { scenarioPath } from '../index.mjs';
import * as shared from '../../shared/index.mjs';

test('scenario path uses upgraded shared slug API', () => {
  assert.equal(scenarioPath(' BB 008: Dependency Upgrade! '), '/scenarios/bb-008-dependency-upgrade.html');
});
test('old slugify API is not reintroduced', () => {
  assert.equal('slugify' in shared, false);
});
