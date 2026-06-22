import { makeSlug } from '../shared/index.mjs';
export function scenarioPath(name) {
  return `/scenarios/${makeSlug(name, { lower: true })}.html`;
}
