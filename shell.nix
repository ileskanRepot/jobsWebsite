{ pkgs ? import <nixpkgs> {}}:
  pkgs.mkShell {
    nativeBuildInputs = let
      env = pyPkgs : with pyPkgs; [
        fastapi
        uvicorn
        psycopg2
        python-keycloak
        autopep8
        aiosmtplib
      ];
    in with pkgs; [
      (python311.withPackages env)
  ];
}
