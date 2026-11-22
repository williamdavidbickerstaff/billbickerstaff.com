"""Crop sketchbook scans to the page, fix orientation, tidy corners, export for web."""
import sys, json, cv2, numpy as np
from pathlib import Path

SRC = Path(sys.argv[1]); OUT = Path(sys.argv[2]); DBG = Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True); DBG.mkdir(parents=True, exist_ok=True)
LONG_EDGE = 2000

# name: (l, t, r, b, outer_side, rotate)   coords in source px, eyeballed; snapped below
# outer_side: which side has the rounded page corners ('L' / 'R' / None)
# rotate: 0, 90 (clockwise), -90 (counter-clockwise)
P = {
 'CoverFront.jpeg': (105, 40, 1740, 2588, 'R', 0),
 'CoverBack.jpeg':  (145, 45, 1757, 2596, 'L', 0),
 'scan_01.jpg': (95, 49, 1692, 2523, 'R', 0),
 'scan_02.jpg': (15, 21, 1542, 2512, 'R', 0),
 'scan_04.jpg': (70, 10, 1594, 2498, 'R', 0),
 'scan_06.jpg': (35, 14, 1563, 2480, 'R', 0),
 'scan_08.jpg': (58, 21, 1560, 2505, 'R', 0),
 'scan_09.jpg': (206, 14, 1759, 2510, 'L', 0),
 'scan_10.jpg': (21, 14, 1602, 2445, 'R', 0),
 'scan_12.jpg': (18, 21, 1574, 2474, 'R', 0),
 'scan_14.jpg': (14, 21, 1574, 2505, 'R', 0),
 'scan_15.jpg': (226, 56, 1759, 2505, 'L', 0),
 'scan_16.jpg': (88, 56, 1690, 2523, 'L', 0),
 'scan_17.jpg': (267, 84, 1759, 2516, 'L', 0),
 'scan_18.jpg': (21, 35, 1588, 2509, 'R', 0),
 'scan_19.jpg': (280, 56, 1759, 2509, 'L', 0),
 'scan_20.jpg': (28, 14, 1550, 2481, 'R', 0),
 'scan_21.jpg': (290, 81, 1759, 2523, 'L', 0),
 'scan_22.jpg': (21, 28, 1553, 2505, 'R', 0),
 'scan_23.jpg': (322, 128, 1759, 2516, 'L', 0),
 'scan_24.jpg': (115, 62, 1584, 2536, 'R', 0),
 'scan_25.jpg': (246, 49, 1759, 2509, 'L', 0),
 'scan_26.jpg': (10, 35, 1504, 2502, 'R', 90),
 'scan_27.jpg': (274, 70, 1759, 2509, 'L', 0),
 'scan_28.jpg': (21, 21, 1651, 2505, 'R', -90),
 'scan_29.jpg': (100, 56, 1759, 2509, 'L', 0),
 'scan_30.jpg': (34, 28, 1609, 2498, 'R', -90),
 'scan_31.jpg': (100, 21, 1735, 2509, None, 0),
 'scan_32.jpg': (14, 35, 1725, 2492, None, 0),
 'scan_34.jpg': (70, 21, 1739, 2509, None, 0),
 'scan_36.jpg': (70, 35, 1539, 2509, 'R', 0),
 'scan_37.jpg': (397, 49, 1759, 2523, 'L', 0),
 'scan_38.jpg': (112, 56, 1567, 2523, 'R', 0),
 'scan_39.jpg': (387, 14, 1759, 2470, 'L', 0),
 'scan_40.jpg': (91, 21, 1539, 2502, 'R', 0),
 'scan_41.jpg': (390, 98, 1759, 2537, 'L', 0),
 'scan_42.jpg': (105, 14, 1574, 2523, 'R', 0),
}
ONLY = set(sys.argv[4:])
NOSNAP = {('scan_01.jpg','r'), ('scan_09.jpg','l'), ('scan_15.jpg','l'), ('scan_20.jpg','l'), ('scan_21.jpg','l'),
          ('scan_23.jpg','l'), ('scan_23.jpg','t'), ('scan_29.jpg','l'), ('scan_30.jpg','l'), ('scan_32.jpg','b'),
          ('scan_41.jpg','l'), ('scan_31.jpg','l'), ('scan_31.jpg','r'), ('scan_19.jpg','l'), ('scan_30.jpg','b')}
TORN_RIGHT = {'scan_32.jpg', 'scan_34.jpg'}

def profile(g, vertical):
    """Per-column (vertical=True) or per-row fraction of strong-gradient pixels."""
    if vertical:
        d = np.abs(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3))
    else:
        d = np.abs(cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)).T
    n = d.shape[0]
    mid = d[int(n * .2):int(n * .8)]
    hit = cv2.dilate((mid > 30).astype(np.uint8), np.ones((1, 5), np.uint8))
    return hit.mean(0)

def snap(prof, est, limit, inner_dir, win=30):
    """Innermost strong straight edge within +-win of the estimate (inner_dir=+1 means page lies at larger coords)."""
    if est <= 6 or est >= limit - 6:
        return est, None  # side is the image boundary
    lo, hi = max(0, est - win), min(limit - 1, est + win)
    order = range(hi, lo - 1, -1) if inner_dir > 0 else range(lo, hi + 1)
    for i in order:
        if prof[i] >= 0.6 and prof[i] >= prof[max(i-1,0)] and prof[i] >= prof[min(i+1,limit-1)]:
            return i, float(prof[i])
    return est, 0.0

