/**
 * Munder Difflin Procedural Pixel-Art Portrait & Sprite Engine
 * Ported directly from scratch/munder-difflin/src/renderer/src/scene/office/portraitArt.ts
 * Generates exact 18x28 pixel bust portraits and 18x32 scene sprites for all 15 characters:
 * michael, jim, pam, dwight, kevin, angela, oscar, stanley, phyllis, andy, kelly, ryan, toby, creed, meredith
 */

(function (window) {
  'use strict';

  const PORTRAIT_W = 18;
  const PORTRAIT_H = 28;
  const SCENE_W = 18;
  const SCENE_H = 32;
  const OUTLINE = [38, 34, 46];
  const HX0 = 4, HX1 = 13; // head skin columns

  let CUR_W = PORTRAIT_W;
  let CUR_H = PORTRAIT_H;

  const clamp = (v) => (v < 0 ? 0 : v > 255 ? 255 : Math.round(v));
  function shades(rgb, dl = 1.22, dd = 0.68) {
    return [
      [clamp(rgb[0] * dl), clamp(rgb[1] * dl), clamp(rgb[2] * dl)],
      [rgb[0], rgb[1], rgb[2]],
      [clamp(rgb[0] * dd), clamp(rgb[1] * dd), clamp(rgb[2] * dd)],
    ];
  }

  function set(buf, x, y, c, a = 255) {
    if (x < 0 || x >= CUR_W || y < 0 || y >= CUR_H) return;
    const i = (y * CUR_W + x) * 4;
    buf[i] = c[0]; buf[i + 1] = c[1]; buf[i + 2] = c[2]; buf[i + 3] = a;
  }
  function alphaAt(buf, x, y) {
    if (x < 0 || x >= CUR_W || y < 0 || y >= CUR_H) return 0;
    return buf[(y * CUR_W + x) * 4 + 3];
  }
  function rgbAt(buf, x, y) {
    const i = (y * CUR_W + x) * 4;
    return [buf[i], buf[i + 1], buf[i + 2]];
  }
  function eq(a, b) { return a[0] === b[0] && a[1] === b[1] && a[2] === b[2]; }
  function rect(buf, x0, y0, x1, y1, c) {
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) set(buf, x, y, c);
    }
  }

  // Palettes
  const SKIN = {
    light: { hi: [255, 221, 189], base: [247, 201, 170], sh: [212, 158, 126], line: [168, 112, 82] },
    tan:   { hi: [232, 182, 136], base: [214, 162, 116], sh: [176, 126, 86],  line: [138, 92, 60] },
    brown: { hi: [180, 130, 94],  base: [158, 112, 78],  sh: [124, 86, 58],   line: [90, 60, 40] },
    dark:  { hi: [142, 98, 70],   base: [120, 80, 56],   sh: [94, 62, 42],    line: [64, 42, 28] },
  };

  function drawHead(buf, skin) {
    const s = SKIN[skin];
    for (let y = 4; y <= 16; y++) {
      for (let x = HX0; x <= HX1; x++) {
        if (((x === HX0 || x === HX1) && (y === 4 || y === 5 || y === 16)) || ((x === 5 || x === 12) && y === 4)) continue;
        set(buf, x, y, s.base);
      }
    }
    for (let y = 6; y < 12; y++) set(buf, 5, y, s.hi);
    set(buf, 6, 5, s.hi); set(buf, 7, 5, s.hi);
    for (let y = 6; y < 15; y++) set(buf, 12, y, s.sh);
    for (const x of [7, 8, 9, 10, 11]) set(buf, x, 16, s.sh);
    for (const ex of [HX0 - 1, HX1 + 1]) { set(buf, ex, 9, s.base); set(buf, ex, 10, s.base); set(buf, ex, 11, s.sh); }
    rect(buf, 7, 17, 10, 18, s.sh); rect(buf, 7, 17, 9, 17, s.base);
  }

  function drawFace(buf, skin, brow, mouth, blush, lashes = false) {
    const s = SKIN[skin];
    const white = [250, 248, 244], pup = [46, 38, 42];
    for (const [a, b, p] of [[5, 6, 6], [10, 11, 10]]) {
      set(buf, a, 9, white); set(buf, b, 9, white); set(buf, p, 9, pup);
    }
    if (lashes) {
      const lash = [54, 40, 48], glint = [252, 250, 248];
      for (const x of [5, 6, 10, 11]) set(buf, x, 8, lash);
      set(buf, 4, 8, lash); set(buf, 12, 8, lash);
      set(buf, 5, 9, glint); set(buf, 10, 9, glint);
    }
    if (brow === 'flat') for (const x of [5, 6, 10, 11]) set(buf, x, 7, s.line);
    else if (brow === 'angry') { set(buf, 5, 8, s.line); set(buf, 6, 7, s.line); set(buf, 10, 7, s.line); set(buf, 11, 8, s.line); }
    else if (brow === 'raised') for (const x of [5, 6, 10, 11]) set(buf, x, 6, s.line);
    else if (brow === 'soft') { for (const x of [5, 11]) set(buf, x, 7, s.line); for (const x of [6, 10]) set(buf, x, 7, s.sh); }
    set(buf, 8, 11, s.sh); set(buf, 8, 12, s.sh); set(buf, 7, 12, s.sh);
    const mc = [158, 86, 80];
    const mouths = {
      neutral: [[7, 14], [8, 14], [9, 14], [10, 14]],
      smile: [[7, 14], [8, 14], [9, 14], [10, 14], [6, 13], [11, 13]],
      frown: [[7, 15], [8, 15], [9, 15], [10, 15], [6, 14], [11, 14]],
      grin: [[7, 14], [8, 14], [9, 14], [10, 14], [7, 13], [8, 13], [9, 13], [10, 13], [6, 13], [11, 13]],
    };
    for (const [x, y] of (mouths[mouth] || mouths.neutral)) set(buf, x, y, mc);
    if (blush) for (const x of [5, 12]) set(buf, x, 12, [235, 150, 140], 140);
  }

  // Hairstyles
  const styleShort = (buf, color, skinBase, a) => {
    const [hi, base, sh] = shades(color);
    const part = a.part || 'L', recede = a.recede || 0;
    rect(buf, HX0, 2, HX1, 4, base);
    for (let x = HX0 - 1; x <= HX1 + 1; x++) set(buf, x, 3, base);
    rect(buf, HX0 - 1, 4, HX1 + 1, 5, base);
    for (let y = 6; y < 9; y++) { set(buf, HX0 - 1, y, base); set(buf, HX0, y, base); set(buf, HX1, y, base); set(buf, HX1 + 1, y, base); }
    for (let x = HX0; x <= HX1; x++) set(buf, x, 5, base);
    if (recede) {
      for (let y = 3; y < 6; y++) for (let x = 6; x < 12; x++) if (eq(rgbAt(buf, x, y), base)) set(buf, x, y, skinBase);
      set(buf, 8, 5, base);
    }
    const hx = part === 'L' ? 6 : 11;
    for (let y = 2; y < 6; y++) set(buf, hx, y, sh);
    for (let x = HX0; x < hx; x++) if (alphaAt(buf, x, 3)) set(buf, x, 3, hi);
    for (let x = HX0; x <= HX1; x++) if (alphaAt(buf, x, 2)) set(buf, x, 2, hi);
  };

  const styleFloppy = (buf, color) => {
    const [hi, base] = shades(color);
    rect(buf, HX0, 2, HX1, 4, base);
    for (let x = HX0 - 1; x <= HX1 + 1; x++) set(buf, x, 3, base);
    rect(buf, HX0 - 1, 4, HX1 + 1, 5, base);
    for (let x = HX0; x <= HX1; x++) set(buf, x, 5, base);
    for (let x = 6; x <= 12; x++) set(buf, x, 6, base);
    set(buf, 9, 7, base); set(buf, 10, 7, base); set(buf, 11, 7, base);
    for (let y = 6; y < 9; y++) { set(buf, HX0 - 1, y, base); set(buf, HX0, y, base); set(buf, HX1, y, base); set(buf, HX1 + 1, y, base); }
    for (let x = HX0; x <= HX1; x++) if (alphaAt(buf, x, 2)) set(buf, x, 2, hi);
    for (const x of [7, 8, 9]) set(buf, x, 6, hi);
  };

  const styleFrame = (buf, color, skinBase, a) => {
    const [hi, base, sh] = shades(color);
    const length = a.length || 17, vol = a.vol || 1;
    rect(buf, HX0 - 1, 2, HX1 + 1, 5, base);
    for (let x = HX0 - 1; x <= HX1 + 1; x++) set(buf, x, 3, base);
    for (let x = HX0; x <= HX1; x++) set(buf, x, 5, base);
    for (let x = 6; x < 12; x++) set(buf, x, 6, base);
    set(buf, 8, 6, skinBase); set(buf, 9, 6, skinBase);
    for (let y = 6; y <= length; y++) {
      for (let dx = 0; dx < vol; dx++) { set(buf, HX0 - 1 - dx, y, base); set(buf, HX1 + 1 + dx, y, base); }
      set(buf, HX0, y, base); set(buf, HX1, y, base);
    }
    for (let x = HX0 - 1; x < HX0 + 1; x++) set(buf, x, length + 1, base);
    for (let x = HX1; x < HX1 + 2; x++) set(buf, x, length + 1, base);
    for (let y = 2; y < 6; y++) if (alphaAt(buf, HX1, y)) set(buf, HX1, y, sh);
    for (let x = HX0; x < 9; x++) if (alphaAt(buf, x, 2)) set(buf, x, 2, hi);
  };

  const styleBun = (buf, color, skinBase) => {
    const [hi, base] = shades(color);
    rect(buf, HX0, 3, HX1, 5, base);
    for (let x = HX0 - 1; x <= HX1 + 1; x++) set(buf, x, 4, base);
    for (let x = HX0; x <= HX1; x++) set(buf, x, 5, base);
    for (let x = 6; x < 12; x++) set(buf, x, 6, base);
    set(buf, 8, 6, skinBase); set(buf, 9, 6, skinBase);
    for (let y = 6; y < 9; y++) { set(buf, HX0, y, base); set(buf, HX1, y, base); }
    rect(buf, 7, 1, 10, 2, base);
    for (let x = HX0; x <= HX1; x++) if (alphaAt(buf, x, 3)) set(buf, x, 3, hi);
  };

  const styleCurly = (buf, color, skinBase) => {
    const [hi, base] = shades(color);
    const pts = [[4, 3], [5, 2], [6, 3], [7, 2], [8, 3], [9, 2], [10, 3], [11, 2], [12, 3], [13, 3],
      [3, 4], [4, 4], [13, 4], [14, 4], [3, 5], [4, 5], [13, 5], [14, 5], [3, 6], [13, 6], [4, 6], [12, 6], [3, 7], [13, 7], [4, 7]];
    rect(buf, HX0, 3, HX1, 5, base);
    for (let x = HX0 - 1; x <= HX1 + 1; x++) set(buf, x, 4, base);
    for (const [x, y] of pts) set(buf, x, y, base);
    for (let x = 6; x < 12; x++) set(buf, x, 6, base);
    set(buf, 8, 6, skinBase); set(buf, 9, 6, skinBase);
    for (const [x, y] of [[5, 2], [7, 2], [9, 2], [11, 2]]) set(buf, x, y, hi);
  };

  const styleMessy = (buf, color, skinBase, a) => {
    const [hi, base] = shades(color);
    const length = a.length || 8;
    rect(buf, HX0 - 1, 2, HX1 + 1, 5, base);
    const spikes = [[3, 2], [5, 1], [7, 2], [9, 1], [11, 2], [13, 1], [14, 2], [4, 2], [12, 2]];
    for (const [x, y] of spikes) set(buf, x, y, base);
    for (let x = HX0; x <= HX1; x++) set(buf, x, 5, base);
    for (let x = 6; x < 12; x++) set(buf, x, 6, base);
    set(buf, 8, 6, skinBase); set(buf, 9, 6, skinBase);
    for (let y = 6; y <= length; y++) { set(buf, HX0 - 1, y, base); set(buf, HX0, y, base); set(buf, HX1, y, base); set(buf, HX1 + 1, y, base); }
    for (const [x, y] of spikes) set(buf, x, y, hi);
  };

  const styleRecede = (buf, color, skinBase) => {
    const [, base, sh] = shades(color);
    for (let y = 4; y < 10; y++) { set(buf, HX0 - 1, y, base); set(buf, HX0, y, base); set(buf, HX1, y, base); set(buf, HX1 + 1, y, base); }
    for (let x = HX0; x <= HX1; x++) set(buf, x, 4, base);
    for (let x = HX0 + 1; x < HX1; x++) set(buf, x, 5, base);
    for (let y = 5; y < 9; y++) for (let x = 6; x < 12; x++) if (eq(rgbAt(buf, x, y), base)) set(buf, x, y, skinBase);
    for (let x = HX0; x <= HX1; x++) if (alphaAt(buf, x, 4)) set(buf, x, 4, sh);
  };

  const styleSpiky = (buf, color, skinBase) => {
    const [hi, base] = shades(color);
    rect(buf, HX0, 3, HX1, 5, base);
    for (let x = HX0 - 1; x <= HX1 + 1; x++) set(buf, x, 4, base);
    for (let x = HX0; x <= HX1; x++) set(buf, x, 5, base);
    const spikes = [[5, 2], [7, 1], [9, 2], [11, 1], [6, 2], [8, 2], [10, 2], [12, 2]];
    for (const [x, y] of spikes) set(buf, x, y, base);
    for (let x = 6; x < 12; x++) set(buf, x, 6, base);
    set(buf, 8, 6, skinBase); set(buf, 9, 6, skinBase);
    for (let y = 6; y < 8; y++) { set(buf, HX0, y, base); set(buf, HX1, y, base); }
    for (const [x, y] of spikes) set(buf, x, y, hi);
  };

  const styleBald = (buf, color, skinBase, a) => {
    const [shi, sbase, ssh] = shades(skinBase, 1.1, 0.82);
    for (let x = 6; x <= 11; x++) set(buf, x, 2, sbase);
    for (let x = 5; x <= 12; x++) set(buf, x, 3, sbase);
    for (let x = HX0; x <= HX1; x++) set(buf, x, 4, sbase);
    for (const x of [7, 8, 9]) set(buf, x, 2, shi);
    set(buf, 6, 3, shi); set(buf, 7, 3, shi);
    set(buf, 5, 3, ssh); set(buf, 12, 3, ssh); set(buf, HX1, 4, ssh);
    const [, base, sh] = shades(color);
    const top = a.recede ? 8 : 6;
    for (let y = top; y <= 10; y++) {
      set(buf, HX0 - 1, y, base); set(buf, HX0, y, base);
      set(buf, HX1, y, base); set(buf, HX1 + 1, y, base);
    }
    for (let y = top; y <= 10; y++) { set(buf, HX0 - 1, y, sh); set(buf, HX1 + 1, y, sh); }
  };

  const HAIR_FNS = { styleShort, styleFloppy, styleFrame, styleBun, styleCurly, styleMessy, styleRecede, styleSpiky, styleBald };

  function drawFacial(buf, kind, color) {
    const [, base, sh] = shades(color);
    if (kind === 'mustache') {
      for (const x of [6, 7, 8, 9, 10]) set(buf, x, 13, base);
      set(buf, 6, 12, base); set(buf, 10, 12, base);
    } else if (kind === 'mustacheSm') {
      for (const x of [7, 8, 9]) set(buf, x, 13, base);
    } else if (kind === 'stubble') {
      for (const [x, y] of [[5, 14], [6, 15], [7, 15], [8, 15], [9, 15], [10, 15], [11, 14], [12, 13], [4, 13], [5, 15], [10, 15]])
        set(buf, x, y, sh, 150);
    } else if (kind === 'goatee') {
      for (const x of [8, 9]) set(buf, x, 15, base);
      set(buf, 8, 14, base); set(buf, 9, 14, base);
      for (const x of [7, 8, 9, 10]) set(buf, x, 13, base);
    }
  }

  function drawGlasses(buf) {
    const frame = [60, 54, 62], glint = [236, 240, 246];
    for (const x of [5, 6]) { set(buf, x, 8, frame); set(buf, x, 10, frame); }
    set(buf, 4, 9, frame); set(buf, 7, 9, frame);
    set(buf, 4, 8, frame); set(buf, 7, 8, frame);
    for (const x of [10, 11]) { set(buf, x, 8, frame); set(buf, x, 10, frame); }
    set(buf, 9, 9, frame); set(buf, 12, 9, frame);
    set(buf, 9, 8, frame); set(buf, 12, 8, frame);
    set(buf, 8, 8, frame);
    set(buf, 3, 9, frame); set(buf, 13, 9, frame);
    set(buf, 4, 8, glint); set(buf, 9, 8, glint);
  }

  function bodyShape(buf, col, heavy = false) {
    const [, base, sh] = shades(col);
    const rows = heavy
      ? [[19, 5, 12], [20, 3, 14], [21, 2, 15], [22, 1, 16], [23, 1, 16], [24, 0, 17], [25, 0, 17], [26, 0, 17], [27, 0, 17]]
      : [[19, 6, 11], [20, 4, 13], [21, 3, 14], [22, 2, 15], [23, 2, 15], [24, 1, 16], [25, 1, 16], [26, 1, 16], [27, 1, 16]];
    for (const [y, a, b] of rows) rect(buf, a, y, b, y, base);
    const [lo, hi] = heavy ? [1, 16] : [2, 15];
    for (let y = 22; y < 28; y++) { set(buf, lo, y, sh); set(buf, hi, y, sh); }
  }

  function drawClothing(buf, kind, c1, c2, tie, skin, heavy = false) {
    const [hi, base, sh] = shades(c1);
    bodyShape(buf, c1, heavy);
    if (kind === 'suit') {
      const white = [238, 238, 236];
      for (const [x, y] of [[8, 19], [9, 19], [7, 20], [8, 20], [9, 20], [10, 20], [8, 21], [9, 21]]) set(buf, x, y, white);
      for (const [x, y] of [[6, 20], [7, 21], [11, 20], [10, 21], [6, 21], [11, 21]]) set(buf, x, y, sh);
      if (tie) { for (let y = 20; y < 26; y++) { set(buf, 8, y, tie); set(buf, 9, y, tie); } set(buf, 8, 20, shades(tie)[0]); }
      else for (let y = 22; y < 26; y++) { set(buf, 8, y, white); set(buf, 9, y, white); }
    } else if (kind === 'dressshirt') {
      for (const [x, y] of [[6, 19], [7, 19], [10, 19], [11, 19], [7, 20], [10, 20]]) set(buf, x, y, sh);
      for (let y = 20; y < 27; y += 2) set(buf, 8, y, sh);
      if (tie) for (let y = 19; y < 26; y++) { set(buf, 8, y, tie); set(buf, 9, y, tie); }
    } else if (kind === 'polo') {
      for (const [x, y] of [[6, 19], [7, 19], [10, 19], [11, 19]]) set(buf, x, y, hi);
      set(buf, 8, 20, sh); set(buf, 8, 22, sh);
      const accent = c2 ? shades(c2)[1] : hi;
      for (const [x, y] of [[7, 20], [9, 20]]) set(buf, x, y, accent);
    } else if (kind === 'blouse') {
      const s = SKIN[skin];
      for (const [x, y] of [[7, 19], [8, 19], [9, 19], [10, 19], [8, 20], [9, 20]]) set(buf, x, y, s.sh);
      for (let x = 5; x < 13; x++) if (eq(rgbAt(buf, x, 20), base)) set(buf, x, 20, hi);
    } else if (kind === 'cardigan') {
      const inner = c2 ? shades(c2)[1] : [235, 233, 226];
      for (let y = 19; y < 27; y++) { set(buf, 8, y, inner); set(buf, 9, y, inner); }
      for (const [x, y] of [[6, 19], [7, 19], [10, 19], [11, 19]]) set(buf, x, y, sh);
    } else if (kind === 'sweater') {
      for (const [x, y] of [[6, 19], [7, 19], [8, 19], [9, 19], [10, 19], [11, 19]]) set(buf, x, y, sh);
    }
  }

  function collarNeck(buf, skin) {
    rect(buf, 7, 18, 10, 19, SKIN[skin].sh);
  }

  const SHOE = [44, 40, 48];
  function drawSceneLegs(buf, pants, phase) {
    const [, base, sh] = shades(pants);
    for (const [lx0, lx1] of [[5, 7], [10, 12]]) {
      rect(buf, lx0, 25, lx1, 30, base);
      for (let y = 25; y <= 30; y++) set(buf, lx1, y, sh);
    }
    const leftLow = phase !== 1, rightLow = phase !== 2;
    rect(buf, 5, leftLow ? 31 : 30, 7, leftLow ? 31 : 30, SHOE);
    rect(buf, 10, rightLow ? 31 : 30, 12, rightLow ? 31 : 30, SHOE);
  }

  function drawSceneTorso(buf, r, back) {
    const [hi, base, sh] = shades(r.c1);
    if (r.heavy) {
      rect(buf, 3, 18, 14, 18, base);
      rect(buf, 2, 19, 15, 19, base);
      rect(buf, 2, 20, 15, 24, base);
      for (let y = 20; y <= 24; y++) { set(buf, 2, y, sh); set(buf, 15, y, sh); set(buf, 14, y, sh); }
    } else {
      rect(buf, 4, 18, 13, 18, base);
      rect(buf, 3, 19, 14, 19, base);
      rect(buf, 4, 20, 13, 24, base);
      for (let y = 20; y <= 24; y++) { set(buf, 3, y, sh); set(buf, 14, y, sh); set(buf, 13, y, sh); }
    }
    if (back) {
      rect(buf, 6, 18, 11, 18, sh);
      for (let y = 19; y <= 24; y++) set(buf, 8, y, sh);
      return;
    }
    const skin = SKIN[r.skin];
    if (r.cloth === 'suit') {
      const white = [238, 238, 236];
      for (const [x, y] of [[8, 18], [9, 18], [7, 19], [8, 19], [9, 19], [10, 19], [8, 20], [9, 20]]) set(buf, x, y, white);
      for (const [x, y] of [[6, 19], [7, 20], [11, 19], [10, 20]]) set(buf, x, y, sh);
      if (r.tie) { for (let y = 19; y <= 24; y++) { set(buf, 8, y, r.tie); set(buf, 9, y, r.tie); } set(buf, 8, 19, shades(r.tie)[0]); }
    } else if (r.cloth === 'dressshirt') {
      for (const [x, y] of [[6, 18], [7, 18], [10, 18], [11, 18], [7, 19], [10, 19]]) set(buf, x, y, sh);
      if (r.tie) for (let y = 18; y <= 24; y++) { set(buf, 8, y, r.tie); set(buf, 9, y, r.tie); }
      else for (let y = 20; y <= 24; y += 2) set(buf, 8, y, sh);
    } else if (r.cloth === 'polo') {
      for (const [x, y] of [[6, 18], [7, 18], [10, 18], [11, 18]]) set(buf, x, y, hi);
      set(buf, 8, 19, sh); set(buf, 8, 21, sh);
    } else if (r.cloth === 'blouse') {
      for (const [x, y] of [[7, 18], [8, 18], [9, 18], [10, 18], [8, 19], [9, 19]]) set(buf, x, y, skin.sh);
      for (let x = 5; x < 13; x++) if (eq(rgbAt(buf, x, 19), base)) set(buf, x, 19, hi);
    } else if (r.cloth === 'cardigan') {
      const inner = r.c2 ? shades(r.c2)[1] : [235, 233, 226];
      for (let y = 18; y <= 24; y++) { set(buf, 8, y, inner); set(buf, 9, y, inner); }
      for (const [x, y] of [[6, 18], [7, 18], [10, 18], [11, 18]]) set(buf, x, y, sh);
    } else if (r.cloth === 'sweater') {
      for (const [x, y] of [[6, 18], [7, 18], [8, 18], [9, 18], [10, 18], [11, 18]]) set(buf, x, y, sh);
    }
  }

  function drawHeadBack(buf, r) {
    const s = SKIN[r.skin];
    if (r.hair === 'styleBald') { drawHeadBackBald(buf, r); return; }
    const [hi, base, sh] = shades(r.hairc);
    const rows = [
      [2, 6, 11], [3, 5, 12], [4, 4, 13], [5, 4, 13], [6, 4, 13], [7, 4, 13], [8, 4, 13],
      [9, 4, 13], [10, 4, 13], [11, 4, 13], [12, 4, 13], [13, 5, 12], [14, 6, 11],
    ];
    for (const [y, a, b] of rows) rect(buf, a, y, b, y, base);
    const len = r.hair === 'styleFrame' ? (r.hairargs?.length || 17)
              : r.hair === 'styleMessy' ? (r.hairargs?.length || 9) : 0;
    for (let y = 11; y <= len; y++) { set(buf, HX0 - 1, y, base); set(buf, HX0, y, base); set(buf, HX1, y, base); set(buf, HX1 + 1, y, base); }
    for (let y = 4; y <= 12; y++) { set(buf, 4, y, sh); set(buf, 13, y, sh); }
    for (const [x, y] of [[5, 3], [12, 3], [5, 13], [12, 13], [6, 14], [11, 14]]) set(buf, x, y, sh);
    for (const [x, y] of [[7, 2], [8, 2], [9, 2], [10, 2], [7, 3], [8, 3], [9, 3]]) set(buf, x, y, hi);
    for (let y = 4; y <= 11; y++) set(buf, 9, y, hi);
    for (let y = 4; y <= 12; y++) set(buf, 8, y, sh);
    rect(buf, 7, 14, 10, 14, sh);
    rect(buf, 7, 15, 10, 17, s.sh);
    rect(buf, 7, 15, 9, 15, s.base);
  }

  function drawHeadBackBald(buf, r) {
    const s = SKIN[r.skin];
    const [shi, sbase, ssh] = shades(s.base, 1.1, 0.82);
    const rows = [
      [2, 6, 11], [3, 5, 12], [4, 4, 13], [5, 4, 13], [6, 4, 13], [7, 4, 13], [8, 4, 13],
      [9, 4, 13], [10, 4, 13], [11, 4, 13], [12, 4, 13], [13, 5, 12], [14, 6, 11],
    ];
    for (const [y, a, b] of rows) rect(buf, a, y, b, y, sbase);
    for (let y = 4; y <= 12; y++) { set(buf, 4, y, ssh); set(buf, 13, y, ssh); }
    for (const [x, y] of [[7, 2], [8, 2], [9, 2], [8, 3], [9, 4], [9, 5]]) set(buf, x, y, shi);
    const [, base, sh] = shades(r.hairc);
    for (let x = 4; x <= 13; x++) { set(buf, x, 11, base); set(buf, x, 12, base); }
    for (const x of [4, 13]) { set(buf, x, 11, sh); set(buf, x, 12, sh); }
    rect(buf, 7, 14, 10, 14, s.sh);
    rect(buf, 7, 15, 10, 17, s.sh);
    rect(buf, 7, 15, 9, 15, s.base);
  }

  function drawHeavyFace(buf, skin) {
    const s = SKIN[skin];
    for (let y = 11; y <= 15; y++) { set(buf, HX0 - 1, y, s.base); set(buf, HX1 + 1, y, s.base); }
    set(buf, HX0 - 1, 15, s.sh); set(buf, HX1 + 1, 15, s.sh);
    for (const x of [5, 6, 11, 12]) set(buf, x, 16, s.base);
    rect(buf, 6, 17, 11, 18, s.base);
    for (const x of [6, 7, 8, 9, 10, 11]) set(buf, x, 18, s.sh);
    set(buf, 7, 17, s.sh); set(buf, 10, 17, s.sh);
  }

  function drawHeadGroup(buf, r) {
    const skinBase = SKIN[r.skin].base;
    drawHead(buf, r.skin);
    if (r.heavy) drawHeavyFace(buf, r.skin);
    drawFace(buf, r.skin, r.brow || 'flat', r.mouth || 'neutral', r.blush || false, r.lashes || false);
    if (r.facial) drawFacial(buf, r.facial, r.hairc);
    (HAIR_FNS[r.hair] || HAIR_FNS.styleShort)(buf, r.hairc, skinBase, r.hairargs || {});
    if (r.glasses) drawGlasses(buf);
  }

  function defaultPants(r) {
    if (r.pants) return r.pants;
    return r.cloth === 'suit' ? shades(r.c1)[2] : [54, 56, 70];
  }

  function outlinePass(buf) {
    const pts = [];
    for (let y = 0; y < CUR_H; y++) {
      for (let x = 0; x < CUR_W; x++) {
        if (alphaAt(buf, x, y) !== 0) continue;
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          if (alphaAt(buf, x + dx, y + dy) === 255) { pts.push([x, y]); break; }
        }
      }
    }
    for (const [x, y] of pts) set(buf, x, y, OUTLINE);
  }

  // Exact Cast Recipes
  const RECIPES = {
    michael:  { skin: 'light', hairc: [58, 42, 28],   hair: 'styleShort',  hairargs: { part: 'L' }, cloth: 'suit', c1: [58, 63, 74], tie: [170, 58, 58], brow: 'flat', mouth: 'smile' },
    jim:      { skin: 'light', hairc: [92, 60, 34],   hair: 'styleFloppy', cloth: 'dressshirt', c1: [172, 196, 224], tie: [120, 130, 150], brow: 'flat', mouth: 'smile' },
    pam:      { skin: 'light', hairc: [120, 76, 42],  hair: 'styleFrame',  hairargs: { length: 18, vol: 2 }, cloth: 'cardigan', c1: [236, 174, 192], c2: [244, 242, 238], brow: 'soft', mouth: 'smile', blush: true, lashes: true },
    dwight:   { skin: 'light', hairc: [64, 48, 28],   hair: 'styleShort',  hairargs: { part: 'L', recede: 1 }, cloth: 'dressshirt', c1: [184, 155, 62], tie: [120, 82, 46], glasses: true, brow: 'angry', mouth: 'neutral' },
    kevin:    { skin: 'light', hairc: [58, 44, 30],   hair: 'styleBald',   cloth: 'polo', c1: [110, 140, 180], c2: [90, 120, 160], brow: 'flat', mouth: 'neutral', heavy: true },
    angela:   { skin: 'light', hairc: [186, 154, 90], hair: 'styleBun',    cloth: 'cardigan', c1: [150, 146, 170], c2: [235, 233, 226], brow: 'angry', mouth: 'frown', lashes: true },
    oscar:    { skin: 'tan',   hairc: [28, 22, 18],   hair: 'styleShort',  hairargs: { part: 'L' }, cloth: 'sweater', c1: [122, 60, 74], brow: 'flat', mouth: 'smile' },
    stanley:  { skin: 'dark',  hairc: [60, 54, 48],   hair: 'styleRecede', cloth: 'dressshirt', c1: [150, 120, 86], tie: [120, 78, 52], glasses: true, facial: 'mustache', brow: 'flat', mouth: 'neutral', heavy: true },
    phyllis:  { skin: 'light', hairc: [196, 162, 110], hair: 'styleCurly', cloth: 'blouse', c1: [202, 160, 192], glasses: true, brow: 'soft', mouth: 'smile', lashes: true, heavy: true },
    andy:     { skin: 'light', hairc: [74, 51, 32],   hair: 'styleShort',  hairargs: { part: 'R' }, cloth: 'polo', c1: [176, 65, 58], c2: [150, 50, 46], brow: 'raised', mouth: 'smile' },
    kelly:    { skin: 'tan',   hairc: [24, 18, 22],   hair: 'styleFrame',  hairargs: { length: 20, vol: 1 }, cloth: 'blouse', c1: [212, 90, 158], brow: 'soft', mouth: 'smile', blush: true, lashes: true },
    ryan:     { skin: 'light', hairc: [42, 32, 24],   hair: 'styleSpiky',  cloth: 'suit', c1: [58, 58, 68], tie: [40, 40, 50], brow: 'flat', mouth: 'neutral' },
    toby:     { skin: 'light', hairc: [106, 90, 66],  hair: 'styleShort',  hairargs: { part: 'L', recede: 1 }, cloth: 'dressshirt', c1: [150, 150, 120], facial: 'mustacheSm', brow: 'soft', mouth: 'frown' },
    creed:    { skin: 'light', hairc: [170, 166, 156], hair: 'styleBald',   cloth: 'dressshirt', c1: [126, 130, 96], facial: 'stubble', brow: 'flat', mouth: 'neutral' },
    meredith: { skin: 'light', hairc: [154, 82, 46],  hair: 'styleMessy',  hairargs: { length: 15 }, cloth: 'blouse', c1: [176, 86, 74], brow: 'raised', mouth: 'smile', lashes: true },
  };

  const OFFICE_CAST = [
    { name: 'michael',  displayName: 'Michael Scott', roleTag: 'BOSS',          accent: 'lemon', blurb: "World's Best Boss", quote: "That's what she said!" },
    { name: 'jim',      displayName: 'Jim Halpert',    roleTag: 'SALES',         accent: 'sky',   blurb: 'Salesman & Job Scout', quote: "Question: What bear is best?" },
    { name: 'pam',      displayName: 'Pam Beesly',     roleTag: 'RECEPTION',     accent: 'coral', blurb: 'Reception & Evidence Vault', quote: "Dunder Mifflin, this is Pam." },
    { name: 'dwight',   displayName: 'Dwight Schrute', roleTag: 'ASST TO REG MGR', accent: 'lemon', blurb: '1-Page PDF Architect', quote: "False! Enforcing 1-page budget." },
    { name: 'ryan',     displayName: 'Ryan Howard',    roleTag: 'TEMP',          accent: 'lilac', blurb: 'Cold Outreach Copywriter', quote: "Just drafted a 3-sentence hook." },
    { name: 'angela',   displayName: 'Angela Martin',  roleTag: 'ACCOUNTING',    accent: 'peach', blurb: 'Quality & Compliance Gate', quote: "First-Reader score must be flawless." },
    { name: 'andy',     displayName: 'Andy Bernard',   roleTag: 'SALES',         accent: 'mint',  blurb: 'Regional Sales & Cornell Pitch', quote: "Rit-dit-dit-di-doo! Cornell '95." },
    { name: 'toby',     displayName: 'Toby Flenderson', roleTag: 'HR ANNEX',      accent: 'coral', blurb: 'Annex Recruiter Radar', quote: "Checking Gmail in the annex..." },
    { name: 'kevin',    displayName: 'Kevin Malone',   roleTag: 'ACCOUNTING',    accent: 'sky',   blurb: 'Famous Chili & Numbers', quote: "Why waste time say lot word?" },
    { name: 'stanley',  displayName: 'Stanley Hudson', roleTag: 'SALES',         accent: 'peach', blurb: 'Pretzel Day Enthusiast', quote: "Did I stutter?" },
    { name: 'oscar',    displayName: 'Oscar Martinez', roleTag: 'ACCOUNTING',    accent: 'lilac', blurb: 'The Rational Consumer', quote: "Actually..." },
    { name: 'phyllis',  displayName: 'Phyllis Vance',  roleTag: 'SALES',         accent: 'coral', blurb: 'Vance Refrigeration', quote: "Bob Vance, Vance Refrigeration." },
    { name: 'kelly',    displayName: 'Kelly Kapoor',   roleTag: 'CUSTOMER SERV', accent: 'coral', blurb: 'Customer Service Diva', quote: "I have a lot of questions." },
    { name: 'creed',    displayName: 'Creed Bratton',  roleTag: 'QA / AUDIT',    accent: 'mint',  blurb: 'Quality Assurance', quote: "Nobody steals from Creed Bratton." },
    { name: 'meredith', displayName: 'Meredith Palmer',roleTag: 'SUPPLIER REL',  accent: 'peach', blurb: 'Supplier Relations', quote: "Did somebody say drinks?" }
  ];

  function composePortrait(r) {
    CUR_W = PORTRAIT_W; CUR_H = PORTRAIT_H;
    const buf = new Uint8ClampedArray(PORTRAIT_W * PORTRAIT_H * 4);
    drawClothing(buf, r.cloth, r.c1, r.c2, r.tie, r.skin, r.heavy || false);
    collarNeck(buf, r.skin);
    drawHeadGroup(buf, r);
    outlinePass(buf);
    return buf;
  }

  function composeScene(r, phase, back) {
    CUR_W = SCENE_W; CUR_H = SCENE_H;
    const buf = new Uint8ClampedArray(SCENE_W * SCENE_H * 4);
    drawSceneTorso(buf, r, back);
    drawSceneLegs(buf, defaultPants(r), phase);
    if (back) drawHeadBack(buf, r);
    else drawHeadGroup(buf, r);
    outlinePass(buf);
    return buf;
  }

  const portraitCache = new Map();
  const sceneCache = new Map();

  function getPortraitBuf(name) {
    let buf = portraitCache.get(name);
    if (!buf) {
      const r = RECIPES[name] || RECIPES.jim;
      buf = composePortrait(r);
      portraitCache.set(name, buf);
    }
    return buf;
  }

  function paintPortrait(ctx, characterName, scale = 2) {
    const buf = getPortraitBuf(characterName);
    const stage = document.createElement('canvas');
    stage.width = PORTRAIT_W; stage.height = PORTRAIT_H;
    const sctx = stage.getContext('2d');
    const img = sctx.createImageData(PORTRAIT_W, PORTRAIT_H);
    img.data.set(buf);
    sctx.putImageData(img, 0, 0);

    ctx.imageSmoothingEnabled = false;
    ctx.clearRect(0, 0, PORTRAIT_W * scale, PORTRAIT_H * scale);
    ctx.drawImage(stage, 0, 0, PORTRAIT_W, PORTRAIT_H, 0, 0, PORTRAIT_W * scale, PORTRAIT_H * scale);
  }

  function getPortraitCanvas(characterName, scale = 2) {
    const canvas = document.createElement('canvas');
    canvas.width = PORTRAIT_W * scale;
    canvas.height = PORTRAIT_H * scale;
    canvas.style.width = `${PORTRAIT_W * scale}px`;
    canvas.style.height = `${PORTRAIT_H * scale}px`;
    canvas.style.imageRendering = 'pixelated';
    const ctx = canvas.getContext('2d');
    paintPortrait(ctx, characterName, scale);
    return canvas;
  }

  function getSceneFrames(characterName) {
    let frames = sceneCache.get(characterName);
    if (!frames) {
      const r = RECIPES[characterName] || RECIPES.jim;
      frames = {
        front: [composeScene(r, 0, false), composeScene(r, 1, false), composeScene(r, 2, false)],
        back: [composeScene(r, 0, true), composeScene(r, 1, true), composeScene(r, 2, true)]
      };
      sceneCache.set(characterName, frames);
    }
    return frames;
  }

  const spriteCanvasCache = new Map();

  function getCachedSceneCanvas(characterName, phase = 0, back = false) {
    const key = `${characterName}_${phase % 3}_${back ? 'back' : 'front'}`;
    let stage = spriteCanvasCache.get(key);
    if (!stage) {
      const frames = getSceneFrames(characterName);
      const buf = (back ? frames.back : frames.front)[phase % 3] || frames.front[0];
      stage = document.createElement('canvas');
      stage.width = SCENE_W;
      stage.height = SCENE_H;
      const sctx = stage.getContext('2d');
      const img = sctx.createImageData(SCENE_W, SCENE_H);
      img.data.set(buf);
      sctx.putImageData(img, 0, 0);
      spriteCanvasCache.set(key, stage);
    }
    return stage;
  }

  function paintSceneSprite(ctx, characterName, phase = 0, back = false, scale = 2, dx = 0, dy = 0) {
    const stage = getCachedSceneCanvas(characterName, phase, back);
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(stage, 0, 0, SCENE_W, SCENE_H, dx, dy, SCENE_W * scale, SCENE_H * scale);
  }

  function paintSeatedSprite(ctx, characterName, phase = 0, back = false, scale = 2, dx = 0, dy = 0) {
    const stage = getCachedSceneCanvas(characterName, phase, back);
    ctx.imageSmoothingEnabled = false;
    // Seated pose: keep top 24px (head + torso + arms), crop bottom 8px (legs tucked under desk)
    ctx.drawImage(stage, 0, 0, SCENE_W, 24, dx, dy, SCENE_W * scale, 24 * scale);
  }

  // Export to global window
  window.PortraitArt = {
    PORTRAIT_W,
    PORTRAIT_H,
    SCENE_W,
    SCENE_H,
    OFFICE_CAST,
    RECIPES,
    paintPortrait,
    getPortraitCanvas,
    paintSceneSprite,
    paintSeatedSprite,
    getSceneFrames
  };

})(window);
