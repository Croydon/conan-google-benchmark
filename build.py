from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="inexorgame")
    # Try shared and not-shared builds
    builder.add_common_builds(shared_option_name="c-ares:shared")
builder.run()
