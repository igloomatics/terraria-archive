#!/usr/bin/env python3
"""Terraria China -> International save converter.

Replaces the Chinese-version save signature b"xindong" with b"relogic".
The web UI is served locally and performs conversion in the browser.
"""
from __future__ import annotations

import argparse
import http.server
import pathlib
import socketserver
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def convert_bytes(data: bytes) -> tuple[bytes, int]:
    """Convert one save and return (converted_data, replacement_count).

    The two signatures have equal length (7 bytes), so this is an in-place
    byte replacement and cannot change offsets elsewhere in the save.
    """
    old, new = b"xindong", b"relogic"
    count = data.count(old)
    if count == 0:
        raise ValueError("未找到国服签名 xindong（十六进制 78 69 6E 64 6F 6E 67）")
    return data.replace(old, new), count


def convert_file(src: pathlib.Path, dst: pathlib.Path) -> int:
    data = src.read_bytes()
    converted, count = convert_bytes(data)
    dst.write_bytes(converted)
    return count


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):  # quieter local server
        sys.stderr.write("[web] " + (fmt % args) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Terraria 国服存档转国际服")
    sub = parser.add_subparsers(dest="command")
    p_convert = sub.add_parser("convert", help="转换文件")
    p_convert.add_argument("source", type=pathlib.Path)
    p_convert.add_argument("-o", "--output", type=pathlib.Path)
    p_serve = sub.add_parser("serve", help="启动本地网页")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    if args.command == "convert":
        output = args.output or args.source.with_name(args.source.stem + "_international" + args.source.suffix)
        try:
            count = convert_file(args.source, output)
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
        print(f"已转换：{output}（替换 {count} 处 xindong → relogic）")
        return

    # Default action: launch the web UI.
    host, port = getattr(args, "host", "127.0.0.1"), getattr(args, "port", 8765)
    with socketserver.ThreadingTCPServer((host, port), Handler) as server:
        print(f"打开 http://{host}:{port}/index.html")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")


if __name__ == "__main__":
    main()
