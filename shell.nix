{ pkgs ? import <nixpkgs> {} }:
pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
}
(pkgs.buildFHSUserEnv {
  name = "bored-bot-userenv";
  targetPkgs = pkgs: (with pkgs; [
	fish
  ]);
  extraBuildCommands = ''poetry install'';
  runScript = ''fish -C "source $(pwd)/venv/bin/activate.fish"'';
}).env
