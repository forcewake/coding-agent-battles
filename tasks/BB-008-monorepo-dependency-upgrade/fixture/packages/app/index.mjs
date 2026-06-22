import { slugify } from '../shared/index.mjs';
export function scenarioPath(name) {
  return `/scenarios/${slugify(name)}.html`;
}
