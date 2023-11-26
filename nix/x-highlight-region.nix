{ atk, cairo, gtk3, gdk-pixbuf, gobject-introspection, pango, wrapGAppsHook
, python3 }:
python3.pkgs.buildPythonApplication {
  pname = "x-highlight-region";
  version = "0.4.1.1";
  nativeBuildInputs =
    [ atk cairo gdk-pixbuf gobject-introspection pango wrapGAppsHook ];
  propagatedBuildInputs =
    (with python3.pkgs; [ pygobject3 pycairo dbus-python xlib keybinder ])
    ++ [ gtk3 ];
  src = ../.;
  preFixup = ''
    makeWrapperArgs+=(
      "''${gappsWrapperArgs[@]}" \
      --unset GDK_SCALE \
      --unset GDK_DPI_SCALE
    )
  '';
}
