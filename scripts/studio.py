#!/usr/bin/env python3
"""Validate a local product manifest and build a portable offline studio."""
import argparse
import base64
import json
import re
import struct
import sys
import zlib
from pathlib import Path

SIGNATURE = b'\x89PNG\r\n\x1a\n'
MAX_FILE = 15 * 1024 * 1024
MAX_TOTAL = 80 * 1024 * 1024
TEXT_LIMITS = {'name': 80, 'brand': 40, 'kicker': 80, 'headline': 80, 'tagline': 100}


def png_stats(data):
    if len(data) > MAX_FILE or not data.startswith(SIGNATURE):
        raise ValueError('Expected a PNG no larger than 15 MB.')
    offset, width, height, depth, color, interlace = 8, 0, 0, 0, 0, 0
    compressed, ended = bytearray(), False
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError('Truncated PNG chunk.')
        length = struct.unpack('>I', data[offset:offset+4])[0]
        kind = data[offset+4:offset+8]
        end = offset + 12 + length
        if end > len(data):
            raise ValueError('Invalid PNG chunk length.')
        payload = data[offset+8:offset+8+length]
        crc = struct.unpack('>I', data[end-4:end])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise ValueError('PNG checksum mismatch.')
        if offset == 8 and kind != b'IHDR':
            raise ValueError('Missing PNG header.')
        if kind == b'IHDR':
            if width or length != 13:
                raise ValueError('Invalid PNG header.')
            width, height, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', payload)
            if not width or not height or width * height > 16000000:
                raise ValueError('PNG must contain at most 16 million pixels.')
            if compression or filtering or interlace or depth != 8 or color not in (4, 6):
                raise ValueError('Use a non-interlaced 8-bit RGBA or grayscale-alpha PNG.')
        elif kind == b'IDAT':
            compressed.extend(payload)
        elif kind == b'IEND':
            if length or end != len(data):
                raise ValueError('Invalid PNG ending.')
            ended = True
            break
        offset = end
    if not ended or not compressed:
        raise ValueError('Incomplete PNG.')
    bpp = 4 if color == 6 else 2
    stride = width * bpp
    expected = (stride + 1) * height
    inflater = zlib.decompressobj()
    raw = inflater.decompress(compressed, expected + 1)
    if len(raw) != expected or not inflater.eof or inflater.unconsumed_tail or inflater.unused_data:
        raise ValueError('PNG pixel data does not match its dimensions.')
    previous = bytearray(stride)
    transparent = visible = 0
    for y in range(height):
        start = y * (stride + 1)
        method = raw[start]
        row = bytearray(raw[start+1:start+1+stride])
        if method > 4:
            raise ValueError('Unknown PNG filter.')
        for x in range(stride):
            left = row[x-bpp] if x >= bpp else 0
            up = previous[x]
            corner = previous[x-bpp] if x >= bpp else 0
            if method == 1: prediction = left
            elif method == 2: prediction = up
            elif method == 3: prediction = (left + up) // 2
            elif method == 4:
                p = left + up - corner
                a, b, c = abs(p-left), abs(p-up), abs(p-corner)
                prediction = left if a <= b and a <= c else up if b <= c else corner
            else: prediction = 0
            row[x] = (row[x] + prediction) & 255
        for alpha in row[bpp-1::bpp]:
            transparent += alpha == 0
            visible += alpha > 0
        previous = row
    if not visible:
        raise ValueError('PNG contains no visible artwork.')
    if not transparent:
        raise ValueError('PNG has no fully transparent pixels.')
    return {'width': width, 'height': height, 'transparentPercent': round(100 * transparent / (width * height), 2)}


