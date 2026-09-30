import { render } from 'preact';
import { useEffect, useRef, useState } from 'preact/hooks';
import { Braces, Check, CircleAlert, Copy, Crop, Download, Monitor, Moon, Sun, X } from 'lucide-preact';
import '@fontsource/barlow-semi-condensed/400.css';
import '@fontsource/barlow-semi-condensed/600.css';
import '@fontsource/barlow-semi-condensed/700.css';
import { zipSync } from 'fflate';
import { Cutter } from './Cutter';
import './style.css';

const ACCEPT = ['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'];
const METHODS = {
  transparent: 'transparent edges',
  color_background: 'flat background',
  svg: 'vector bounds',
};
const THEMES = { system: Monitor, light: Sun, dark: Moon };
const NEXT_THEME = { system: 'light', light: 'dark', dark: 'system' };

// lucide 1.x dropped brand icons; this is its former GitHub outline (ISC) so it matches the rest
const GitHub = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 3.5c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

const extension = (name) => name.split('.').pop().toLowerCase();
const area = (size) => size.split('x').reduce((a, b) => a * b, 1);
const dims = (size) => size.replace('x', ' × ');

// images are already compressed, so store them (level 0) instead of deflating again
async function downloadZip(results) {
  const files = {};
  for (const { filename, image } of results) {
    let name = filename;
    for (let n = 2; name in files; n++) name = filename.replace(/(\.\w+)$/, `_${n}$1`);
    files[name] = [new Uint8Array(await (await fetch(image)).arrayBuffer()), { level: 0 }];
  }
  const url = URL.createObjectURL(new Blob([zipSync(files)], { type: 'application/zip' }));
  Object.assign(document.createElement('a'), { href: url, download: 'cropped-images.zip' }).click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function cropFile(file) {
  const body = new FormData();
  body.append('file', file);
  // relative URL keeps reverse-proxy sub-paths working
  const response = await fetch('api/process', { method: 'POST', body });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = Array.isArray(data.detail) ? data.detail[0]?.msg : data.detail;
    throw new Error(detail || `Server responded with ${response.status}`);
  }
  return data;
}

function useTheme() {
  const [theme, setTheme] = useState(() => {
    try { return localStorage.getItem('theme') || 'system'; } catch { return 'system'; }
  });
  useEffect(() => {
    const media = matchMedia('(prefers-color-scheme: dark)');
    const apply = () => {
      document.documentElement.dataset.theme = theme === 'system' ? (media.matches ? 'dark' : 'light') : theme;
    };
    apply();
    try { localStorage.setItem('theme', theme); } catch {}
    media.addEventListener('change', apply);
    return () => media.removeEventListener('change', apply);
  }, [theme]);
  return [theme, () => setTheme(NEXT_THEME[theme])];
}

