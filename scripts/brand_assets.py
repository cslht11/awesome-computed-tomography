#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Brand files for the built site: favicon, touch icon, share image.

Everything here is pure stdlib (html / math / struct / zlib): the build
stays PyYAML-only, so the repository carries no binary blobs and no SVG
renderer or imaging library is needed at build time.

The raster versions re-draw assets/logo.svg's geometry -- two concentric
rings, a fan of three lines, a top dot, a centre ellipse -- with
distance-based anti-aliasing, so the favicon and the share image match
the SVG instead of being a second, drifting logo.
"""

import html
import math
import struct
import zlib

LOGO_BLUE = (92, 107, 192)      # #5c6bc0, the colour in assets/logo.svg
OG_BG_TOP = (27, 32, 68)       # deep indigo, top of the share image
OG_BG_BOTTOM = (47, 55, 112)   # deep indigo, bottom of the share image
WHITE = (255, 255, 255)
OG_SIZE = (1200, 630)          # the size share cards expect
TOUCH_SIZE = 180               # iOS apple-touch-icon
FAVICON_SIZES = (16, 32, 48)   # sizes packed into favicon.ico
OG_ALT = "Awesome Computed Tomography"


def _esc(s):
    return html.escape(str(s), quote=True)


def head_brand(origin):
    """Favicon + share-image <head> lines shared by every page.

    ``origin`` is the site root with a trailing slash, e.g.
    https://computedtomography.org/. One block on every page, so a share
    card or a browser tab never depends on which head builder a page took.
    """
    if not origin.endswith("/"):
        origin += "/"
    lines = [
        '<link rel="icon" href="%sfavicon.svg" type="image/svg+xml">'
        % _esc(origin),
        '<link rel="alternate icon" href="%sfavicon.ico" type="image/x-icon">'
        % _esc(origin),
        '<link rel="apple-touch-icon" href="%sapple-touch-icon.png">'
        % _esc(origin),
        '<meta property="og:image" content="%sog-image.png">' % _esc(origin),
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="%s">' % _esc(OG_ALT),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:image" content="%sog-image.png">' % _esc(origin),
    ]
    return "\n".join(lines)


def _clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


class _Canvas(object):
    """RGBA canvas, one byte per channel, source-over compositing."""

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 4)  # transparent black

    def fill(self, rgb, alpha=255):
        row = bytes([rgb[0], rgb[1], rgb[2], alpha]) * self.w
        for y in range(self.h):
            self.px[y * self.w * 4:(y + 1) * self.w * 4] = row

    def fill_vertical_gradient(self, top, bottom):
        for y in range(self.h):
            t = y / float(max(1, self.h - 1))
            rgb = tuple(int(round(top[i] + (bottom[i] - top[i]) * t))
                        for i in range(3))
            row = bytes([rgb[0], rgb[1], rgb[2], 255]) * self.w
            self.px[y * self.w * 4:(y + 1) * self.w * 4] = row

    def _blend(self, idx, rgb, cov):
        """Composite opaque rgb at coverage cov (0..1) over pixel idx."""
        if cov <= 0:
            return
        if cov > 1:
            cov = 1.0
        da = self.px[idx + 3] / 255.0
        out_a = cov + da * (1.0 - cov)
        if out_a <= 0:
            return
        for c in range(3):
            self.px[idx + c] = int(round(
                (rgb[c] * cov + self.px[idx + c] * da * (1.0 - cov)) / out_a))
        self.px[idx + 3] = int(round(out_a * 255))


def _disk(cv, cx, cy, r, rgb, alpha=1.0):
    x0 = max(0, int(cx - r - 1))
    x1 = min(cv.w - 1, int(cx + r + 1))
    y0 = max(0, int(cy - r - 1))
    y1 = min(cv.h - 1, int(cy + r + 1))
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            cov = _clamp01(r + 0.5 - d) * alpha
            if cov:
                cv._blend((y * cv.w + x) * 4, rgb, cov)


def _ring(cv, cx, cy, r, width, rgb, alpha=1.0):
    x0 = max(0, int(cx - r - width - 1))
    x1 = min(cv.w - 1, int(cx + r + width + 1))
    y0 = max(0, int(cy - r - width - 1))
    y1 = min(cv.h - 1, int(cy + r + width + 1))
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            cov = _clamp01(width / 2.0 + 0.5 - abs(d - r)) * alpha
            if cov:
                cv._blend((y * cv.w + x) * 4, rgb, cov)


def _dashed_ring(cv, cx, cy, r, width, dash, gap, rgb, alpha=1.0):
    circ = 2 * math.pi * r
    period = dash + gap
    x0 = max(0, int(cx - r - width - 1))
    x1 = min(cv.w - 1, int(cx + r + width + 1))
    y0 = max(0, int(cy - r - width - 1))
    y1 = min(cv.h - 1, int(cy + r + width + 1))
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            cov = _clamp01(width / 2.0 + 0.5 - abs(d - r))
            if not cov:
                continue
            ang = math.atan2(y + 0.5 - cy, x + 0.5 - cx)
            t = ((ang + math.pi) / (2 * math.pi) * circ) % period
            if t < 1:
                dc = t  # rising edge of a dash, anti-aliased
            elif t <= dash:
                dc = 1.0
            elif t <= dash + 1:
                dc = dash + 1 - t  # falling edge, anti-aliased
            else:
                dc = 0.0
            if dc:
                cv._blend((y * cv.w + x) * 4, rgb, cov * dc * alpha)


def _line(cv, x1, y1, x2, y2, width, rgb, alpha=1.0):
    m = width / 2.0 + 1
    x0 = max(0, int(min(x1, x2) - m))
    x1b = min(cv.w - 1, int(max(x1, x2) + m))
    y0 = max(0, int(min(y1, y2) - m))
    y1b = min(cv.h - 1, int(max(y1, y2) + m))
    dx, dy = x2 - x1, y2 - y1
    len2 = dx * dx + dy * dy or 1.0
    for y in range(y0, y1b + 1):
        for x in range(x0, x1b + 1):
            px, py = x + 0.5, y + 0.5
            t = ((px - x1) * dx + (py - y1) * dy) / len2
            t = max(0.0, min(1.0, t))
            d = math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))
            cov = _clamp01(width / 2.0 + 0.5 - d) * alpha
            if cov:
                cv._blend((y * cv.w + x) * 4, rgb, cov)


def _ellipse_fill(cv, cx, cy, rx, ry, rgb, alpha=1.0):
    x0 = max(0, int(cx - rx - 1))
    x1 = min(cv.w - 1, int(cx + rx + 1))
    y0 = max(0, int(cy - ry - 1))
    y1 = min(cv.h - 1, int(cy + ry + 1))
    m = min(rx, ry)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            q = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            d = math.sqrt(q)
            cov = _clamp01((1.0 - d) * m + 0.5) * alpha
            if cov:
                cv._blend((y * cv.w + x) * 4, rgb, cov)


def _ellipse_ring(cv, cx, cy, rx, ry, width, rgb, alpha=1.0):
    x0 = max(0, int(cx - rx - width - 1))
    x1 = min(cv.w - 1, int(cx + rx + width + 1))
    y0 = max(0, int(cy - ry - width - 1))
    y1 = min(cv.h - 1, int(cy + ry + width + 1))
    m = min(rx, ry)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            q = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            d = math.sqrt(q)
            cov = _clamp01(width / 2.0 + 0.5 - abs(d - 1.0) * m) * alpha
            if cov:
                cv._blend((y * cv.w + x) * 4, rgb, cov)


def _draw_logo(cv, cx, cy, size, rgb):
    """The assets/logo.svg motif, scaled so viewBox 0 0 64 64 -> size px.

    Paint order follows the SVG: outer ring, dashed ring, fan lines,
    top dot, centre ellipse (fill, then stroke).
    """
    s = size / 64.0
    ox, oy = cx - 32 * s, cy - 32 * s

    def X(v):
        return ox + v * s

    def Y(v):
        return oy + v * s

    _ring(cv, X(32), Y(32), 27 * s, 3 * s, rgb, 1.0)
    _dashed_ring(cv, X(32), Y(32), 19 * s, 2 * s, 2 * s, 3 * s, rgb, 0.5)
    for ex, ey in ((14, 52), (32, 59), (50, 52)):
        _line(cv, X(32), Y(5), X(ex), Y(ey), 2 * s, rgb, 0.6)
    _disk(cv, X(32), Y(5), 4 * s, rgb, 1.0)
    _ellipse_fill(cv, X(32), Y(34), 9 * s, 11 * s, rgb, 0.25)
    _ellipse_ring(cv, X(32), Y(34), 9 * s, 11 * s, 2 * s, rgb, 1.0)


def _png(cv):
    raw = bytearray()
    stride = cv.w * 4
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * stride:(y + 1) * stride]

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff))

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))


def _ico(parts):
    """ICO holding one PNG per size: [(size, png_bytes)]."""
    n = len(parts)
    header = struct.pack("<HHH", 0, 1, n)
    offset = 6 + 16 * n
    entries = b""
    data = b""
    for size, png in parts:
        dim = size if size < 256 else 0
        entries += struct.pack("<BBBBHHII", dim, dim, 0, 0, 1, 32,
                                len(png), offset)
        data += png
        offset += len(png)
    return header + entries + data


def favicon_ico():
    """favicon.ico: the logo at 16, 32 and 48 px on transparency."""
    parts = []
    for size in FAVICON_SIZES:
        cv = _Canvas(size, size)
        _draw_logo(cv, size / 2.0, size / 2.0, size, LOGO_BLUE)
        parts.append((size, _png(cv)))
    return _ico(parts)


def apple_touch_icon():
    """180x180 PNG on white: iOS shows transparency as black, so no alpha."""
    cv = _Canvas(TOUCH_SIZE, TOUCH_SIZE)
    cv.fill(WHITE, 255)
    _draw_logo(cv, TOUCH_SIZE / 2.0, TOUCH_SIZE / 2.0, 150, LOGO_BLUE)
    return _png(cv)


def og_image():
    """1200x630 share image: the logo on deep indigo, fan-beam accent."""
    w, h = OG_SIZE
    cv = _Canvas(w, h)
    cv.fill_vertical_gradient(OG_BG_TOP, OG_BG_BOTTOM)
    # Fan beam radiating from the logo centre, fading into the right half.
    for i in range(7):
        _line(cv, 300, 315, 1150, 315 + (i - 3) * 90, 3, WHITE, 0.10)
    _ring(cv, 300, 315, 260, 2, WHITE, 0.10)
    _dashed_ring(cv, 950, 315, 140, 2, 10, 12, WHITE, 0.12)
    _draw_logo(cv, 300, 315, 360, WHITE)
    return _png(cv)
