
Plot complex roots of a polynomial in z.

## Requirements
- Python 3.x
- sympy
- matplotlib

## Create a venv (example)
1) python3 -m venv ~/.venvs/preim
2) ~/.venvs/preim/bin/python -m pip install --upgrade pip
3) ~/.venvs/preim/bin/pip install sympy matplotlib

## Wire it up as a CLI
- Ensure the shebang in `~/bin/pReIm.py` points to your venv Python:
  - `#!/home/eko/.venvs/preim/bin/python`
- Make it executable:
  - `chmod +x ~/bin/pReIm.py`
- Make a Symlink:
  - `ln -sf ~/bin/pReIm.py ~/bin/pReIm`

## Put ~/bin on PATH if it isn't already
- bash:
  - `echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc`
  - `source ~/.bashrc`

## Usage
- Show GUI:
  - `pReIm "z^3-1"`
- Save with transparent background:
  - `pReIm "z^3-1" --save --out roots.png --transparent`
