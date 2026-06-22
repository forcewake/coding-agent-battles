export function makeSlug(text, options = {}) {
  const lower = options.lower !== false;
  const source = lower ? text.toLowerCase() : text;
  return source.trim().replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '');
}