def paper_level(img):
    """Luminance gain so that typical paper is ~250; never darkens."""
    y = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    paper = np.percentile(y, 70)
    gain = min(250.0 / max(paper, 1), 1.25)
    if gain <= 1.0:
        return img, paper
    return np.clip(img.astype(np.float32) * gain, 0, 255).astype(np.uint8), paper

def round_corners(img, side, rad):
    h, w = img.shape[:2]
    # paper colour = median of a band just inside the page
    sample = img[h // 4:3 * h // 4, (w - 120 if side == 'R' else 40):(w - 40 if side == 'R' else 120)]
    col = np.median(sample.reshape(-1, 3), axis=0).astype(np.uint8)
    mask = np.zeros((h, w), np.uint8)
    xs = [w - rad] if side == 'R' else [rad]
    for cx in xs:
        for cy in (rad, h - rad):
            corner = np.zeros((h, w), np.uint8)
            x0 = cx if side == 'R' else 0
            y0 = 0 if cy == rad else cy
            cv2.rectangle(corner, (x0, y0), (x0 + rad, y0 + rad), 255, -1)
            cv2.circle(corner, (cx, cy), rad, 0, -1)
            mask |= corner
    img = img.copy(); img[mask > 0] = col
    return img

def clean_torn_right(img, band=330):
    """Paint out pages/cover visible beyond a torn right edge (cream or dark areas touching the right border)."""
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 1] > 28) | (hsv[..., 2] < 150)).astype(np.uint8)
    m[:, :w - band] = 0
    n, lab = cv2.connectedComponents(m)
    touch = set(np.unique(lab[:, -3:])) - {0}
    keep = np.isin(lab, list(touch)).astype(np.uint8) * 255
    keep = cv2.dilate(keep, np.ones((5, 5), np.uint8))
    col = np.median(img[h // 4:3 * h // 4, w - band - 200:w - band].reshape(-1, 3), axis=0).astype(np.uint8)
    img = img.copy(); img[keep > 0] = col
    return img

def remove_ribbon(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (0, 90, 90), (22, 255, 255))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))  # ignore stray orange specks
    if m.sum() < 255 * 400:
        return img
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61)))  # include the ribbon's shadow
    out = cv2.inpaint(img, m, 15, cv2.INPAINT_TELEA)
    # restore a little paper grain so the patch doesn't look airbrushed
    rng = np.random.default_rng(0)
    grain = rng.normal(0, 2.0, out.shape[:2])[..., None]
    soft = cv2.GaussianBlur(m, (31, 31), 0)[..., None] / 255.0
    return np.clip(out + grain * soft, 0, 255).astype(np.uint8)

report = {}
for name, (l, t, r, b, side, rot) in P.items():
    if ONLY and name not in ONLY:
        continue
    img = cv2.imread(str(SRC / name)); H, W = img.shape[:2]
    g = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (3, 3), 0)
    pv, ph = profile(g, True), profile(g, False)
    def sn(side, prof, est, lim, d):
        return (est, 0.0) if (name, side) in NOSNAP else snap(prof, est, lim, d)
    L, sl = sn('l', pv, l, W, +1); R, sr = sn('r', pv, min(r, W - 1), W, -1)
    T, st = sn('t', ph, t, H, +1); B, sb = sn('b', ph, min(b, H - 1), H, -1)
    inset = 12
    L2 = L + (inset if sl is not None else 0); R2 = R - (inset if sr is not None else 0)
    T2 = T + (inset if st is not None else 0); B2 = B - (inset if sb is not None else 0)
    L2, T2 = max(L2, 0), max(T2, 0); R2, B2 = min(R2, W), min(B2, H)

    dbg = img.copy()
    cv2.rectangle(dbg, (l, t), (r, b), (255, 0, 0), 3)
    cv2.rectangle(dbg, (L2, T2), (R2, B2), (0, 0, 255), 5)
    cv2.imwrite(str(DBG / (Path(name).stem + '.jpg')), cv2.resize(dbg, None, fx=.3, fy=.3, interpolation=cv2.INTER_AREA))

    crop = img[T2:B2, L2:R2]
    if not name.startswith('Cover'):
        crop = remove_ribbon(crop)
        if name in TORN_RIGHT:
            crop = clean_torn_right(crop)
        crop, paper = paper_level(crop)
    else:
        paper = None
    if side:
        crop = round_corners(crop, side, 55)
    if rot == 90:
        crop = cv2.rotate(crop, cv2.ROTATE_90_CLOCKWISE)
    elif rot == -90:
        crop = cv2.rotate(crop, cv2.ROTATE_90_COUNTERCLOCKWISE)
    h, w = crop.shape[:2]
    s = min(1.0, LONG_EDGE / max(h, w))
    if s < 1:
        crop = cv2.resize(crop, (round(w * s), round(h * s)), interpolation=cv2.INTER_AREA)
    out = OUT / name
    cv2.imwrite(str(out), crop, [cv2.IMWRITE_JPEG_QUALITY, 84, cv2.IMWRITE_JPEG_PROGRESSIVE, 1, cv2.IMWRITE_JPEG_OPTIMIZE, 1])
    report[name] = dict(est=(l, t, r, b), snapped=(L, T, R, B),
                        scores=[None if v is None else round(v, 2) for v in (sl, st, sr, sb)],
                        paper=None if paper is None else round(float(paper), 1), out=crop.shape[1::-1])
    print(name, report[name], flush=True)
json.dump(report, open(DBG / 'report.json', 'w'), indent=1)
