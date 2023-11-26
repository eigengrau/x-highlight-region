{
  description = "x-highlight-region";
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.11";
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }:
    (utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            (final: prev: {
              python3 = prev.python3.override {
                packageOverrides = (final-python: prev-python: {
                  keybinder = final-python.callPackage ./nix/keybinder.nix { };
                });
              };
              x-highlight-region =
                final.callPackage ./nix/x-highlight-region.nix { };
            })
          ];
        };
      in rec {
        packages = rec {
          default = x-highlight-region;
          x-highlight-region = pkgs.x-highlight-region;
        };
        apps = {
          default = {
            type = "app";
            program = "${packages.x-highlight-region}/bin/xhighlight";
          };
        };
      }));
}
