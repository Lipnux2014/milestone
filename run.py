from app import app
import argparse

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Development Server Help")
    parse.add_argument("-d", "--debug", action="store_true", dest="debug_mode", default=False)
    parse.add_argument("-p", "--port", dest="port", default=5000)
    cmd_args = parse.parse_args()
    app_options = {"port": int(cmd_args.port)}
    app_options = {"host": "0.0.0.0"}
    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False
    app.run(**app_options)
