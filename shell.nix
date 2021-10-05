{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "bored-bot-userenv";
  targetPkgs = pkgs: (with pkgs; [
    python39
    python39Packages.pip
    python39Packages.virtualenv
	fish
  ]);
  runScript = ''fish -C "source $(pwd)/venv/bin/activate.fish"'';
}).env
