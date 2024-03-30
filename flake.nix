{
  outputs = { self, nixpkgs }: {
    devShells.x86_64-linux.default = let
      pkgs = import nixpkgs {
        system = "x86_64-linux";
      };
      luma-core = pkgs.python3Packages.buildPythonPackage rec {
        pname = "luma.core";
        version = "2.4.2";
        src = pkgs.pythonPackages.fetchPypi {
          inherit pname version;
          sha256 = "sha256-ljwmQWTUN09UnVfbCVmeDKRYzqG9BeFpOYl2Gb5Obb0=";
        };
        propagatedBuildInputs = with pkgs.python3Packages; [
          pip
          pillow
          smbus2
          pyftdi
          cbor2
          rpi-gpio
          spidev
        ];
        doCheck = false;
      };
      luma-oled = pkgs.python3Packages.buildPythonPackage rec {
        pname = "luma.oled";
        version = "3.13.0";
        src = pkgs.pythonPackages.fetchPypi {
          inherit pname version;
          sha256 = "sha256-fioNakyWjGSYAlXWgewnkU2avVpmqQGbKJvzrQUMISU=";
        };
        propagatedBuildInputs = with pkgs.python3Packages; [
          luma-core
        ];
        doCheck = false;
      };
      luma-emulator = pkgs.python3Packages.buildPythonPackage rec {
        pname = "luma.emulator";
        version = "1.5.0";
        src = pkgs.pythonPackages.fetchPypi {
          inherit pname version;
          sha256 = "sha256-0PCbFz9BQmXadpL+THw348tU9PgTjhNfixtHFeN4248=";
        };
        propagatedBuildInputs = with pkgs.python3Packages; [
          luma-core
          pygame
        ];
        doCheck = false;
      };
      pystrix = pkgs.python3Packages.buildPythonPackage rec {
        pname = "pystrix";
        version = "1.2.0";
        src = pkgs.pythonPackages.fetchPypi {
          inherit pname version;
          sha256 = "sha256-+ri88pF3hzDXA0zAmegtQCRrNBAE7clYPkmzjQ5uodQ=";
        };
      };
      python-env = pkgs: pkgs.python3.withPackages(ps: with ps; [
        luma-core luma-oled luma-emulator pystrix
      ]);
    in pkgs.mkShell {
      buildInputs = [
        (python-env pkgs)
      ];
    };
  };
}
