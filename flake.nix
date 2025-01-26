{
  inputs = {
    # indirectly reference pinned unstable nixpkgs of my system using the registry
    # source: https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake.html#flake-inputs
    # this should have the effect of not downloading extra packages and using existing store links
    nixpkgs.url = "nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        packages = with pkgs; [
          (python3.withPackages (
            python-pkgs: with python-pkgs; [
              # select Python packages here
              pyside6
              thefuzz
              pydantic
              weaviate-client
              openai
              python-dotenv
              pypdf2
            ]
          ))
        ];
      in
      {
        # mkShell documentation: https://ryantm.github.io/nixpkgs/builders/special/mkshell/
        # mkDerivation docs: https://blog.ielliott.io/nix-docs/mkDerivation.html
        devShells.default = pkgs.mkShell {
          name = "Thing that actually lets me launch gui";
          buildInputs = [ packages ];
          nativeBuildInputs = [ packages ];
        };
      }
    );
}