function App() {
  const [theme, cycleTheme] = useTheme();
  const [items, setItems] = useState([]);
  const [dragging, setDragging] = useState(false);
  const [info, setInfo] = useState(null);
  const input = useRef();
  const nextId = useRef(0);

  const update = (id, patch) => setItems((all) => all.map((it) => (it.id === id ? { ...it, ...patch } : it)));

  const addFiles = (fileList) => {
    for (const file of fileList) {
      const id = nextId.current++;
      const item = { id, name: file.name || 'pasted.png', status: 'processing' };
      setItems((all) => [...all, item]);
      if (!ACCEPT.includes(extension(item.name)) && !file.type.startsWith('image/')) {
        update(id, { status: 'error', error: 'Not an image this tool can crop. Use PNG, JPEG, GIF, WEBP or SVG.' });
        continue;
      }
      cropFile(file.name ? file : new File([file], item.name, { type: file.type }))
        .then((result) => update(id, { status: 'done', result }))
        .catch((error) => update(id, { status: 'error', error: error.message }));
    }
  };

  const remove = (id) => setItems((all) => all.filter((it) => it.id !== id));

  useEffect(() => {
    fetch('api/app-info').then((r) => r.json()).then(setInfo).catch(() => {});

    let depth = 0;
    const hasFiles = (e) => e.dataTransfer?.types.includes('Files');
    const onEnter = (e) => { if (hasFiles(e)) { depth++; setDragging(true); } };
    const onLeave = () => { if (--depth <= 0) { depth = 0; setDragging(false); } };
    const onOver = (e) => { if (hasFiles(e)) e.preventDefault(); };
    const onDrop = (e) => {
      if (!hasFiles(e)) return;
      e.preventDefault();
      depth = 0;
      setDragging(false);
      addFiles(e.dataTransfer.files);
    };
    const onPaste = (e) => { if (e.clipboardData?.files.length) addFiles(e.clipboardData.files); };
    const events = { dragenter: onEnter, dragleave: onLeave, dragover: onOver, drop: onDrop, paste: onPaste };
    Object.entries(events).forEach(([name, fn]) => addEventListener(name, fn));
    return () => Object.entries(events).forEach(([name, fn]) => removeEventListener(name, fn));
  }, []);

  const ThemeIcon = THEMES[theme];
  const browse = () => input.current.click();
  const done = items.filter((it) => it.status === 'done');

  return (
    <>
      <header class="top">
        <a class="brand" href="./"><Crop size={20} strokeWidth={2.25} />CropTransparent</a>
        <p class="tagline">Trims empty edges off images.</p>
        <nav class="tools">
          <a href="docs" target="_blank" rel="noreferrer" title="API documentation" aria-label="API documentation"><Braces size={18} /></a>
          <a href="https://github.com/Pianonic/CropTransparent" target="_blank" rel="noreferrer" title="GitHub" aria-label="GitHub"><GitHub size={18} /></a>
          <button onClick={cycleTheme} title={`Theme: ${theme}`} aria-label={`Theme: ${theme}. Switch to ${NEXT_THEME[theme]}`}>
            <ThemeIcon size={18} />
          </button>
        </nav>
      </header>

      <main class={`mat ${dragging ? 'is-dragging' : ''}`}>
        <input
          ref={input} type="file" multiple hidden accept={ACCEPT.map((e) => `.${e}`).join(',')}
          onChange={(e) => { addFiles(e.currentTarget.files); e.currentTarget.value = ''; }}
        />

        {items.length === 0 ? (
          <div class="empty">
            <h1>Drop images on the mat</h1>
            <p>
              Transparent edges are cut from PNG, WEBP and GIF. Flat backgrounds are cut from JPEG.
              SVGs keep their paths, animated GIFs keep every frame.
            </p>
            <div class="empty-actions">
              <button class="btn primary" onClick={browse}>Choose images</button>
              <span>or paste with <kbd>Ctrl</kbd> <kbd>V</kbd></span>
            </div>
            <Cutter class="cutter" />
          </div>
        ) : (
          <>
            <div class="mat-bar">
              <button class="btn primary" onClick={browse}>Add images</button>
              {done.length > 1 && (
                <button class="btn plain" onClick={() => downloadZip(done.map((it) => it.result))}>
                  <Download size={16} />Download all ({done.length})
                </button>
              )}
              <button class="btn plain clear" onClick={() => setItems([])}>Clear the mat</button>
            </div>
            <div class="pieces">
              {items.map((item) => <Piece key={item.id} item={item} onRemove={() => remove(item.id)} />)}
            </div>
          </>
        )}

        {dragging && <div class="drop-hint"><Cutter class="drop-cutter" />Let go to crop</div>}
      </main>

      <footer class="bottom">
        <span>Images are cropped in memory and never saved.</span>
        <span class="spacer" />
        <a href="https://github.com/Pianonic/CropTransparent/blob/main/LICENSE" target="_blank" rel="noreferrer">MIT licence</a>
        {info && (
          <a href={`https://github.com/Pianonic/CropTransparent/releases/tag/${info.version}`} target="_blank" rel="noreferrer">
            {info.version} ({info.environment})
          </a>
        )}
      </footer>
    </>
  );
}

function ColourChip({ rgb }) {
  const hex = '#' + rgb.map((c) => c.toString(16).padStart(2, '0')).join('');
  const light = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255 > 0.6;
  return (
    <span class="colour" style={{ background: hex, color: light ? '#1d201e' : '#f2f5ef' }} title="Detected background colour">
      {hex.toUpperCase()}
    </span>
  );
}

function Piece({ item, onRemove }) {
  const { status, result } = item;
  const [copied, setCopied] = useState(false);
  const canCopy = result?.output_format === 'png' && typeof ClipboardItem !== 'undefined';

  const copy = async () => {
    const blob = await (await fetch(result.image)).blob();
    await navigator.clipboard.write([new ClipboardItem({ [blob.type]: blob })]);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <article class={`piece is-${status}`}>
      <div class="piece-stage">
        {status === 'processing' && <div class="cutting">Cutting…</div>}
        {status === 'error' && <div class="failed"><CircleAlert size={20} />{item.error}</div>}
        {status === 'done' && (
          <span class="trim">
            <img src={result.image} alt={`${item.name}, cropped`} />
          </span>
        )}
      </div>

      <div class="label">
        <div class="label-head">
          <strong title={item.name}>{item.name}</strong>
          <button class="icon" onClick={onRemove} aria-label={`Remove ${item.name}`}><X size={16} /></button>
        </div>
        {status === 'done' && (
          <>
            <p class="numbers">
              {dims(result.original_size)} to <b>{dims(result.cropped_size)}</b>,{' '}
              {Math.round((1 - area(result.cropped_size) / area(result.original_size)) * 100)}% smaller
            </p>
            <p class="method">
              Cut {METHODS[result.crop_method] || result.crop_method}
              {result.background_color && <ColourChip rgb={result.background_color} />}
            </p>
            <div class="label-actions">
              <a class="btn primary" href={result.image} download={result.filename}><Download size={16} />Download</a>
              {canCopy && (
                <button class={`btn plain square ${copied ? 'is-done' : ''}`} onClick={copy} title={copied ? 'Copied' : 'Copy to clipboard'} aria-label={copied ? 'Copied' : 'Copy to clipboard'}>
                  {copied ? <Check size={16} /> : <Copy size={16} />}
                </button>
              )}
            </div>
          </>
        )}
      </div>
    </article>
  );
}

render(<App />, document.getElementById('app'));
