# TOOLS

Research-side tooling only: parsers, structure scanners, crosswalk generators, validators, diff/report generators, and migration helpers.

Production converters and build-time tools that directly emit insertion-ready assets belong in Tsubaki. Tools that merely identify or document official source structures belong here in Sakurai.

All tools must consume release/dump identities from project manifests rather than infer ownership from filenames such as `EUR`, `MULTI`, or `REV-ALL`.