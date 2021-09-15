{ pkgs }:
pkgs.python38Packages.buildPythonApplication {
  pname = "x-highlight-region";
  version = "0.4.1.1";
  nativeBuildInputs = (with pkgs; [
    atk
    cairo
    gdk-pixbuf
    gobject-introspection
    pango
    wrapGAppsHook
  ]);
  propagatedBuildInputs = (with pkgs.python38Packages; [
    pygobject3
    pycairo
    dbus-python
    xlib
    keybinder
  ]) ++ (with pkgs; [ gtk3 ]);
  src = ../.;
  preFixup = ''
    makeWrapperArgs+=(
      "''${gappsWrapperArgs[@]}" \
      --unset GDK_SCALE \
      --unset GDK_DPI_SCALE
    )
  '';
}
