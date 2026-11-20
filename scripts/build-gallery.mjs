// Scans public/gallery for images and writes public/gallery.json.
// Runs automatically on every Vercel deploy (see vercel.json).
import { readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const dir = join(process.cwd(), 'public', 'gallery');
const exts = /\.(jpe?g|png|webp|avif|gif)$/i;
const files = readdirSync(dir)
  .filter((f) => exts.test(f) && !f.startsWith('.'))
  .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));

const list = files.map((f) => '/gallery/' + encodeURIComponent(f));
writeFileSync(join(process.cwd(), 'public', 'gallery.json'), JSON.stringify(list, null, 2));
console.log(`gallery.json: ${list.length} photo(s)`);
