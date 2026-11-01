import argparse
import os
import sys

import yt_dlp


def download(url, folder):
    if "instagram.com" not in url.lower():
        print("Error: please enter a valid Instagram URL.")
        return False
    os.makedirs(folder, exist_ok=True)
    options = {
        "outtmpl": os.path.join(folder, "%(title).80s.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print(f"Done! Saved in {folder}")
        return True
    except Exception as error:
        print("Download failed: the video may be private, unavailable, or need login.")
        print(str(error)[:300])
        return False


def main():
    parser = argparse.ArgumentParser(
        prog="reelflow",
        description="ReelFlow - Instagram video downloader",
    )
    parser.add_argument("url", nargs="*", help="Instagram video link(s)")
    parser.add_argument(
        "-o", "--output",
        default=os.path.join(os.path.expanduser("~"), "Downloads", "ReelFlow"),
        help="folder to save videos (default: ~/Downloads/ReelFlow)",
    )
    args = parser.parse_args()

    if args.url:
        results = [download(u, args.output) for u in args.url]
        sys.exit(0 if all(results) else 1)

    print("ReelFlow - paste a link, or type q to quit")
    while True:
        try:
            url = input("\nLink: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if url.lower() in ("q", "quit", "exit"):
            break
        if url:
            download(url, args.output)


if __name__ == "__main__":
    main()
