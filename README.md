# Slot Machines Project
Users can play and win vitual tokens.

## Prerequisites
1. Install system packages:
   - docker
   - direnv
   - yq
   - sponge

2. Activate `direnv` (execute and/or add to profile):
   ```
   # bash:
   eval "$(direnv hook bash)
   # zsh:
   eval "$(direnv hook zsh)
   ```

3. Create `.envrc` file in repo root, for instance:
   ```
   export PATH="$(pwd)/bin:$PATH"
   source ./.venv/bin/activate
   ```

4. Create virtual env:
   ```
   python -m venv .venv
   ```

5. Exit/enter project folder to activate `.envrc` (and python virtual env)

6. Install `uv` in Python virtual env:
   ```
   pip install uv
   ```

## Usage
1. Compile & build Docker images:
   ```
   build.sh
   ```
2. Start all:
   ```
   docker compose up -d
   ```
