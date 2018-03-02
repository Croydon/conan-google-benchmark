from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="inexorgame")
    builder.add_common_builds(shared_option_name="benchmark:shared")
builder.run()
