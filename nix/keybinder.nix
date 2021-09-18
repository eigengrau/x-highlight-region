{ lib, python3Packages }:
python3Packages.buildPythonPackage rec {
  pname = "python3-keybinder";
  version = "1.1.2";
  src = python3Packages.fetchPypi {
    inherit pname version;
    sha256 = "0kwf9r84cpwv5fl2awwivbi1vv802g54ygm37rigp8wplllmk92b";
  };
  doCheck = false;
  meta = with lib; { license = licenses.gpl3; };
}
