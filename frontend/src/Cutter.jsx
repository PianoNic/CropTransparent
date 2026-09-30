// Aluminium snap-off utility knife, drawn pointing right. Size and rotation come from CSS.
const range = (from, to, step) => Array.from({ length: Math.floor((to - from) / step) + 1 }, (_, i) => from + i * step);

export function Cutter(props) {
  return (
    <svg viewBox="0 0 410 72" aria-hidden="true" {...props}>
      <defs>
        <linearGradient id="cutter-alu" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#f1f3f4" />
          <stop offset="0.45" stop-color="#c9cfd3" />
          <stop offset="0.7" stop-color="#e2e6e8" />
          <stop offset="1" stop-color="#9ea6ab" />
        </linearGradient>
        <linearGradient id="cutter-blade" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#e4e8ea" />
          <stop offset="1" stop-color="#b3bbc0" />
        </linearGradient>
      </defs>

      <g stroke="#737c82" stroke-width="0.75">
        <path d="M100 27 H382 L398 44 H100 Z" fill="url(#cutter-blade)" />
        <path d="M396.5 42.5 L382 27" stroke="#f7f9fa" stroke-width="1.2" />
        {range(128, 370, 22).map((x) => <path key={x} d={`M${x} 27 L${x + 18} 44`} />)}

        {range(118, 330, 13).map((x) => <rect key={x} x={x} y="9" width="6" height="9" rx="1.5" fill="url(#cutter-alu)" />)}
        <path d="M46 15 H342 L352 21 V27 H46 Z" fill="url(#cutter-alu)" />

        {range(52, 160, 13).map((x) => <rect key={x} x={x} y="52" width="6" height="9" rx="1.5" fill="url(#cutter-alu)" />)}
        <path d="M46 44 H334 L326 50 H240 L228 55 H46 Z" fill="url(#cutter-alu)" />

        <path
          d="M52 14 Q30 14 22 30 L12 50 A14 14 0 0 0 38 62 L50 56 Z M24 52 A5 5 0 1 0 34 52 A5 5 0 1 0 24 52 Z"
          fill="url(#cutter-alu)"
          fill-rule="evenodd"
        />
        <path d="M52 16 Q36 16 29 28 L24 38 H46 V27 Z" fill="#2b2f31" stroke="none" />
      </g>

      <circle cx="146" cy="35.5" r="3.5" fill="#1b1e1f" />
      <rect x="78" y="22" width="58" height="26" rx="4" fill="#2b2f31" />
      <g stroke="#4a5054" stroke-width="1.5">
        {range(86, 128, 5).map((x) => <path key={x} d={`M${x} 26 V44`} />)}
      </g>
    </svg>
  );
}
