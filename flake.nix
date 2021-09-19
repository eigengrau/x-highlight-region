{
  description = "x-highlight-region";
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-21.05";
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
        packages = {
          x-highlight-region = pkgs.x-highlight-region;
          python3 = pkgs.python3;
        };
        defaultPackage = packages.x-highlight-region;
        defaultApp = {
          type = "app";
          program = "${packages.x-highlight-region}/bin/xhighlight";
        };
      }));
}