def load_project(manifest):
    if manifest.stat().st_size > 120 * 1024 * 1024:
        raise ValueError('Manifest exceeds 120 MB.')
    project = json.loads(manifest.read_text(encoding='utf-8'))
    if not isinstance(project, dict) or project.get('schemaVersion') != 1:
        raise ValueError('Unsupported project schema; expected version 1.')
    clean = {'schemaVersion': 1}
    for key, limit in TEXT_LIMITS.items():
        value = project.get(key, '')
        if not isinstance(value, str) or len(value) > limit:
            raise ValueError(f'{key} must be text no longer than {limit} characters.')
        clean[key] = value
    assets = project.get('assets')
    if not isinstance(assets, list) or not 1 <= len(assets) <= 32:
        raise ValueError('A collection must contain 1–32 assets.')
    root, seen, filenames, total, stats = manifest.parent.resolve(), set(), set(), 0, []
    clean['assets'] = []
    for asset in assets:
        if not isinstance(asset, dict):
            raise ValueError('Invalid asset entry.')
        ident, name, filename = asset.get('id'), asset.get('name'), asset.get('filename')
        if not isinstance(ident, str) or not re.fullmatch(r'[a-z0-9-]{1,64}', ident) or ident in seen:
            raise ValueError('Asset IDs must be unique lowercase letters, digits, or hyphens.')
        seen.add(ident)
        if not isinstance(name, str) or not 1 <= len(name) <= 80:
            raise ValueError('Asset names must contain 1–80 characters.')
        if not isinstance(filename, str) or len(filename) > 120 or not filename.lower().endswith('.png') or any(c in filename for c in '/\\') or '..' in filename:
            raise ValueError('Asset filename must be a PNG basename.')
        if filename in filenames:
            raise ValueError('Asset filenames must be unique.')
        filenames.add(filename)
        if ('file' in asset) == ('dataURL' in asset):
            raise ValueError('Each asset must have either file or dataURL, exclusively.')
        if 'file' in asset:
            if not isinstance(asset['file'], str):
                raise ValueError('Asset file must be a relative path.')
            relative = Path(asset['file'])
            candidate = (root / relative).resolve()
            if relative.is_absolute() or not candidate.is_relative_to(root):
                raise ValueError('Asset path escapes the project folder.')
            if candidate.stat().st_size > MAX_FILE:
                raise ValueError('PNG exceeds 15 MB.')
            data = candidate.read_bytes()
        else:
            value = asset['dataURL']
            prefix = 'data:image/png;base64,'
            if not isinstance(value, str) or not value.startswith(prefix) or len(value) > MAX_FILE * 4 // 3 + 100:
                raise ValueError('Expected a bounded PNG data URL.')
            data = base64.b64decode(value[len(prefix):], validate=True)
        total += len(data)
        if total > MAX_TOTAL:
            raise ValueError('Collection exceeds 80 MB of PNG data.')
        stats.append({'id': ident, **png_stats(data)})
        clean['assets'].append({'id': ident, 'name': name, 'filename': filename, 'dataURL': 'data:image/png;base64,' + base64.b64encode(data).decode('ascii')})
    settings = project.get('settings', {})
    if not isinstance(settings, dict):
        raise ValueError('settings must be an object.')
    allowed = {'layout': ('campaign','slide','social'), 'arrangement': ('one','two','all'), 'product': tuple(seen), 'placement': ('left','right','center'), 'theme': ('spring','summer','autumn','winter')}
    clean['settings'] = {}
    for key, choices in allowed.items():
        if key in settings:
            if settings[key] not in choices: raise ValueError(f'Invalid setting: {key}.')
            clean['settings'][key] = settings[key]
    if 'scale' in settings:
        value = settings['scale']
        if isinstance(value, bool) or not isinstance(value, (int,float)) or not 40 <= value <= 110: raise ValueError('Invalid scale.')
        clean['settings']['scale'] = value
    if 'checker' in settings:
        if not isinstance(settings['checker'], bool): raise ValueError('Invalid checker setting.')
        clean['settings']['checker'] = settings['checker']
    return clean, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate','build'))
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'build' and (args.output is None or args.output.exists() or args.output.is_symlink()):
            raise ValueError('Build requires a new output filename; originals are never overwritten.')
        project, stats = load_project(args.manifest)
        if args.command == 'build':
            template = Path(__file__).resolve().parents[1] / 'assets' / 'studio-template.html'
            source = template.read_text(encoding='utf-8')
            if source.count('__PROJECT_JSON__') != 1:
                raise ValueError('Studio template placeholder is missing or duplicated.')
            encoded = json.dumps(project, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
            source = source.replace('__PROJECT_JSON__', encoded)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x', encoding='utf-8') as target:
                target.write(source)
        print(json.dumps({'ok': True, 'assets': stats, 'output': str(args.output) if args.command == 'build' else None}, indent=2))
    except (OSError, ValueError, zlib.error) as error:
        print(json.dumps({'ok': False, 'error': str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
