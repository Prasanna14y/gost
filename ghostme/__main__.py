import argparse
import logging
import webbrowser
import threading

from ghostme.app import run


def main():
    parser = argparse.ArgumentParser(description="GhostMe - iPhone Location Spoofer")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    url = f"http://{args.host}:{args.port}"
    print(f"\n  GhostMe v1.0.0")
    print(f"  Running at {url}")
    print(f"  Press Ctrl+C to quit\n")

    if not args.no_browser:
        threading.Timer(1.0, webbrowser.open, args=(url,)).start()

    run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
